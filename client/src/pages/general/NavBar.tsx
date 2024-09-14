/** @format */

import { Link, useNavigate } from "react-router-dom";

export default function NavBar(): JSX.Element {
  const navigate = useNavigate();

  return (
    <nav className="fixed w-full bg-white shadow-lg">
      <div className="mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link className="flex-shrink-0 h-28 w-28" to={"/"}>
            <img src={"/doglogo.png"} alt="Company Logo" />
          </Link>

          <div className="md:flex space-x-10">
            <Link to={"/"} className="text-gray-700 hover:text-blue-500">
              Home
            </Link>
            <Link
              to={"/listofpets"}
              className="text-gray-700 hover:text-blue-500"
            >
              List of Pets
            </Link>
          </div>

          <div>
            <button
              className="bg-blue-500 text-white px-4 py-2 rounded-lg transition ease-in-out hover:scale-110 hover:bg-indigo-500 duration-300"
              onClick={() => {
                navigate("/login");
              }}
            >
              Login
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}
