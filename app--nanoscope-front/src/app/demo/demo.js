export default function Demo() {
  return (
    <div className="min-h-screen bg-[#1E9A99]/10 flex justify-between ">
      <div className="w-1/2 bg-[#1E9A99]/10  p-2 flex">
        {" "}
        {/* Defina altura e largura do container */}
        <svg
          width="100%"
          height="100%"
          viewBox="0 0 260 239"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          preserveAspectRatio="none" // Mantém proporção com centralização
        >
          <rect
            x="25"
            y="1"
            width="200"
            height="235"
            rx="12"
            fill="#215651"
            fillOpacity="0.28" // use camelCase no React
            stroke="#05675F"
            strokeDasharray="10 4" // camelCase
          />
        </svg>
      </div>
      <div className="w-1/2 flex flex-col items-center justify-around p-2">
        <form className="w-5/6 bg-transparent border   rounded-xl">
          <input
            className="border border-black m-6 rounded p-1 w-9/10"
            placeholder="Patient name"
          />
          <input
            className="border border-black m-6 mt-2 rounded p-1 w-9/10"
            placeholder="Patient name"
          />
          <input
            className="border border-black m-6 mt-2 rounded p-1 w-9/10"
            placeholder="Patient name"
          />
          <input
            className="border border-black m-6 mt-2 rounded p-1 w-9/10"
            placeholder="Patient name"
          />
          <input
            className="border border-black m-6 mt-2 rounded p-1 w-9/10"
            placeholder="Patient name"
          />
          <input
            className="border border-black m-6 mt-2 rounded p-1 w-9/10"
            placeholder="Patient name"
          />
        </form>
        <div className="w-5/6 flex justify-end">
          <button className="bg-transparent border rounded p-3 px-6 border-[#E9E9E9] hover:bg-white text-[#E9E9E9]">
            <span>Run</span>
          </button>
        </div>
      </div>
    </div>
  );
}
