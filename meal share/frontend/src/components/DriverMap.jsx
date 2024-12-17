import logo from './meal share/frontend/src/logo.svg';
import './meal share/frontend/src/App.css'
import React, { useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

// Import pages
import About from './pages/About';
import DriverLogin from './components/DriverLogin';
import DriverAbout from './pages/DriverAbout';
import DriverMap from './components/DriverMap';
import ProviderLogin from './components/ProviderLogin';
import ProviderAbout from './pages/ProviderAbout';
import ProviderUpdate from './components/ProviderUpdate';

function DriverMap() {
  const [meals, setMeals] = useState([]);
  const [selectedMeal, setSelectedMeal] = useState(null);

  useEffect(() => {
    // Fetch available meals when component mounts
    const fetchMeals = async () => {
      try {
        const response = await axios.get('/api/meals/available');
        setMeals(response.data.meals);
      } catch (error) {
        console.error('Error fetching meals:', error);
      }
    };

    fetchMeals();
    // Optional: Set up periodic refresh
    const intervalId = setInterval(fetchMeals, 60000); // Refresh every minute
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Available Meals Map</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Meal List */}
        <div className="bg-white shadow rounded p-4">
          <h2 className="text-lg font-semibold mb-2">Meal Locations</h2>
          {meals.length === 0 ? (
            <p className="text-gray-500">No meals currently available</p>
          ) : (
            <ul>
              {meals.map((meal, index) => (
                <li 
                  key={index} 
                  className="p-2 hover:bg-green-100 cursor-pointer"
                  onClick={() => setSelectedMeal(meal)}
                >
                  {meal[0]} - {meal[1]}
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Placeholder for Map (would integrate with actual map service) */}
        <div className="bg-gray-100 rounded p-4 h-96">
          {selectedMeal ? (
            <div>
              <h3 className="text-xl font-bold">Selected Location</h3>
              <p>Restaurant: {selectedMeal[0]}</p>
              <p>Meal: {selectedMeal[1]}</p>
            </div>
          ) : (
            <p className="text-gray-500 text-center">Select a meal to view details</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default DriverMap;