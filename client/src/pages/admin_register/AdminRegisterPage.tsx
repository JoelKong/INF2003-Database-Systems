import React, {useState} from "react";


function AdminRegisterPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (e: any) => {
    e.preventDefault();

    setMessage('');
    setError('');

    if (!username || !password) {
      setError('Username and password are required');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/api/v1/admin/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({username, password}),
      });

      const data = await response.json();
      setMessage(data.message);
      setUsername('');
      setPassword('');
    } catch (err) {
      setError(err.response?.data?.error || 'got error happen during registration');
    }
  };

  return (
    <div className="admin-register">
      <h2>Admin Registration</h2>
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
        <button type="submit">Register</button>
      </form>
      {message && <p className="success-message">{message}</p>}
      {error && <p className="error-message">{error}</p>}
    </div>
  )
}

export default AdminRegisterPage;