import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function AdminPage() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const user = sessionStorage.getItem('user');

    if (user) {
      setUser(JSON.parse(user));
    } else {
      navigate('/admin/login');
    }
  }, [navigate]);

  const handleLogout = () => {
    sessionStorage.removeItem('user');
    navigate('/admin/login');
  };

  if (!user) return null;

  return (
    <div className="admin-page">
      <h1>Welcome, {user.username}!</h1>
      <p>Admin ID: {user.admin_id}</p>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}

export default AdminPage;