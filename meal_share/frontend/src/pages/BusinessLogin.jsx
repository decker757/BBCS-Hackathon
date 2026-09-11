import './DriverLogin.css';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';

function BusinessLogin() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [isError, setIsError] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await api.post("/api/business/login", {
        username,
        password,
      });

      if (response.status === 200) {
        navigate("/businessabout", { state: { username }}); // Redirect to MealDonation page
      }
    } catch (error) {
      if (error.response) {
        // Backend returned an error
        setMessage(error.response.data.message || "Invalid credentials");
        setIsError(true);
      } else {
        setMessage("An error occurred. Please try again later.");
        setIsError(true);
      }
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
                <label htmlFor="business-username">Username:</label>
                <input
                  id="business-username" type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
              </div>
              <div>
                <label htmlFor="business-password">Password:</label>
                <input
                  id="business-password" type="password"
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
export default BusinessLogin;
