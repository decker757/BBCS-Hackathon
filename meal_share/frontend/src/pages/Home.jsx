import React from 'react';
import { Link } from 'react-router-dom';
import bgImage from './testimage.jpg';
import './Home.css';

function Home() {
  return (
    <div className="home-container" style={{backgroundImage: `url(${bgImage})`}}>
      <h2 className="home-overview">NomNomNetwork</h2>
      <h3 className="overview-description">
        Connecting delivery riders and restaurant owners through shared meals and mutual appreciation
      </h3>

      <div className="flex-container">
        <div className="driver-container">
          <h2 className="driver-header1">Here as a rider?</h2>
          <h2 className="driver-header">Enjoy free meals from generous restaurants and connect with fellow riders over a shared table 🎄</h2>
          <button className="login-button">
            <Link to="/driverlogin" style={{ textDecoration: 'none', color: 'white' }}>Login</Link>
          </button>
          <button className="signup-button"> 
            <Link to="/driversignup" style={{ textDecoration: 'none', color: 'white' }}>Sign Up</Link>
            </button>
        </div>
        <div className="business-container">
          <h2 className="driver-header1">Here as a food business owner?</h2>
          <h2 className="business-header">Show appreciation to the riders who support your business by sharing a meal with them 🎁</h2>
          <button className="login-button">
            <Link to="/businesslogin" style={{ textDecoration: 'none', color: 'white' }}>Login</Link>
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
