import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function DriverLogin() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      await axios.post('/login', { user_type: 'driver', username, password });
      navigate('/drivermap');
    } catch {
      alert('Login failed');
    }
  };

  return (
    <div>
      <h2>Driver Login</h2>
      <input placeholder="Username" onChange={(e) => setUsername(e.target.value)} />
      <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}

export default DriverLogin;
