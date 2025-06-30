// components/Navbar.jsx
import { Search, Bell } from 'lucide-react';  

export default function Navbar() {
  return (
    <nav className="flex items-center justify-between bg-gray-800 px-6 py-3 rounded-xl shadow-md">
      <div className="flex items-center space-x-6">
        <div className="text-xl font-bold text-orange-400/90">NanoScope</div>
        <button className="px-3 py-1 rounded-md bg-gray-800 text-gray-300 hover:bg-blue-700 hover:text-white">X-rays</button>
        <button className="text-gray-400 hover:text-white">My Appointments</button>
        <button className="text-gray-400 hover:text-white">Help</button>
        <button className="text-gray-400 hover:text-white">Contact</button>
      </div>
      <div className="flex items-center space-x-4">
        <button className="p-1 rounded-md hover:bg-gray-800"><Search size={20} /></button>
        <button className="p-1 rounded-md hover:bg-gray-800"><Bell size={20} /></button>    
      </div>
    </nav>
  );
}