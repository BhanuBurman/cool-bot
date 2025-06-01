import Logo from '../assets/logo.png';
import { CiCirclePlus } from "react-icons/ci";
import { GrDocument } from "react-icons/gr";
const Navbar = () => {

  const handleUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.type === "application/pdf") {
      const formData = new FormData();
      formData.append("file", file);
      
      fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      })
      .then(response => response.json())
      .then(data => {
        console.log("File uploaded successfully:", data);
      })
      .catch(error => {
        console.error("Error uploading file:", error);
      });
    } else {
      alert("Please upload a valid PDF file.");
    }
  }
  return (
    <div className="navbar absolute top-0 left-0 w-full px-10 h-16 flex items-center justify-center shadow-md bg-white">
      <ul className="flex items-center justify-between w-full">
        <li>
            <img src={Logo} className='h-14' />
        </li>
        <div className='flex items-center'>
        <div className='mx-5 flex items-center gap-2 p-1 px-5 rounded-md hover:bg-gray-100 font-semibold'>
          <GrDocument className='text-2xl h-7 text-green-500 border-1 p-1 rounded-sm border-green-400' />
          <span className='text-green-500'>
            curr.pdf
            </span>
        </div>
        <button type='file' className='border-2 p-1 px-5 rounded-md flex items-center justify-center gap-2 hover:bg-gray-100 transition-all duration-300 cursor-pointer font-semibold'>
          <input type="file" accept=".pdf" className="hidden" onChange={handleUpload} />
          <CiCirclePlus />
            <span>
              Upload PDF
              </span>
        </button>
        </div>
      </ul>
    </div>
  );
};

export default Navbar;
