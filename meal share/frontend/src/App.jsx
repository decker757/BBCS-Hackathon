import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

// Import pages
import About from './pages/About';
import DriverLogin from './components/DriverLogin';
import DriverAbout from './pages/DriverAbout';
import DriverMap from './components/DriverMap';
import ProviderLogin from './components/ProviderLogin';
import ProviderAbout from './pages/ProviderAbout';
import ProviderUpdate from './components/ProviderUpdate';

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault(); //Prevents form from reloading
    if (username === 'admin' && password === '1234'){
      alert('Login Successful!');
      setIsLoggedIn(true);
    }else{
      alert('Invalid Username or Password');
    }
  };
  const handleLogout = () =>{
    setIsLoggedIn(false);
    setUsername('');
    setPassword('');
  };

  return (
    <Router>
    <div className="min-h-screen bg-green-50">
      <nav className="bg-green-600 text-white p-4">
        <div className="container mx-auto flex justify-between items-center">
          <Link to="/" className="text-2xl font-bold">MealShare</Link>
          <div>
            <Link to="/about" className="mx-2">About</Link>
            <Link to="/driverlogin" className="mx-2">Driver Portal</Link>
            <Link to="/providerlogin" className="mx-2">Provider Portal</Link>
          </div>
        </div>
      </nav>

      <div className="container mx-auto mt-8">
        <Routes>
          {/* Public Routes */}
          <Route path="/about" element={<About />} />
          
          {/* Driver Routes */}
          <Route path="/driverlogin" element={<DriverLogin />} />
          <Route path="/driverabout" element={<DriverAbout />} />
          <Route path="/drivermap" element={<DriverMap />} />
          
          {/* Provider Routes */}
          <Route path="/providerlogin" element={<ProviderLogin />} />
          <Route path="/providerabout" element={<ProviderAbout />} />
          <Route path="/providerupdate" element={<ProviderUpdate />} />
        </Routes>
      </div>

      <div className="App">
        <header className="App-header">
          {!isLoggedIn ? (
            <div>
              <h2>Login Page</h2>
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
          ) : (
            <div>
              <h2>Welcome, {username}!</h2>
              <button onClick={handleLogout}>Logout</button>
            </div>
          )}
        </header>
      </div>

      <footer className="bg-green-700 text-white p-4 mt-8 text-center">
        <p>© 2024 MealShare - Spreading Generosity, One Meal at a Time</p>
      </footer>
    </div>
  </Router>
);
}
export default App;
