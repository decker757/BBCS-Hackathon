import React from 'react';
import { Link } from 'react-router-dom';
import bgImage from './testimage2.jpg';
import './Home.css';

function Home() {
  return (
    <div className="home-container" style={{backgroundImage: `url(${bgImage})`}}>
      <h2 className="home-overview">🎄 Overview 🎅</h2>
      <h3 className="overview-description">
        Join us this festive season in paying back to the food delivery drivers! Pay a meal forward and dine in with them.
        Happy Holidays!
      </h3>

      <div className="flex-container">
        <div className="driver-container">
          <h2 className="driver-header">🎁 Here as a delivery driver?</h2>

          <button className="login-button">
            <Link to="/DriverLogin" style={{ textDecoration: 'none', color: 'white' }}>Login</Link>
          </button>
          <button className="signup-button"> 
            <Link to="/driversignup" style={{ textDecoration: 'none', color: 'white' }}>Sign Up</Link>
            </button>
        </div>
        <div className="business-container">
          <h2 className="business-header">🎄 Here as a business owner?</h2>
          <button className="login-button">
            <Link to="/BusinessLogin" style={{ textDecoration: 'none', color: 'white' }}>Login</Link>
          </button>
          <button className="signup-button">
            <Link to="/businesssignup" style={{ textDecoration: 'none', color: 'white' }}>Sign Up</Link>
          </button>
        </div>
      </div>

      {/* Snowfall Decorations */}
      <div className="snowflake" style={{ left: '10%' }}></div>
      <div className="snowflake" style={{ left: '30%' }}></div>
      <div className="snowflake" style={{ left: '50%' }}></div>
      <div className="snowflake" style={{ left: '70%' }}></div>
      <div className="snowflake" style={{ left: '90%' }}></div>
    </div>
  );
}

export default Home;
