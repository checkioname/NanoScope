"use client";

import { Josefin_Sans } from "next/font/google";
import { useRef, useState } from "react";

const josefin = Josefin_Sans({
  weight: "600",
  subsets: ["latin"],
});

export default function UploadSVG() {
  const inputFileRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);
  
  function handleClick() {
    if (inputFileRef.current) {
      inputFileRef.current.click();
    }
  }

  function handleFileChange(event) {
    const file = event.target.files[0];
    if (file) {
      alert(`Selected file: ${file.name}`);
      // Aqui você pode fazer o upload, enviar para backend, etc.
    }
  }

  function handleDrop(event) {
    event.preventDefault();
    setIsDragging(false);

    const files = event.dataTransfer.files;
    if (files.length) {
      alert(`Dragged file: ${files[0].name}`);
      // Aqui você pode enviar o arquivo para sua API
    }
  }

  function handleDragOver(event) {
    event.preventDefault();
    if (!isDragging) setIsDragging(true);
  }

  function handleDragLeave(event) {
    event.preventDefault();
    setIsDragging(false);
  }

  return (
    <>
      <svg
        width="100%"
        height="100%"
        viewBox="0 0 260 90"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        preserveAspectRatio="none"
        className="font-sans"
        style={{ fontFamily: "'Lato', sans-serif" }}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={handleClick}
      >
        <text
          x="50%" // posição horizontal central
          y="40%" // posição vertical central
          dominantBaseline="middle" // alinhamento vertical central
          textAnchor="middle" // alinhamento horizontal central
          fill="#E9E9E9"
          fontSize="2"
          fontFamily="'Lato', sans-serif"
        >
          Upload image
        </text>{" "}
        <text
          x="50%" // posição horizontal central
          y="43%" // posição vertical central
          dominantBaseline="middle" // alinhamento vertical central
          textAnchor="middle" // alinhamento horizontal central
          fill="#E9E9E9"
          fontSize="2"
          fontFamily="'Lato', sans-serif"
        >
          or Drag and drop
        </text>
        <text
          x="50%" // posição horizontal central
          y="46%" // posição vertical central
          dominantBaseline="middle" // alinhamento vertical central
          textAnchor="middle" // alinhamento horizontal central
          fill="#E9E9E9"
          fontSize="2"
          className={josefin.className}
        >
          Allowed formats are: jpeg, png, jpg
        </text>
        <rect
          x="9"
          y="5"
          width="240"
          height="80"
          rx="4"
          fill="#215651"
          fillOpacity="0.5"
          stroke="#05675F"
          strokeWidth="0.4"
          strokeDasharray="1.8 1" // camelCase
        />
      </svg>
      <input
        type="file"
        accept="image/*"
        ref={inputFileRef}
        style={{ display: "none" }}
        onChange={handleFileChange}
      />
    </>
  );
}
