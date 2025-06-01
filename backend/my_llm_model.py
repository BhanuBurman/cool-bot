# import os
# from dotenv import load_dotenv
# from langchain_core.messages import HumanMessage, AIMessage
# from langchain_core.messages.utils import count_tokens_approximately
# from langchain_groq import ChatGroq
# from langchain_core.output_parsers import StrOutputParser
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_chroma import Chroma
# from langchain.chains import RetrievalQA
# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.graph import START, MessagesState, StateGraph
# from langchain_core.messages import trim_messages
#
# load_dotenv()
# GROQ_API_KEY = os.getenv('GROQ_API_KEY')
#
#
# def vector_store_retriever(document_path: str):
#     loader = PyPDFLoader(document_path)
#     documents = loader.load()
#
#     splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     docs = splitter.split_documents(documents)
#
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
#     vector_store = Chroma(
#         collection_name="pdf_collection",
#         embedding_function=embeddings,
#         persist_directory="./data",
#     )
#
#     existing_docs = vector_store.get()
#     if not existing_docs or len(existing_docs["ids"]) == 0:
#         vector_store.add_documents(docs)
#         print("✅ Added documents to vector store.")
#     else:
#         print("ℹ️ Vector store already has documents. Skipping addition.")
#
#     return vector_store.as_retriever()
#
#
# def build_qa_chain(retriever):
#     parser = StrOutputParser()
#     model = ChatGroq(api_key=GROQ_API_KEY, model="llama3-8b-8192", temperature=0.4, max_retries=2)
#     llm = model | parser
#
#     qa_chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         retriever=retriever,
#         return_source_documents=True,
#     )
#     return qa_chain
#
#
# def build_llm(qa_chain, workflow):
#     trimmer = trim_messages(
#         max_tokens=1500,  # Adjust based on your model's context window
#         strategy="last",
#         token_counter=count_tokens_approximately,
#         include_system=True,
#         allow_partial=False,
#         start_on="human",
#     )
#
#     def call_model(state: MessagesState):
#         # Trim the full message history to fit context window
#         trimmed_messages = trimmer.invoke(state["messages"])
#
#         # Extract the latest human message content as query string
#         temp_query = [msg.content for msg in trimmed_messages if msg.type == "human"][-1]
#
#         # Query the RetrievalQA chain with the latest user message string
#         response = qa_chain.invoke(temp_query)
#
#         # Append the AI response to the trimmed messages
#         updated_messages = trimmed_messages + [AIMessage(content=response["result"])]
#
#         # Return updated messages to update the state (memory)
#         return {"messages": updated_messages}
#
#     workflow.add_edge(START, "model")
#     workflow.add_node("model", call_model)
#
#     memory = MemorySaver()
#     app = workflow.compile(checkpointer=memory)
#     return app
#
#
# def run_custom_llm(user_id, user_query, app):
#     config = {"configurable": {"thread_id": user_id}}
#
#     # Retrieve existing messages from state or start empty
#     try:
#         state = app.get_state(config).values
#         current_messages = state.get("messages", [])
#     except Exception:
#         current_messages = []
#
#     # Append new user message to existing messages
#     new_messages = current_messages + [HumanMessage(content=user_query)]
#
#     # Invoke the app with the full updated message history
#     response = app.invoke({"messages": new_messages}, config=config)
#
#     # Print the AI's latest response
#     print(response["messages"][-1].content, end="", flush=True)
#
#     # Optionally, print the full current message history
#     state = app.get_state(config).values
#     print("\nPrinting current message history....")
#     for message in state["messages"]:
#         message.pretty_print()
#
#
# if __name__ == "__main__":
#     v_retriever = vector_store_retriever("documents/PHP Developer.pdf")
#     qa_chain = build_qa_chain(v_retriever)
#     workflow = StateGraph(state_schema=MessagesState)
#     app = build_llm(qa_chain, workflow)
#
#     query = ""
#     while "stop" not in query.lower():
#         query = input("Please enter a prompt: ")
#         if "stop" in query.lower():
#             break
#         run_custom_llm("abc1234", query, app)
#         print("\n\n")
