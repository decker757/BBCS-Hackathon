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

function ProviderUpdate() {
  const [foodstall, setFoodstall] = useState('');
  const [count, setCount] = useState('');

  const updateMeals = async () => {
    await axios.post('/meals', { foodstall, count });
    alert('Meals updated');
  };

  return (
    <div>
      <h2>Update Free Meals</h2>
      <input placeholder="Food Stall Name" onChange={(e) => setFoodstall(e.target.value)} />
      <input placeholder="Meal Count" onChange={(e) => setCount(e.target.value)} />
      <button onClick={updateMeals}>Update</button>
    </div>
  );
}

export default ProviderUpdate;
