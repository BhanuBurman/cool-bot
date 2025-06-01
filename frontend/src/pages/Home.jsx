import { IoArrowForwardCircleSharp } from "react-icons/io5";
import axios from "axios";
import { useState } from "react";
import ReactMarkDown from "react-markdown";
import remarkGfm from "remark-gfm";

const Home = () => {
  const [query, setQuery] = useState("");
  const [responseList, setResponseList] = useState([]);
  const [info, setInfo] = useState("");
  const [loading, setLoading] = useState(false);
  const [isChatStart, setIsChatStart] = useState(false);

  const handleSubmit = async () => {
    setIsChatStart(true);
    try {
      const response = await fetch("http://localhost:8000/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });
      const data = await response.json();
      console.log(data.response);
      const userMessage = {
        role: "user",
        content: query,
      };
      const aiMessage = {
        role: "assistant",
        content: data.response,
      };
      setResponseList([...responseList, userMessage, aiMessage]);
      setQuery("");
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 px-30 py-20">
      <div className="output_window w-full mb-10">
        {isChatStart ? (
          <div className="chat_window">
            {responseList.map((message, index) => (
              <div className={`flex flex-row items-center my-2 ${message.role === "user"? "justify-end":"justify-start"}`} key={index}>
                {message.role === "user" ? (
                  <span className="user_profile w-15 h-15 rounded-full bg-violet-800 text-white font-bold flex items-center justify-center mr-2 text-3xl">
                    B
                  </span>
                ) : (
                  <span className="ai_profile user_profile w-15 h-15 rounded-full bg-green-700 text-white font-bold flex items-center justify-center mr-2 text-3xl">
                    AI
                  </span>
                )}
                <div
                  key={index}
                  className={`p-4 my-2 rounded-lg w-fit ${
                    message.role === "user"
                      ? "bg-blue-100 text-blue-800 self-end"
                      : "bg-green-100 text-green-800 self-start "
                  }`}
                >
                  <ReactMarkDown remarkPlugins={[remarkGfm]}>
                    {message.content}
                  </ReactMarkDown>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="default_content w-full flex justify-center">
            <h1 className="text-5xl font-semibold my-5">
              Welcome, How can I help you?
            </h1>
          </div>
        )}
      </div>
      <div className="user_input sticky bottom-15 w-full shadow-lg shadow-gray-400 bg-white p-4 rounded-lg flex items-center justify-between ">
        <textarea
          className="outline-none w-full mr-8 resize-none overflow-y-auto p-2 rounded"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          rows={1}
          placeholder="Ask me anything..."
          autoFocus
          style={{ maxHeight: "200px" }}
          onInput={(e) => {
            e.target.style.height = "auto"; // Reset the height
            e.target.style.height = e.target.scrollHeight + "px"; // Adjust to scroll height
          }}
        />
        <IoArrowForwardCircleSharp size={44} onClick={handleSubmit} />
      </div>
    </div>
  );
};

export default Home;
