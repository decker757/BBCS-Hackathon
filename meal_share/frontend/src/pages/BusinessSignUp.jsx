import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import './DriverSignUp.css';

function BusinessSignUp() {
  const navigate = useNavigate();
  // State to store user input
  const [formData, setFormData] = useState({
    firstname: '',
    lastname: '',
    role: '',
    businessemail: '',
    address: '',
    postal: '',
    username: '',
    password: '',
  });

  // Handle changes in form inputs
  const handleChange = (e) => {
    const { name, value } = e.target;
    
    setFormData({ ...formData, [name]: value });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:5000/api/business/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();
      if (!response.ok) {
        // Handle errors: check if errors is a list
        if (result.errors && Array.isArray(result.errors)) {
          alert(`Errors:\n${result.errors.join("\n")}`);
        } else if (result.message) {
          alert(`Error: ${result.message}`);
        } else {
          alert("An unknown error occurred.");
        }
      } else {
        // Handle success
        alert(result.message || "Registration successful!");
        navigate('/businesslogin');
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Network error or server not reachable.");
    }
  };

  return (
    <div className="signup-container">
      <form className="signup-form" onSubmit={handleSubmit}>
        <h2>🎄 Sign Up 🎅</h2>
        <div className='form-group'>
        <label>First Name</label>
        <input 
            type="text"
            name="firstname"
            placeholder="Enter your first name"
            value={formData.firstname}
            onChange={handleChange}
            required
         />
         </div>
        <div className='form-group'>
        <label>Last Name</label>
        <input 
            type="text"
            name="lastname"
            placeholder="Enter your last name"
            value={formData.lastname}
            onChange={handleChange}
            required
         />
         </div>
        <div className='form-group'>
            <label>Role</label>
            <input 
                type="text"
                name="role"
                placeholder="Enter your role in your enterprise"
                value={formData.role}
                onChange={handleChange}
                required
            />
         </div> 
        {/* Email Field */}
        <div className="form-group">
          <label>Business Email</label>
          <input
            type="email"
            name="businessemail"
            placeholder="Enter your business email"
            value={formData.businessemail}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Address</label>
          <input
            type="text"
            name="address"
            placeholder="Enter your business' address"
            value={formData.address}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Postal Code</label>
          <input
            type="text"
            name="postal"
            placeholder="Enter your business' postal code"
            value={formData.postal}
            onChange={handleChange}
            required
          />
        </div>
        {/* Username Field */}
        <div className="form-group">
          <label>Username</label>
          <input
            type="text"
            name="username"
            placeholder="Enter your username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>


        {/* Password Field */}
        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            name="password"
            placeholder="Enter your password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

        {/* Submit Button */}
        <button type="submit" className="signupp-button">Sign Up</button>
      </form>
    </div>
  );
}

export default BusinessSignUp;
