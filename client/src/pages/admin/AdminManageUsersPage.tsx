import React, {useEffect, useState} from 'react';
import {useNavigate} from "react-router-dom";
import AdminNavBar from "./AdminNavbar.tsx";
import Loader from "../general/Loader.tsx";

function AddUserModal({isOpen, onClose, onAddAdopter}) {
  const [newAdopter, setNewAdopter] = useState({name: '', password: ''});

  const handleSubmit = (e) => {
    e.preventDefault();
    onAddAdopter(newAdopter);
    setNewAdopter({name: '', password: ''});
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
      <div className="bg-white p-6 rounded-lg max-w-md w-full">
        <h2 className="text-xl font-bold mb-4">Add New Adopter</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block mb-2" htmlFor="name">Name:</label>
            <input
              id="name"
              type="text"
              placeholder="Name"
              value={newAdopter.name}
              onChange={(e) => setNewAdopter({...newAdopter, name: e.target.value})}
              required
              className="w-full p-2 border rounded"
            />
          </div>
          <div className="mb-4">
            <label className="block mb-2" htmlFor="password">Password:</label>
            <input
              id="password"
              type="password"
              placeholder="Password"
              value={newAdopter.password}
              onChange={(e) => setNewAdopter({...newAdopter, password: e.target.value})}
              required
              className="w-full p-2 border rounded"
            />
          </div>
          <div className="flex justify-end space-x-2">
            <button
              type="submit"
              className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded"
            >
              Add Adopter
            </button>
            <button
              onClick={onClose}
              className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function Modal({isOpen, onClose, adopter, onUpdateRole}) {
  if (!isOpen || !adopter) return null;

  const [newRole, setNewRole] = useState(adopter.role);

  const handleRoleChange = (e) => {
    setNewRole(e.target.value);
  };

  const handleSubmit = () => {
    onUpdateRole(adopter.adopter_id, newRole);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
      <div className="bg-white p-6 rounded-lg max-w-md w-full">
        <h2 className="text-xl font-bold mb-4">Adopter Details</h2>
        <p><strong>Name:</strong> {adopter.name}</p>
        <p><strong>ID:</strong> {adopter.adopter_id}</p>
        <div className="my-4">
          <label className="block mb-2">Role:</label>
          <select
            value={newRole}
            onChange={handleRoleChange}
            className="w-full p-2 border rounded"
          >
            <option value="adopter">Adopter</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        <div className="mt-4 flex justify-end space-x-2">
          <button
            onClick={handleSubmit}
            className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded"
          >
            Update Role
          </button>
          <button
            onClick={onClose}
            className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

function AdminManageUsersPage() {
  const [adopters, setAdopters] = useState([]);
  const [selectedAdopter, setSelectedAdopter] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);

  const [loading, setLoading] = useState(true);

  const navigate = useNavigate();

  const user = JSON.parse(sessionStorage.getItem("user"));

  async function getAdopters() {
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:5000/api/v1/admin/getAdopters", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({user}),
      });
      const data = await response.json();
      setAdopters(data.adopters);
    } catch (error) {
      console.error("Error fetching adopters:", error);
    } finally {
      setLoading(false);
    }
  }

  async function addAdopter(newAdopterData) {
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:5000/api/v1/admin/addAdopter", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({user, newAdopter: newAdopterData}),
      });
      if (response.ok) {
        await getAdopters();
        setIsAddModalOpen(false);
      } else {
        const data = await response.json();
        console.error("Error adding adopter:", data.error);
      }
    } catch (error) {
      console.error("Error adding adopter:", error);
    } finally {
      setLoading(false);
    }
  }

  async function updateAdopterRole(adopterId, newRole) {
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:5000/api/v1/admin/updateAdopterRole", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({user, adopterId, newRole}),
      });
      if (response.ok) {
        await getAdopters();
        setIsModalOpen(false);
      } else {
        const data = await response.json();
        console.error("Error updating role:", data.error);
      }
    } catch (error) {
      console.error("Error updating role:", error);
    } finally {
      setLoading(false);
    }
  }

  const handleManageUserButton = (adopter) => {
    setSelectedAdopter(adopter);
    setIsModalOpen(true);
  };

  useEffect(() => {
    const user = sessionStorage.getItem("user");
    if (user) {
      const parsedUser = JSON.parse(user);
      if (parsedUser.role !== "admin") {
        navigate("/")
      }
    }

    getAdopters()
  }, []);

  return (
    <>
      <AdminNavBar/>

      {loading && <Loader message="Fetching adopters..."/>}

      <main className="container mx-auto px-4 py-8">
        <div className="mb-4">
          <button
            onClick={() => setIsAddModalOpen(true)}
            className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded"
          >
            Add Adopter
          </button>
        </div>

        <br/>

        <div>
          <h2 className="text-2xl font-bold mb-4">List of Adopters</h2>
          <table className="min-w-full bg-white shadow-md rounded-lg overflow-hidden">
            <thead className="bg-gray-100">
            <tr>
              <th className="px-4 py-2 text-left text-gray-600 w-1/3">Name</th>
              <th className="px-4 py-2 text-left text-gray-600 w-1/3">Role</th>
              <th className="px-4 py-2 text-right text-gray-600 w-1/3">Actions</th>
            </tr>
            </thead>
            <tbody>
            {adopters.map(adopter => (
              <tr key={adopter.adopter_id} className="border-b hover:bg-gray-50">
                <td className="px-4 py-2">{adopter.name}</td>
                <td className="px-4 py-2">{adopter.role}</td>
                <td className="px-4 py-2">
                  <div className="flex justify-end">
                    <button
                      className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-1 px-3 rounded"
                      onClick={() => handleManageUserButton(adopter)}
                    >
                      Manage Adopter
                    </button>
                  </div>
                </td>
              </tr>
            ))}
            </tbody>
          </table>
        </div>
      </main>

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        adopter={selectedAdopter}
        onUpdateRole={updateAdopterRole}
      />

      <AddUserModal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        onAddAdopter={addAdopter}
      />
    </>
  )
}

export default AdminManageUsersPage;