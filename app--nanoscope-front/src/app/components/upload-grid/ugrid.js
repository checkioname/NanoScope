import { Plus } from 'lucide-react';

export default function UgridComponent() {
    return (
        <div className="w-full h-96 border-2 border-dashed border-blue-800 rounded-xl flex flex-col justify-center items-center">
          <p className="mb-2 text-center">
            Add an X-ray file<br />
            Allowed formats: DICOM, PDF, PNG, JPEG.
          </p>
          <button className="bg-blue-600 hover:bg-blue-800 transition px-6 py-2 rounded-full flex items-center space-x-2">
            <input className="" type="file" placeholder="123-45-678" accept="image/png, image/jpeg"></input>
            <Plus size={18} />
            <label for="file">Add file</label>
          </button>
        </div>
    )
}