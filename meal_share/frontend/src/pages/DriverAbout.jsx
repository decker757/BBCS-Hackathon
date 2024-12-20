import React from "react";
import StoreLocator from "../components/StoreLocator"; // Adjust path as needed

const DriverAbout = () => {
  return (
    <div>
      <header style={{ padding: "20px", textAlign: "center", backgroundColor: "#f8f9fa" }}>
        <h1>Claim your free meal and eat with fellow riders</h1>
      </header>

      <main style={{ padding: "20px" }}>
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
