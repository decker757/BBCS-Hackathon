import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import { api } from '../api';
import StoreLocator from "../components/StoreLocator"; // Adjust path as needed

const DriverAbout = () => {
  const navigate = useNavigate();
  const [error, setError] = useState('');
  async function logout() {
    try {
      await api.post('/api/logout');
      navigate('/');
    } catch (failure) {
      setError('Unable to sign out. Please retry.');
    }
  }
  return (
    <div>
      <header style={{ padding: "20px", textAlign: "center", backgroundColor: "#f8f9fa" }}>
        <h1>Claim your free meal and eat with fellow riders</h1>
      </header>

      <main style={{ padding: "20px" }}>
        {error && <p role="alert">{error}</p>}
        <button onClick={logout}>Logout</button>
        <section>
          <p>
            Find stores offering meals using the store locator.
          </p>
        </section>

        <section>
          <h2>Available Meal Locations</h2>
          {/* Integrating the StoreLocator component */}
          <StoreLocator/>
        </section>
      </main>

      <footer style={{ padding: "20px", textAlign: "center", backgroundColor: "#f8f9fa" }}>
        <p>© 2024 NomNomNetwork. All Rights Reserved.</p>
      </footer>
    </div>
  );
};

export default DriverAbout;
