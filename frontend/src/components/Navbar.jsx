import Logo from "../assets/logo.png";
import { CiCirclePlus } from "react-icons/ci";
import { GrDocument } from "react-icons/gr";
import LoadingUpload from "./LoadingUpload";
import { useEffect, useState } from "react";
import { RiArrowDropDownLine } from "react-icons/ri";

const Navbar = () => {
  const [isUploading, setIsUploading] = useState(false);
  const [fileName, setFileName] = useState("No file");
  const [infoType, setInfoType] = useState("Loading...");
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [fileList, setFileList] = useState([]);

  useEffect(() => {
    fetchAllFiles();
  }, []);

  const fetchAllFiles = async () => {
    try {
      const response = await fetch("http://localhost:8000/get-all-files");
      if (!response.ok) {
        throw new Error("Failed to fetch files");
      }
      const data = await response.json();
      setFileList(data);
      console.log("Fetched files:", data);
    } catch (error) {
      console.error("Error fetching files:", error);
    }
  };

  const handleFileEmbedding = async (fileName) => {
    if (fileName === "No file") {
      return;
    }
    try {
      setIsUploading(true);
      setInfoType("Embedding file...");
      const response = await fetch("http://localhost:8000/embed_file/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ file_name: fileName }),
      });
      if (!response.ok) {
        throw new Error("Error embedding file");
      }

      const data = await response.json();
      setInfoType("File embedded successfully");
      console.log("Embedding response:", data);
    } catch (error) {
      console.error("Error embedding file:", error);
      setInfoType("Error embedding file");
    } finally {
      setTimeout(() => {
        setIsUploading(false);
      }, 2000);
    }
  };

  const handleUpload = async (event) => {
    const file = event.target.files[0];

    if (!file || file.type !== "application/pdf") {
      alert("Please upload a valid PDF file.");
      return;
    }

    setIsUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      // Step 1: Upload the file
      const uploadResponse = await fetch("http://localhost:8000/upload/", {
        method: "POST",
        body: formData,
      });

      if (!uploadResponse.ok) {
        throw new Error("File upload failed");
      }

      setInfoType("Started Embedding Process...!");

      // Step 2: Process the file
      const processResponse = await fetch("http://localhost:8000/embed_file/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ file_name: file.name }),
      });
      if (!processResponse.ok) {
        throw new Error("Error processing file");
      }

      setInfoType("Uploading file information...");

      // Step 3: Get upload info
      const infoResponse = await fetch("http://localhost:8000/upload_info/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ file_name: file.name }),
      });

      if (!infoResponse.ok) {
        throw new Error("Error fetching uploaded file info");
      }

      const infoData = await infoResponse.json();
      setFileName(infoData.file_name || "Unknown");
      setTimeout(() => {
        setInfoType("File uploaded and processed successfully!");
      }, 2000);
    } catch (error) {
      console.error("Upload Error:", error);
      alert(error.message);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="navbar absolute top-0 left-0 w-full px-5 md:px-10 h-16 flex items-center justify-center shadow-md bg-white">
      {isUploading && <LoadingUpload infoType={infoType} />}
      <ul className="flex items-center justify-between w-full">
        <li>
          <img src={Logo} className="h-7 md:h-14" />
        </li>
        <div className="flex items-center">
          <div className="flex justify-center items-center">
            <div
              onClick={() => setDropdownOpen(!dropdownOpen)}
              className="mx-2 text-nowrap md:mx-5 flex items-center gap-2 w-50 p-1 px-5 rounded-md hover:bg-gray-100 font-semibold cursor-pointer"
            >
              <GrDocument className="text-2xl h-7 text-green-500 border-1 p-1 rounded-sm border-green-400" />
              <span className="text-green-500">
                {fileName.substring(0, 13) +
                  (fileName.length > 13 ? "..." : "")}
              </span>
              <RiArrowDropDownLine className="text-3xl text-green-600"/>
            </div>
            {dropdownOpen && (
              <div className="drop_down absolute w-50 flex flex-col rounded-bl-md rounded-br-md shadow-md  bg-gray-100 py-2  top-12 z-10">
                {fileList.length > 0 &&
                  fileList.map((file, index) => (
                    <span
                      key={index}
                      onClick={() => {
                        setFileName(file.file_name);
                        handleFileEmbedding(file.file_name);
                        setDropdownOpen(false);
                      }}
                      className="text-gray-700 hover:text-gray-900 cursor-pointer border-b-2 border-gray-300 p-2"
                    >
                      {file.file_name.substring(0, 20) +
                        (file.file_name.length > 20 ? "..." : "")}
                    </span>
                  ))}
              </div>
            )}
          </div>
          <label
            type="file"
            className="border-2 p-1 px-1 md:px-5 rounded-md flex items-center justify-center gap-2 hover:bg-gray-100 transition-all duration-300 cursor-pointer font-semibold hover:-mt-1"
          >
            <input
              type="file"
              accept=".pdf"
              className="hidden"
              onChange={handleUpload}
            />
            <CiCirclePlus />
            <span className="hidden lg:inline">Upload PDF</span>
          </label>
        </div>
      </ul>
    </div>
  );
};

export default Navbar;
