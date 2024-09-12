import { Link } from "react-router-dom";

export default function NavBar(): JSX.Element {
  return (
    <nav className="bg-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link className="flex-shrink-0 h-28 w-28" to={"/"}>
            <img src={"/doglogo.png"} alt="Company Logo" />
          </Link>

          <div className="md:flex space-x-10">
            <Link to={"/"} className="text-gray-700 hover:text-blue-500">
              Home
            </Link>
            <Link to={"/"} className="text-gray-700 hover:text-blue-500">
              About
            </Link>
            <Link to={"/"} className="text-gray-700 hover:text-blue-500">
              Services
            </Link>
            <Link to={"/"} className="text-gray-700 hover:text-blue-500">
              Contact
            </Link>
          </div>

          <div>
            <button className="bg-blue-500 text-white px-4 py-2 rounded-lg transition ease-in-out hover:scale-110 hover:bg-indigo-500 duration-300">
              Login
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}
