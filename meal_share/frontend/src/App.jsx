import logo from './logo.svg';
import './App.css'
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

// Import pages
import About from './pages/About';
import DriverAbout from './pages/DriverAbout';
import DriverMap from './components/DriverMap';
import ProviderAbout from './pages/ProviderAbout';
import ProviderUpdate from './components/ProviderUpdate';
import Home from './pages/Home';
import Login from './pages/Login';
import DriverSignUp from './pages/DriverSignUp';
import BusinessSignUp from './pages/BusinessSignUp';

function App() {
  return (
    <Router>
      <Routes>
      <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/login" element={<Login />} />
        <Route path="/driversignup" element={<DriverSignUp />} />
        <Route path="/businesssignup" element={<BusinessSignUp />} />
        <Route path="/drivermap" element={<DriverMap />} />
        <Route path="/providerupdate" element={<ProviderUpdate />} />
        <Route path="/driverabout" element={<DriverAbout />} />
        <Route path="/providerabout" element={<ProviderAbout />} />
      </Routes>
    </Router>
  );
}

export default App;