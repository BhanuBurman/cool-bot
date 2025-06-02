import React from "react";

const LoadingUpload = ({infoType = "Loading..."}) => {
  return (
    <div className="loading_window absolute top-0 left-0 h-screen w-full z-10 bg-black/35 flex items-center justify-center">
      <div className="loading_box h-[50%] w-[50%] bg-white flex flex-col justify-center items-center rounded-2xl text-3xl transition-all duration-300 shadow-lg shadow-gray-500">
        <span className="animate-spin w-10 h-10 border-4 border-t-transparent mb-3 rounded-full"></span>
        <span>{infoType}</span>
      </div>
    </div>
  );
};

export default LoadingUpload;