"use client";

import { useRef, useState } from "react";
import { Josefin_Sans } from 'next/font/google';
import UploadSVG from "../components/upload-svg/upload";

const josefin = Josefin_Sans({
     weight: '600',
     subsets: ['latin'],
   });

export default function Demo() {
  return (
    <div className="min-h-screen bg-[#1E9A99]/10 flex justify-between ">
      <div className="w-full bg-[#1E9A99]/20  p-2 flex flex-col">
        <UploadSVG/>
        <div className="w-full flex justify-end">
          <div className="flex flex-col items-end justify-around p-2 mr-18">
            <button className="bg-transparent border rounded p-3 px-6 border-[#1E9A99] hover:bg-[#1E9A99] text-[#1E9A99] hover:text-black">
              <span>Run</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
