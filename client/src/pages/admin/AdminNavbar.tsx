import { Link, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";

export default function AdminNavBar(): JSX.Element {
  const navigate = useNavigate();
  const [adopterName, setAdopterName] = useState<string | null>(null);

  useEffect(() => {
    const user = sessionStorage.getItem("user");
    if (user) {
      const parsedUser = JSON.parse(user);
      setAdopterName(parsedUser.username);
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
              Go Back
            </Link>
            <Link
              to={"/admin/managepets"}
              className="text-gray-700 hover:text-blue-500"
            >
              Manage Pets
            </Link>
            <Link
              to={"/admin/manage-users"}
              className="text-gray-700 hover:text-blue-500"
            >
              Manage Users
            </Link>
            <Link
              to={"/admin/applications"}
              className="text-gray-700 hover:text-blue-500"
            >
              Manage Applications
            </Link>
            <Link
              to={"/admin/manage-adoptions"}
              className="text-gray-700 hover:text-blue-500"
            >
              Manage Adoptions
            </Link>
          </div>

          {adopterName ? (
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">Welcome, {adopterName}!</span>
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
    </nav>
  );
}
