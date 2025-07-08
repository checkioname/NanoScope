import { Lato } from "next/font/google";
import { ArrowRight } from "lucide-react";

const latoFont = Lato({
  subsets: ["latin"],
  weight: "300",
});

export default function About() {
  return (
    <div
      className={`flex flex-col items-center min-h-screen bg-white text-black ${latoFont.className}`}
    >
      <div className="w-full p-8 flex bg-[#1E9A99]/100 justify-between">
        <div>
          <h1 className="text-3xl">Medicine Meets AI:</h1>
          <h1 className="text-2xl">A Breakthrough in Healthcare</h1>
        </div>
        <button className="w-1/10 group relative border flex items-center justify-around px-4 py-2 overflow-hidden">
          <span className="transition-all duration-500 group-hover:pr-4">
            Contact us
          </span>
          <ArrowRight
            className="absolute right-5 opacity-0 translate-x-0 transition-all duration-700 ease-in-out 
      group-hover:opacity-100 group-hover:-rotate-45 group-hover:translate-x-4"
            style={{ top: "10%", transformOrigin: "center" }}
          />
        </button>
      </div>
      <div className="flex min-h-100 w-3/4 items-center justify-around">
        <div className="flex flex-col items-center w-60">
          <h1 className="bg-gray-200 p-2 px-10 rounded-full text-center w-60">
            Feature Engineering
          </h1>
          <p>
            Aprimore dados clínicos complexos para gerar insights decisivos.
          </p>
        </div>
        <div className="flex flex-col items-center w-60">
          <h1 className="bg-gray-200 p-2 px-1 rounded-full text-center w-60">
            Feature Engineering
          </h1>
          <p className="">
            A tecnologia que aprende com dados reais, crescente e precisa.
          </p>
        </div>
      </div>
      <div className="flex flex-col w-full h-full p-10">
        <span className="text-7xl text-[#1E9A99]/100">Predictive</span>
        <span className="text-7xl font-bold">Analysis</span>
      </div>
    </div>
  );
}
