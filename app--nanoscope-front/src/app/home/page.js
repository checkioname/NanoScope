import { Lato } from "next/font/google";
import Image from "next/image";
import About from "../components/about/about";

const latoFont = Lato({
  subsets: ["latin"],
  weight: "300",
});

export default function Home() {
  return (
    <>
      <div className="relative flex min-h-screen w-full bg-[#E9E9E9] text-black justify-between items-end p-10">
        <div className="text-7xl font-lato space-y-0">
          <p className="transition-transform duration-200 ease-in-out hover:scale-110">
            Self
          </p>
          <p className="transition-transform duration-200 ease-in-out hover:scale-110">
            Supervised
          </p>
          <p className="transition-transform duration-200 ease-in-out hover:scale-120">
            Learning<span className="text-[#0E9F93]">*</span>
          </p>
        </div>
        <div>
          {/* <button className="border rounded p-3 px-6 border-[#0E9F93] hover:bg-[#0E9F93]">
            <span className="text-[#0E9F93] hover:text-[#E9E9E9]">Demo</span>
          </button> */}
          <button className="bg-transparent border rounded p-3 px-6 border-[#0E9F93] hover:bg-white text-[#0E9F93]">
            Demo
          </button>
        </div>
        <div
          className={`absolute right-210 top-20 w-62 text-3xl font-lat ${latoFont.className}`}
        >
          <p>
            "We empower healthcare providers to faster, more accurate decisions,
            improving patient outcomes & lives"
          </p>
        </div>
        <div className="absolute right-0 top-0 max-w-full w-[42vw] h-[100vh] overflow-hidden">
          <Image
            // className="overflow-hidden"
            src="/159BG.png"
            alt="Background DNA"
            fill
            style={{
              objectFit: "contain",
              transform: "rotate(266deg) scale(1.2)",
              transformOrigin: "center",
            }}
            priority
          />
        </div>
      </div>
      <About/>
    </>
  );
}
