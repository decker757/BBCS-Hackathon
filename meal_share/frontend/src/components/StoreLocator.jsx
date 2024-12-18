import React, { useEffect, useState } from "react";

const StoreLocator = () => {
  const [locations, setLocations] = useState([]);

  useEffect(() => {
    // Fetch dynamic location data from the JSON file
    const fetchLocations = async () => {
      try {
        const response = await fetch("/restaurants.json"); // Assuming JSON is in the public folder
        const data = await response.json();
        setLocations(data);
      } catch (error) {
        console.error("Error fetching locations:", error);
      }
    };

    fetchLocations();
  }, []);

  useEffect(() => {
    if (locations.length > 0) {
      const CONFIGURATION = {
        locations: locations,
        mapOptions: {
          center: { lat: 1.3521, lng: 103.8198 }, // Default center: Singapore
          fullscreenControl: true,
          mapTypeControl: false,
          streetViewControl: false,
          zoom: 12,
          zoomControl: true,
          maxZoom: 17,
          mapId: "",
        },
        mapsApiKey: "AIzaSyBaNy6ZCohVuDnfSY1CCRLe8s6E7s_9kJw",
        capabilities: {
          input: true,
          autocomplete: true,
          directions: true,
          distanceMatrix: true,
          details: true,
          actions: false,
        },
      };

      const loadStoreLocator = async () => {
        // Load Extended Component Library dynamically
        await import("https://unpkg.com/@googlemaps/extended-component-library@0.6");

        // Configure the locator once locations are updated
        await customElements.whenDefined("gmpx-store-locator");
        const locator = document.querySelector("gmpx-store-locator");
        if (locator) {
          locator.configureFromQuickBuilder(CONFIGURATION);
        }
      };

      loadStoreLocator();
    }
  }, [locations]); // Re-run when `locations` changes

  return (
    <div style={{ width: "100%", height: "100vh" }}>
      {/* API Loader for Google Maps */}
      <gmpx-api-loader
        key="AIzaSyBaNy6ZCohVuDnfSY1CCRLe8s6E7s_9kJw"
        solution-channel="GMP_QB_locatorplus_v10_cABCDE"
      ></gmpx-api-loader>

      {/* Store Locator */}
      <gmpx-store-locator map-id="DEMO_MAP_ID"></gmpx-store-locator>
    </div>
  );
};

export default StoreLocator;
