import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import axios from "axios";

function ProviderUpdate() {
  const location = useLocation();
  const username = location.state?.username;

  console.log("Received username in ProviderUpdate:", username); // Debug log

  const [formData, setFormData] = useState({
    dishName: "",
    mealType: "",
    quantity: "",
  });
  const [meals, setMeals] = useState([]);
  const [editingIndex, setEditingIndex] = useState(null);
  const [newQuantity, setNewQuantity] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`http://127.0.0.1:5000/meals/available/${username}`, formData, {
        headers: { "Content-Type": "application/json" },
      });
      fetchMeals(); // Fetch updated meals
      setFormData({ dishName: "", mealType: "", quantity: "" }); // Reset form
    } catch (error) {
      console.error("Error adding meal:", error.response?.data || error.message);
    }
  };

  const fetchMeals = async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/business/updatemeals/${username}`);
      setMeals(response.data);
    } catch (error) {
      console.error("Error fetching meals:", error.response?.data || error.message);
    }
  };

  const handleEditClick = (index, currentQuantity) => {
    setEditingIndex(index);
    setNewQuantity(currentQuantity);
  };

  const handleUpdateQuantity = async (index, meal) => {
    try {
      // Send a PUT request to update the meal quantity
      await axios.put(`http://127.0.0.1:5000/business/updatemeals/${username}`, {
        dishName: meal.dishName,
        newQuantity: newQuantity,
      });
      setEditingIndex(null); // Exit editing mode
      fetchMeals(); // Refresh updated meals
    } catch (error) {
      console.error("Error updating quantity:", error.response?.data || error.message);
    }
  };

  useEffect(() => {
    fetchMeals();
  }, [username]); // Fetch meals when username changes

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="dishName"
          placeholder="Dish Name"
          value={formData.dishName}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="mealType"
          placeholder="Meal Type"
          value={formData.mealType}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="quantity"
          placeholder="Quantity"
          value={formData.quantity}
          onChange={handleChange}
          required
        />
        <button type="submit">Add Meal</button>
      </form>

      <h3>Updated Meals</h3>
      <ul>
        {meals.map((meal, index) => (
          <li key={index}>
            {meal.dishName} ({meal.mealType}) - Quantity:{" "}
            {editingIndex === index ? (
              <>
                <input
                  type="number"
                  value={newQuantity}
                  onChange={(e) => setNewQuantity(e.target.value)}
                />
                <button onClick={() => handleUpdateQuantity(index, meal)}>Save</button>
              </>
            ) : (
              <>
                {meal.quantity}
                <button onClick={() => handleEditClick(index, meal.quantity)}>Edit</button>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ProviderUpdate;

