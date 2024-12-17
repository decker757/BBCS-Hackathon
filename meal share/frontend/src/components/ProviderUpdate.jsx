import React, { useState } from 'react';
import axios from 'axios';

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
