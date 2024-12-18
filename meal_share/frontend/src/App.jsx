import logo from './logo.svg';
import './App.css'
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

// Import pages
import About from './pages/About';
import DriverAbout from './pages/DriverAbout';
import DriverMap from './components/DriverMap';
import BusinessAbout from './pages/BusinessAbout';
import ProviderUpdate from './components/ProviderUpdate';
import Home from './pages/Home';
import DriverLogin from './pages/DriverLogin';
import DriverSignUp from './pages/DriverSignUp';
import BusinessSignUp from './pages/BusinessSignUp';
import BusinessLogin from './pages/BusinessLogin';

function App() {
  return (
    <Router>
      <Routes>
      <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/driverlogin" element={<DriverLogin />} />
        <Route path="/driversignup" element={<DriverSignUp />} />
        <Route path="/businesssignup" element={<BusinessSignUp />} />
        <Route path="/businesslogin" element={<BusinessLogin />} />
        <Route path="/drivermap" element={<DriverMap />} />
        <Route path="/providerupdate" element={<ProviderUpdate />} />
        <Route path="/driverabout" element={<DriverAbout />} />
        <Route path="/bussinessabout" element={<BusinessAbout />} />
      </Routes>
    </Router>
  );
}

export default App;