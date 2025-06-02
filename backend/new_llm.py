import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

def create_retriever(document_path: str):
    loader = PyPDFLoader(document_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    vector_store = Chroma.from_documents(docs, embeddings, collection_name="my_docs")

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    return retriever

def create_doc_qa_chain(retriever):
    llm = ChatGroq(api_key=GROQ_API_KEY, model="llama3-8b-8192", temperature=0.4, max_retries=2)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
    return qa_chain

def create_general_chain():
    llm = ChatGroq(api_key=GROQ_API_KEY, model="llama3-8b-8192", temperature=0.4, max_retries=2)
    prompt = PromptTemplate(template="{input}", input_variables=["input"])

    def general_func(messages):
        # messages is a list of HumanMessage and AIMessage
        # Format messages into a single prompt string for Groq chat model
        conversation = ""
        for msg in messages:
            role = "User" if isinstance(msg, HumanMessage) else "Assistant"
            conversation += f"{role}: {msg.content}\n"
        prompt_text = prompt.format(input=conversation)
        return llm.invoke(prompt_text).content

    return general_func

def router_func(query: str) -> str:
    keywords = ["project", "file", "content", "document"]
    if any(k in query.lower() for k in keywords):
        return "document_qa"
    else:
        return "general"


def chat_func(message:str, doc_chain, general_chain, chat_history) -> str:
    try:
        route = router_func(message)
        if route == "document_qa":
            # RetrievalQA expects a string query, no chat history
            response = doc_chain.invoke({"query": message})
            result = response["result"]
            # Append user and bot messages to history
            chat_history.append(HumanMessage(content=message))
            chat_history.append(AIMessage(content=result))
        else:
            # For general chat, pass full chat history including new user message
            chat_history.append(HumanMessage(content=message))
            result = general_chain(chat_history)
            chat_history.append(AIMessage(content=result))

        return result
    except Exception as e:
        return str(e)