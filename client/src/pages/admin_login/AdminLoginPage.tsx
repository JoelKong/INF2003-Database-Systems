import React, {useState} from "react";
import {useNavigate} from "react-router-dom";

function AdminLoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const navigate = useNavigate();

  const handleSubmit = async (e: any) => {
    e.preventDefault();

    setMessage('');
    setError('');

    if (!username || !password) {
      setError('Username and password are required');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/api/v1/admin/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({username, password}),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(data.message);
        console.log(data);

        // store user data inside session storage
        sessionStorage.setItem('user', JSON.stringify({
          admin_id: data.user.admin_id,
          username: data.user.username
        }));

        setUsername("");
        setMessage("");

        navigate('/admin');
      } else {
        setError(data.error || 'Login failed');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'got error happen during login');
    }
  };

  return (
    <div className="admin-login">
      <h2>Admin Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
      {message && <p className="success-message">{message}</p>}
      {error && <p className="error-message">{error}</p>}
    </div>
  )
}

export default AdminLoginPage;