import logo from './logo.svg';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';
import Home from './webpages/Home';
import Login from './webpages/Login';
import DriverSignUp from './webpages/DriverSignUp';
import BusinessSignUp from './webpages/BusinessSignUp';
import About from './webpages/About';
import React, { useState } from 'react';

function App() {
  return (
    <BrowserRouter>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/driversignup" element={<DriverSignUp />} />
        <Route path="/businesssignup" element={<BusinessSignUp />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  );
}
export default App;
