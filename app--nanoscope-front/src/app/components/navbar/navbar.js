// components/Navbar.jsx
import { Search, Bell } from 'lucide-react';  

export default function Navbar() {
  return (
    <nav className="flex items-center justify-between bg-gray-800 px-6 rounded-full shadow-md border border-gray-700">
      <div className="flex items-center space-x-6">
        <div className="text-xl font-bold text-orange-400/90">NanoScope</div>
        <button className="p-4 m-0 rounded-full bg-gray-800 text-gray-300 hover:bg-gray-700 hover:text-white">Diagnosis</button>
        <button className="p-4 m-0 text-gray-400 rounded-full hover:bg-gray-700 hover:text-white">Help</button>
        <button className="p-4 m-0 text-gray-400 rounded-full hover:bg-gray-700 hover:text-white">My Appointments</button>
        <button className="p-4 m-0 text-gray-400 rounded-full hover:bg-gray-700 hover:text-white">Contact</button>
      </div>
      <div className="flex items-center space-x-4">
        <button className="p-1 rounded-md hover:bg-gray-800"><Search size={20} /></button>
        <button className="p-1 rounded-md hover:bg-gray-800"><Bell size={20} /></button>    
      </div>
    </nav>
  );
}

