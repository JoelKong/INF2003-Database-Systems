import React, {useState, useEffect} from 'react';
import {useParams, useNavigate} from 'react-router-dom';
import AdminNavBar from "./AdminNavbar.tsx";
import Loader from "../general/Loader.tsx";

interface User {
    user_id: number;
    username: string;
    role: string;
}

function AdminManageUserPage() {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [updateMessage, setUpdateMessage] = useState<string | null>(null);

    const {user_id} = useParams<{ user_id: string }>();

    useEffect(() => {
        fetchUserDetails();
    }, [user_id]);

    const fetchUserDetails = async () => {
        try {
            const user = JSON.parse(sessionStorage.getItem('user') || '{}');
            const response = await fetch(`http://127.0.0.1:5000/api/v1/admin/getUser/${user_id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({admin_id: user.user_id}),
            });

            if (!response.ok) {
                throw new Error('Failed to fetch user details');
            }

            const data = await response.json();
            setUser(data.user);
        } catch (err) {
            setError('Error fetching user details');
            console.error('Error:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleUpdateUser = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setUpdateMessage(null);

        if (!user) return;

        try {
            const adminUser = JSON.parse(sessionStorage.getItem('user') || '{}');
            const response = await fetch(`http://127.0.0.1:5000/api/v1/admin/updateUser/${user_id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    admin_id: adminUser.user_id,
                    username: user.username,
                    role: user.role,
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to update user');
            }

            setUpdateMessage('User updated successfully');
        } catch (err) {
            setError('Error updating user');
            console.error('Error:', err);
        }
    };

    const handleDeleteUser = async () => {
        if (window.confirm('Are you sure you want to delete this user?')) {
            try {
                const adminUser = JSON.parse(sessionStorage.getItem('user') || '{}');
                const response = await fetch(`http://127.0.0.1:5000/api/v1/admin/deleteUser/${user_id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        admin_id: adminUser.user_id,
                    }),
                });
                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.error || 'Failed to delete user');
                }

                setUpdateMessage('User deleted successfully');
                na
            } catch (err) {
                setError('Error deleting user');
                console.error('Error:', err);
            }
        }
    };

    if (error) return <p className="text-red-500">{error}</p>;
    if (loading) return <Loader message="Fetching user..."/>

    return (
        <>
            <AdminNavBar/>

            <div className="container mx-auto mt-8">
                <h1 className="text-2xl font-bold mb-4">Manage User: {user.username}</h1>
                {updateMessage && <p className="text-green-500 mb-4">{updateMessage}</p>}
                {error && <p className="text-red-500 mb-4">{error}</p>}
                <form onSubmit={handleUpdateUser} className="max-w-md">
                    <div className="mb-4">
                        <label htmlFor="username" className="block mb-2">Username:</label>
                        <input
                            type="text"
                            id="username"
                            value={user.username}
                            onChange={(e) => setUser({...user, username: e.target.value})}
                            className="w-full px-3 py-2 border rounded"
                        />
                    </div>
                    <div className="mb-4">
                        <label htmlFor="role" className="block mb-2">Role:</label>
                        <select
                            id="role"
                            value={user.role}
                            onChange={(e) => setUser({...user, role: e.target.value})}
                            className="w-full px-3 py-2 border rounded"
                        >
                            <option value="adopter">adopter</option>
                            <option value="admin">admin</option>
                        </select>
                    </div>
                    <div className="flex justify-between">
                        <button type="submit"
                                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                            Update User
                        </button>
                        <button
                            type="button"
                            onClick={handleDeleteUser}
                            className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
                        >
                            Delete User
                        </button>
                    </div>
                </form>
            </div>
        </>
    );
}

export default AdminManageUserPage;