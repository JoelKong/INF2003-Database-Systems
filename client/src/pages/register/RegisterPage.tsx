import NavBar from "../general/NavBar";
import {useNavigate} from "react-router-dom";
import {useState} from "react";

export default function RegisterPage(): JSX.Element {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleRegister(name, password);
  };

  async function handleRegister(name: string, password: string) {
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:5000/api/v1/register", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({name, password}),
        credentials: 'include'
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Register success: ", data);
      navigate("/login");
    } catch (error) {
      console.error("Register error:", error);
      alert("Register failed. Please check your details and try again.");
    } finally {
      setLoading(false);
    }
  }


  return (
    <div className="w-screen h-screen">
      <NavBar/>
      <div className="w-full h-[calc(100%-64px)] flex justify-center items-center">
        <div
          className="w-1/2 p-8 border-2 border-black rounded-lg bg-gradient-to-tr from-amber-600 to-orange-300 flex flex-col items-center">
          <h1 className="tracking-wide font-bold text-4xl text-gray-700 mb-6">
            Register
          </h1>
          <form className="w-full max-w-md mb-6" onSubmit={handleSubmit}>
            <input
              className="w-full mb-4 p-2 rounded"
              type="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Name"
              required
            />
            <input
              className="w-full mb-4 p-2 rounded"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              required
            />
            <button
              className="w-full bg-blue-500 text-white px-4 py-2 rounded-lg transition ease-in-out hover:bg-blue-600 duration-300"
              type="submit"
              disabled={loading}
            >
              {loading ? 'Registering...' : 'Register'}
            </button>
          </form>
        </div>
      </div>
      {loading && <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="text-white">Registering...</div>
      </div>}
    </div>
  );
}