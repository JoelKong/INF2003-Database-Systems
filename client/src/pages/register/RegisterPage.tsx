/** @format */

import NavBar from "../general/NavBar";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import axios from "axios";

export default function RegisterPage(): JSX.Element {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/api/v1/register",
        { email, name, password },
        { withCredentials: true }
      );
      console.log("Register success: ", response.data);
      navigate("/login");
    } catch (error: any) {
      console.error(
        "Register error:",
        error.response ? error.response.data : error.message
      );
      alert("Register failed. Please check your details and try again.");
    }
  };

  return (
    <div className="w-screen h-screen">
      <NavBar />
      <div className="w-full h-[calc(100%-64px)] flex justify-center items-center">
        <div className="w-1/2 p-8 border-2 border-black rounded-lg bg-gradient-to-tr from-amber-600 to-orange-300 flex flex-col items-center">
          <h1 className="tracking-wide font-bold text-4xl text-gray-700 mb-6">
            Register
          </h1>
          <form className="w-full max-w-md mb-6" onSubmit={handleSubmit}>
            <input
              className="w-full mb-4 p-2 rounded"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Email"
              required
            />
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
            >
              Register
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
