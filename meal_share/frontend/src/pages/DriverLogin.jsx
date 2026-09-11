import { apiFetch } from '../api';
import './DriverLogin.css';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';


function DriverLogin() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState(''); // For both success and error messages
  const [isError, setIsError] = useState(false); // Track if the message is an error
  const navigate = useNavigate();
  

  // Function to handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevents form from reloading

    setMessage(''); // Reset previous messages
    setIsError(false);

    try {
      // Send POST request to Flask backend
      const response = await apiFetch('/api/driver/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }), // Sending username and password
      });

      const result = await response.json(); // Parse the response JSON

      if (response.ok) {
        // If login successful
        navigate('/driverabout', { state: {username} });
        setMessage('Login successful!'); // Show success message
        setIsError(false);

      } else {
        // If login failed
        setMessage(result.message || 'Invalid credentials'); // Show error message
        setIsError(true);
      }
    } catch (error) {
      console.error('Error during login:', error);
      setMessage('An error occurred. Please try again later.');
      setIsError(true); // Mark it as an error
    }
  };


  return (
    <div className="login">
      <header className="login-header">
          <div>
            <h2>Login Page</h2>
            {/* Display success or error message */}
            {message && (
              <p role="alert" style={{ color: isError ? 'red' : 'green' }}>{message}</p>
            )}

            <form onSubmit={handleSubmit}>
              <div>
                <label htmlFor="driver-username">Username:</label>
                <input
                  id="driver-username" type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
              </div>
              <div>
                <label htmlFor="driver-password">Password:</label>
                <input
                  id="driver-password" type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              <button type="submit">Login</button>
            </form>
          </div>
      </header>
    </div>
  );
}
export default DriverLogin;
