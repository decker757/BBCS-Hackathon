import logo from './logo.svg';
import './App.css'
import React, { useState } from 'react';
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
  return (
    <Router>
      <Routes>
        <Route path="/" element={<About />} />
        <Route path="/driverlogin" element={<DriverLogin />} />
        <Route path="/providerlogin" element={<ProviderLogin />} />
        <Route path="/drivermap" element={<DriverMap />} />
        <Route path="/providerupdate" element={<ProviderUpdate />} />
        <Route path="/driverabout" element={<DriverAbout />} />
        <Route path="/providerabout" element={<ProviderAbout />} />
      </Routes>
    </Router>
  );
}

export default App;