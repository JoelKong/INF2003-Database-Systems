import { useNavigate } from "react-router-dom";

export default function Landing(): JSX.Element {
    const navigate = useNavigate()

  return (
    <div className="w-full h-full flex justify-center items-center">
      <div className="w-1/2 h-1/2 border-2 border-black rounded-lg bg-gradient-to-tr from-amber-600 to-orange-300 flex justify-center items-center flex-col">
        <h1 className="tracking-wide font-bold text-4xl text-gray-700 mb-6">
          Adopt A Pet Today!
        </h1>
        <button className="bg-blue-500 text-white px-4 py-2 rounded-lg transition ease-in-out hover:scale-110 hover:bg-indigo-500 duration-300" onClick={() => navigate("/listofpets")}>
          Adopt Now
        </button>
      </div>
    </div>
  );
}
