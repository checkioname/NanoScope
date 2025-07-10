"use client";

import { useRef, useState } from "react";
import UploadSVG from "../components/upload-svg/upload";
import { motion, AnimatePresence } from "framer-motion";
import ButtonDialog from "../components/button-dialog/button";

export default function Demo() {
  const inputFileRef = useRef(null);
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [diagnostico, setDiagnostico] = useState("");
  const [isExpanded, setIsExpanded] = useState(false);

  function handleFileSelect(selectedFile) {
    if (!selectedFile) return;

    const reader = new FileReader();
    reader.onload = () => {
      setFile(reader.result);
      setDiagnostico("Diagnóstico simulado: Resultado positivo."); // Ajuste conforme backend/real
      setIsExpanded(false);
    };
    reader.readAsDataURL(selectedFile);
  }
  
  function handleRun() {
    alert("Run executado!");
  }

  return (
    <div className="min-h-screen bg-[#1E9A99]/10 flex justify-between ">
      <div className="w-full bg-[#1E9A99]/20  p-10 flex flex-col">
        <div className="">
          <UploadSVG
            onFileSelect={handleFileSelect}
            isDragging={isDragging}
            setIsDragging={setIsDragging}
            shrink={!!file} // reduz quando o arquivo está carregado
          />
          <input
            type="file"
            accept="image/*"
            ref={inputFileRef}
            style={{ display: "none" }}
            onChange={(e) => handleFileSelect(e.target.files[0])}
          />
        </div>

        {file && (
          <AnimatePresence>
            {file && (
              <motion.img
                key="uploaded-image"
                src={file}
                alt="Imagem carregada"
                draggable={false}
                initial={{ opacity: 0, scale: 0.9 }} // estado inicial da animação (invisível e menor)
                animate={{ opacity: 1, scale: 1 }} // estado quando animado (visível e tamanho normal)
                exit={{ opacity: 0, scale: 0.9 }} // animação de saída (sumir)
                transition={{ duration: 0.8, ease: "easeInOut" }} // tempo e easing da animação
                className="w-1/2 h-5/6 object-fill rounded-lg"
              />
            )}
          </AnimatePresence>
        )}
        <div className="h-full flex justify-end items-end">
          {!file && <ButtonDialog onRun={handleRun} />}
        </div>
      </div>
    </div>
  );
}
