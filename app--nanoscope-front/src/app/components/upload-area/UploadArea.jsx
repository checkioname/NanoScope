import { useState, useRef, useEffect } from "react";
import UploadSVG from "../upload-svg/upload";

function LoaderOverlay() {
  return (
    <div className="absolute inset-0 flex items-center justify-center bg-black/30 rounded-lg">
      <div className="w-12 h-12 border-4 border-white border-t-transparent rounded-full animate-spin" />
    </div>
  );
}

// Componente pra mostrar a imagem processada
function ImageWithMask({ src, analysisData }) {
  const { globalMetrics, cellFeatures, totalCells } = analysisData || {};
  useEffect(() => {
    console.log("valor de src em image with mask", src);
  });
  return (
    <div className="w-full h-full min-h-full flex items-center justify-between bg-black/30 rounded-3xl p-4">
      <img
        src={src}
        alt="Imagem processada com máscara"
        className="object-cover rounded-3xl max-w-1/2"
        draggable={false}
      />

      <div className="h-full w-1/2 flex flex-col items-start p-4">
        <span className="text-xl font-bold">Análise celular</span>
        <br />

        <div className="text-justify space-y-2">
          <p><strong>Total de células detectadas:</strong> {totalCells || 0 }</p>

          {globalMetrics && (
            <>
              <p><strong>Células potencialmente malignas:</strong> {globalMetrics.potentially_malignant_cells}</p>
              <p><strong>Percentual de malignidade:</strong> {globalMetrics.malignancyPercentage}</p>
              <p><strong>Densidade celular (por mm2):</strong> {globalMetrics.cell_density_per_mm2}</p>
              <p><strong>Tamanho médio das células:</strong> {globalMetrics.mean_cell_size1}</p>
              <p><strong>Qualidade da imagem:</strong> {globalMetrics.image_quality_score}</p>
            </>
          )}

        </div>
      </div>
    </div>
  );
}

// async function fakeApiProcessFile(file) {
//   const url = "https://picsum.photos/id/237/500/500";
//   const response = await fetch(url, {
//     method: "GET",
//     redirect: "manual", // para pegar o redirecionamento
//   });

//   const imageUrl = response.headers.get("location") || url;
//   await new Promise((r) => setTimeout(r, 500));

//   return {
//     processedImageUrl: imageUrl,
//   };
// }

async function processFile(file) {
  try {
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch("http://localhost:3000/image", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      console.log(response)
      throw new Error("Erro ao processar imagem");
    }
    const data = await response.json();

    return {
      processedImageUrl: data.processedImage,
      cellFeatures: data.cellFeatures,
      globalMetrics: data.globalMetrics,
      totalCells: data.totalCells
    };
  } catch (error) {
    console.error("Erro ao processar imagem:", error);
    throw error;
  }
}


export default function UploadArea() {
  const [status, setStatus] = useState("idle"); // idle | loading | done
  const [imageUrl, setImageUrl] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const inputFileRef = useRef(null);

  async function onFileSelected(file) {
    if (!file) return;

    try {
      setStatus("loading");
      const response = await processFile(file);
      console.log("Imagem recebida: ", response.processedImage);
      setImageUrl(response.processedImage);
      setAnalysisData(response);
      console.log(imageUrl);
      setStatus("done");
    } catch (error) {
      console.error("Erro ao processar imagem:", error);
      setStatus("error");
    }
  }

  useEffect(() => {
    console.log("imageUrl atualizado:", imageUrl);
  }, [imageUrl]);

  function openFileDialog() {
    if (inputFileRef.current) inputFileRef.current.click();
  }

  return (
    <div className="relative w-full h-full rounded-lg">
      {(status === "idle" || status === "loading") && (
        <>
          <UploadSVG
            onFileSelect={onFileSelected}
            onClick={openFileDialog}
            shrink={status !== "idle"}
          />
          {status === "loading" && <LoaderOverlay />}
          <input
            type="file"
            accept="image/*"
            ref={inputFileRef}
            style={{ display: "none" }}
            onChange={(e) => onFileSelected(e.target.files[0])}
          />
        </>
      )}

      {status === "done" && <ImageWithMask src={imageUrl} />}
    </div>
  );
}
