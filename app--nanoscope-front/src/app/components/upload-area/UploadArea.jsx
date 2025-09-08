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
function ImageWithMask({ src }) {
  useEffect(() => {
    console.log("valor de src em image with mask", src);
  });
  return (
    <div className="w-full h-full min-h-full flex items-center justify-between bg-black/30 rounded-3xl p-4">
      <img
        src={src}
        alt="Imagem processada com máscara"
        className="object-cover rounded-3xl"
        draggable={false}
      />

      <div className="h-full w-1/2 flex flex-col items-start p-4">
        <span className="text-xl font-bold">Disease</span>
        <br />
        <span className="text-justify">
          The diagnostic is Lorem ipsum dolor sit amet, consectetur adipiscing
          elit. Suspendisse tortor sapien, pulvinar sed quam non, facilisis
          sollicitudin sapien. Pellentesque habitant morbi tristique senectus et
          netus et malesuada fames ac turpis egestas. Maecenas tellus nibh,
          sollicitudin vel justo quis, volutpat tempus quam. Suspendisse augue
          leo, commodo ut consequat sed, tristique id nisi. Morbi sit amet nibh
          vulputate, faucibus lacus tincidunt, sagittis nisi. Vestibulum ante
          ipsum primis in faucibus orci luctus et ultrices posuere cubilia
          curae; Vestibulum rhoncus, ante eget gravida iaculis, lorem risus
          sollicitudin eros, porttitor tempor neque lorem eu risus. Donec
          bibendum at justo id mollis. Nam eu congue mi. Pellentesque nibh
          ligula, dictum vitae ultricies vel, faucibus vitae purus. Mauris
          semper ut urna eget ornare. Curabitur ac mauris nisi. Ut nec quam id
          nisi ornare convallis. Nullam eu eleifend mi. Nam finibus molestie
          feugiat. Quisque tincidunt, turpis sed feugiat mattis, libero tellus
          posuere eros, sit amet vulputate nunc lectus ut libero. In hac
          habitasse platea dictumst. Suspendisse a facilisis odio. Pellentesque
          accumsan at ex vitae maximus. Maecenas tempus viverra dolor aliquet
          hendrerit. Vivamus auctor suscipit dui, vel cursus est congue in.
          Donec sollicitudin sapien justo, id lacinia est tincidunt at. Nam
          viverra vulputate nulla. Morbi tellus nunc, facilisis ac malesuada
          eget, dictum vel augue.
        </span>
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
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);

    return {
      processedImageUrl: url,
    };
  } catch (error) {
    console.error("Erro ao processar imagem:", error);
    throw error;
  }
}


export default function UploadArea() {
  const [status, setStatus] = useState("idle"); // idle | loading | done
  const [imageUrl, setImageUrl] = useState(null);
  const inputFileRef = useRef(null);

  async function onFileSelected(file) {
    if (!file) return;

    try {
      setStatus("loading");
      const response = await processFile(file);
      console.log("Imagem recebida: ", response.processedImageUrl);
      setImageUrl(response.processedImageUrl);
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
