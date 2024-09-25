import { Link, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { BsCartFill } from "react-icons/bs";

export default function NavBar(): JSX.Element {
  const navigate = useNavigate();
  const [adopterName, setAdopterName] = useState<string | null>(null);
  const [role, setRole] = useState("");

  useEffect(() => {
    const user = sessionStorage.getItem("user");
    if (user) {
      const parsedUser = JSON.parse(user);
      setAdopterName(parsedUser.name);
      setRole(parsedUser.role);
    }
  }, []);

  const handleLogout = async () => {
    sessionStorage.removeItem("user");
    setAdopterName(null);
    navigate("/login");
  };

  return (
    <nav className="w-full bg-white shadow-lg">
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
            <Link
              to={"/favourites"}
              className="text-gray-700 hover:text-blue-500"
            >
              Favourites
            </Link>
            {role == "admin" && (
              <Link to={"/admin"} className="text-gray-700 hover:text-blue-500">
                Admin Dashboard
              </Link>
            )}
          </div>

          <div>
            {adopterName ? (
              <div className="flex items-center space-x-4">
                <span className="text-gray-700">Welcome, {adopterName}!</span>
                <button
                  onClick={() => {
                    navigate("/cart");
                  }}
                >
                  <BsCartFill />
                </button>
                <button
                  className="bg-red-500 text-white px-4 py-2 rounded-lg transition ease-in-out hover:scale-110 hover:bg-red-600 duration-300"
                  onClick={() => handleLogout()}
                >
                  Logout
                </button>
              </div>
            ) : (
              <button
                className="bg-blue-500 text-white px-4 py-2 rounded-lg transition ease-in-out hover:scale-110 hover:bg-indigo-500 duration-300"
                onClick={() => {
                  navigate("/login");
                }}
              >
                Login
              </button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
