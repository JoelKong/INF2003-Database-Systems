import React, {useState, useEffect} from 'react';
import AdminNavBar from "./AdminNavbar.tsx";
import {Link, useNavigate} from "react-router-dom";
import Loader from "../general/Loader.tsx";

interface User {
  user_id: number;
  username: string;
  role: string;
}

function AdminManageUsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const userSession: any = sessionStorage.getItem("user")
  const user = JSON.parse(userSession);

  const navigate = useNavigate();

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const user = JSON.parse(sessionStorage.getItem('user') || '{}');
      const response = await fetch('http://127.0.0.1:5000/api/v1/admin/getUsers', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({user_id: user.user_id}),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch users');
      }

      const data = await response.json();
      setUsers(data.users);
    } catch (err) {
      setError('Error fetching users');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleManageUser = (userId: number) => {
    navigate(`/admin/manage-user/${userId}`);
  };

  console.log(users)

  return (
    <>
      <AdminNavBar/>
      {loading && <Loader message="Fetching users..." />}

      <div className="container mx-auto mt-8">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-2xl font-bold">Manage Users</h1>
          <Link
            to="/admin/add-user"
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Add New User
          </Link>
        </div>

        {error && <p className="text-red-500">{error}</p>}
        {!loading && !error && (
          <table className="min-w-full bg-white border border-gray-300">
            <thead>
            <tr>
              <th className="py-2 px-4 border-b">User ID</th>
              <th className="py-2 px-4 border-b">Username</th>
              <th className="py-2 px-4 border-b">Role</th>
              <th className="py-2 px-4 border-b">Actions</th>
            </tr>
            </thead>
            <tbody>
            {users.map((user) => (
              <tr key={user.user_id}>
                <td className="py-2 px-4 border-b">{user.user_id}</td>
                <td className="py-2 px-4 border-b">{user.username}</td>
                <td className="py-2 px-4 border-b">{user.role}</td>
                <td className="py-2 px-4 border-b">
                  <button
                    onClick={() => handleManageUser(user.user_id)}
                    className="bg-green-500 hover:bg-green-700 text-white font-bold py-1 px-2 rounded"
                  >
                    Manage
                  </button>
                </td>
              </tr>
            ))}
            </tbody>
          </table>
        )}
      </div>
    </>
  );
}

export default AdminManageUsersPage;