import logo from '../logo.svg';
import '../App.css'
import React, { useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

// Import pages
import About from '../pages/About';
import DriverLogin from '../components/DriverLogin';
import DriverAbout from '../pages/DriverAbout';
import DriverMap from '../components/DriverMap';
import ProviderLogin from '../components/ProviderLogin';
import ProviderAbout from '../pages/ProviderAbout';
import ProviderUpdate from '../components/ProviderUpdate';

function App() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isLoggedIn, setIsLoggedIn] = useState(false);
  
    const handleLogout = () =>{
      setIsLoggedIn(false);
      setUsername('');
      setPassword('');
    };
    
    const handleLogin = async () => {
      try {
        await axios.post('/api/driver/login', { user_type: 'driver', username, password });
        navigate('/drivermap');
      } catch {
        alert('Login failed');
      }
    };
  
    return (
  
        <div className="App">
          <header className="App-header">
            {!isLoggedIn ? (
              <div>
                <h2>Login Page</h2>
                <form onSubmit={handleLogin}>
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
            ) : (
              <div>
                <h2>Welcome, {username}!</h2>
                <button onClick={handleLogout}>Logout</button>
              </div>
            )}
          </header>
        </div>
  
      );
  }
  export default App;