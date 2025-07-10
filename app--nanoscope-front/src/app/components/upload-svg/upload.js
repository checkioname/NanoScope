"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Josefin_Sans } from "next/font/google";

const josefin = Josefin_Sans({
  weight: "600",
  subsets: ["latin"],
});

export default function UploadSVG({
  onFileSelect,
  onClick,
  isDragging,
  setIsDragging,
  shrink = false, // nova prop para controlar escala
}) {
  function handleDrop(event) {
    event.preventDefault();
    setIsDragging(false);
    const files = event.dataTransfer.files;
    if (files.length && onFileSelect) {
      onFileSelect(files[0]);
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
    <motion.div
      style={{ originX: 0 }}
      animate={{ scaleX: shrink ? 0.5 : 1 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      className="w-full h-full"
    >
      <svg
        width="100%"
        height="100%"
        viewBox="0 0 260 90"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        preserveAspectRatio="none"
        className={`font-sans transition-all duration-700 ease-in-out`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={onClick}
        style={{ cursor: "pointer" }}
      >
        <rect
          x="9"
          y="5"
          width="240"
          height="80"
          rx="4"
          fill="#215651"
          fillOpacity={isDragging ? 0.7 : 0.5}
          stroke="#05675F"
          strokeWidth={0.4}
          strokeDasharray="1.8 1"
          className="transition-all duration-300"
        />
        <text
          x="50%"
          y="40%"
          dominantBaseline="middle"
          textAnchor="middle"
          fill="#E9E9E9"
          fontSize="2"
          fontFamily="'Lato', sans-serif"
        >
          Upload image
        </text>
        <text
          x="50%"
          y="43%"
          dominantBaseline="middle"
          textAnchor="middle"
          fill="#E9E9E9"
          fontSize="2"
          fontFamily="'Lato', sans-serif"
        >
          or Drag and drop
        </text>
        <text
          x="50%"
          y="46%"
          dominantBaseline="middle"
          textAnchor="middle"
          fill="#E9E9E9"
          fontSize="2"
          className={josefin.className}
        >
          Allowed formats are: jpeg, png, jpg
        </text>
      </svg>
    </motion.div>
  );
}
