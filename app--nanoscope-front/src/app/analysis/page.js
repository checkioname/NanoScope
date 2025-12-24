import { ArrowLeft, ZoomIn, ZoomOut, Printer, Download } from 'lucide-react';
import Navbar from '../components/navbar/navbar';

export default function ResultsPage() {
  return (
    <div className="bg-[#0A1220] min-h-screen text-gray-300 flex items-end">
        <div className="w-5/6 fixed top-10 right-50 left-50">
            <Navbar />
        </div>
      <main className="flex flex-col max-w-7xl mx-auto p-8 bg-white/10 rounded-4xl mb-2">
        <button className="flex items-center text-gray-400 mb-6 hover:text-indigo-600 transition space-x-2"
        >
          <ArrowLeft size={20} />
          <span className="font-semibold text-xl">Diagnosis</span>
        </button>

        <div className="flex gap-8 flex-1">
          <section className="relative bg-gray-800 rounded-xl flex-shrink-0 w-[480px] h-[560px] shadow-lg flex flex-col items-center justify-center p-6">
            <img
              src="/images/xray-example.png"
              alt="X-ray"
              className="rounded-xl shadow-md object-contain max-h-full"
            />
            
            <div className="absolute bottom-6 right-6 flex flex-col space-y-3 bg-gray-900 bg-opacity-60 p-2 rounded-md">
              <button className="p-1 bg-gray-700 rounded-md hover:bg-indigo-600 transition" title="Zoom in">
                <ZoomIn size={20} />
              </button>
              <button className="p-1 bg-gray-700 rounded-md hover:bg-indigo-600 transition" title="Zoom out">
                <ZoomOut size={20} />
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-4 italic text-center">
              Hover over the image or description to read the diagnosis.
            </p>
          </section>

          
          <section className="flex flex-col flex-grow gap-6">
          
            <div className="bg-gray-800 rounded-xl p-5 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 shadow">
              <div className="flex items-center gap-4">
                <div className="bg-yellow-600 rounded-full p-2">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M12 9v2m0 4h.01M12 5a7 7 0 0 0-7 7h14a7 7 0 0 0-7-7z" />
                  </svg>
                </div>
                <div>
                  <p className="font-semibold text-lg text-yellow-400">Cardiologist</p>
                  <p className="text-sm text-yellow-300">
                    No immediate life threat. Diagnostics recommended
                  </p>
                  <p className="text-xs text-yellow-300 mt-1">
                    Reason: Chronic heart failure
                  </p>
                </div>
              </div>
              <button className="bg-indigo-600 hover:bg-indigo-700 text-white rounded-full px-5 py-2 shadow">
                Schedule an appointment
              </button>
            </div>

            
            <div className="bg-gray-800 rounded-xl p-6 shadow overflow-y-auto max-h-[420px]">
              <h2 className="text-xl font-semibold mb-4">Detailed diagnosis</h2>
              <DiagnosisItem 
                title="Lung Fields" 
                icon="danger" 
                points={[
                  "In the lower lung fields, bilaterally, patchy parenchymal consolidations are visible, which may suggest inflammatory changes (pneumonia).",
                  "There are small perihilar infiltrates, more pronounced on the right side."
                ]}
                highlights={[{text:"pneumonia", type:"danger"}, {text:"perihilar infiltrates", type:"info"}]}
              />

              <DiagnosisItem 
                title="Heart and Mediastinum" 
                icon="warning" 
                points={[
                  "The heart silhouette is enlarged, with a cardio-thoracic ratio of 0.55, indicating moderate cardiomegaly.",
                  "The contours of the aortic arch and pulmonary hila are somewhat widened, which may suggest signs of chronic heart failure or pulmonary hypertension."
                ]}
                highlights={[{text:"cardio-thoracic ratio", type:"link"}, {text:"chronic heart failure", type:"warning"}]}
              />

              <DiagnosisItem 
                title="Trachea and Bronchi"
                icon="warning"
                points={[
                  "The trachea is midline, not displaced.",
                  "Mild dilation of the main bronchi is visible, which may suggest chronic bronchitis or bronchiectasis."
                ]}
              />

              <DiagnosisItem 
                title="Bones"
                icon="success"
                points={[
                  "Visible bony structures (ribs, clavicles, thoracic spine) show no traumatic or destructive changes.",
                  "Mild degenerative changes in the thoracic spine."
                ]}
              />
            </div>

            
            <div className="flex justify-end gap-4 mt-6">
              <button className="flex items-center gap-2 bg-gray-700 hover:bg-gray-600 rounded-full px-5 py-2 transition">
                <Printer size={18} />
                Print diagnosis
              </button>
              <button className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 rounded-full px-5 py-2 text-white transition">
                <Download size={18} />
                Download diagnosis
              </button>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}

function DiagnosisItem({ title, icon, points, highlights = [] }) {
  // Ícones pequenos para status
  const icons = {
    danger: (
      <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round">
        <path d="M18 12H6" />
        <path d="M12 6v12" />
      </svg>
    ),
    warning: (
      <svg className="w-5 h-5 text-yellow-400" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 9v2" />
        <path d="M12 15h.01" />
        <path d="M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z" />
      </svg>
    ),
    success: (
      <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round">
        <path d="M5 13l4 4L19 7" />
      </svg>
    )
  };

  // Função para aplicar destaque no texto (substitui palavras-chave)
  const renderTextWithHighlights = (text) => {
    if (!highlights.length) return text;

    let parts = [text];
    highlights.forEach(({ text: hlText, type }) => {
      parts = parts.flatMap(part => {
        if (typeof part !== "string") return [part];

        const split = part.split(new RegExp(`(${hlText})`, "gi"));
        return split.map((segment, i) => 
          segment.toLowerCase() === hlText.toLowerCase() ? (
            <span key={`${hlText}-${i}`} className={`rounded px-1 text-sm
              ${type === "danger" ? "bg-red-700 text-red-300" : ""}
              ${type === "warning" ? "bg-yellow-700 text-yellow-300" : ""}
              ${type === "info" ? "bg-indigo-700 text-indigo-300" : ""}
              ${type === "link" ? "underline cursor-pointer text-indigo-400" : ""}
            `}>
              {segment}
            </span>
          ) : segment
        );
      });
    });
    return parts;
  };

  return (
    <div className="mb-6">
      <h3 className="flex items-center font-semibold text-lg mb-2 space-x-2 border-l-4 pl-3
        border-transparent">
        {title}
        {icons[icon] && icons[icon]}
      </h3>
      <ul className="list-disc list-inside space-y-1 text-sm leading-relaxed">
        {points.map((point, i) => (
          <li key={i}>{renderTextWithHighlights(point)}</li>
        ))}
      </ul>
    </div>
  );
}