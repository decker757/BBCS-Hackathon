import React, { useState } from 'react';
import './DriverSignUp.css';

function BusinessSignUp() {
  // State to store user input
  const [formData, setFormData] = useState({
    firstname: '',
    lastname: '',
    role: '',
    businessemail: '',
    username: '',
    password: '',
  });

  // Handle changes in form inputs
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form Submitted', formData);
    alert('Sign Up Successful!'); // Replace with actual functionality
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
            name="email"
            placeholder="Enter your business email"
            value={formData.email}
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
