import './DriverLogin.css';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function BusinessLogin() {
   const [username, setUsername] = useState('');
   const [password, setPassword] = useState('');
   const [isLoggedIn, setIsLoggedIn] = useState(false);
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
       const response = await fetch('http://127.0.0.1:5000/api/business/login', {
         method: 'POST',
         headers: {
           'Content-Type': 'application/json',
         },
         body: JSON.stringify({ username, password }), // Sending username and password
       });
 
       const result = await response.json(); // Parse the response JSON
 
       if (response.ok) {
         // If login successful
         navigate('/businessabout', { state: {username} });
         setIsLoggedIn(true);
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
       setIsError(true);
     }
   };
 
   // Function to handle logout
   const handleLogout = () => {
     setIsLoggedIn(false);
     setUsername('');
     setPassword('');
     setMessage('');
     setIsError(false);
   };

  return (
    <div className="login">
      <header className="login-header">
          <div>
            <h2>Login Page</h2>
            {/* Display success or error message */}
              {message && (
              <p style={{ color: isError ? 'red' : 'green' }}>{message}</p>
            )}
            <form onSubmit={handleSubmit}>
              <div>
                <label>Username:</label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
              </div>
              <div>
                <label>Password:</label>
                <input
                  type="password"
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