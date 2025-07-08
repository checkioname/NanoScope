import Navbar from "../components/navbar/navbar";
import UgridComponent from "../components/upload-grid/ugrid";
import { Plus } from 'lucide-react';

export default function UploadPage() {
    return (
    <div className="bg-[#13223C] min-h-screen text-gray-300 flex items-end">      
        <div className="w-5/6 fixed top-10 right-50 left-50">
            <Navbar />
        </div>
      <main className="flex flex-col items-start p-8 max-w-5xl mx-auto w-full">
        <button className="text-white-400 mb-4 flex items-center space-x-2 hover:underline cursor-pointer">
          <svg className="w-8 h-6" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round"><path d="M15 18l-6-6 6-6"/></svg>
          <span>X-ray diagnosis</span>
        </button>

        <UgridComponent/>

        <a href="#" className="mt-4 text-blue-500 hover:underline">Learn more about x-rays</a>
      </main>
    </div>
    );
}