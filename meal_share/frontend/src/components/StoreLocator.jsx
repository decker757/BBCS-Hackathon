import React, { useEffect, useState } from "react";
import { GoogleMap, LoadScript, Marker, InfoWindow } from "@react-google-maps/api";

const containerStyle = {
  width: "100%",
  height: "400px",
};

const defaultCenter = {
  lat: 1.3521, // Singapore Latitude
  lng: 103.8198, // Singapore Longitude
};

const StoreLocator = () => {
  const [locations, setLocations] = useState([]); // Stores all fetched locations
  const [selectedLocation, setSelectedLocation] = useState(null); // Tracks the selected marker's location

  // Fetch locations from the backend
  useEffect(() => {
    const fetchLocations = async () => {
      try {
        console.log('fetching locations');
        const response = await fetch("http://localhost:5000/api/locations");
        console.log('response', response);
        const data = await response.json();
        console.log("Data:", data); // Debug log
        setLocations(data); // Save locations to state
      } catch (error) {
        console.error("Error fetching locations:", error);
      }
    };

    fetchLocations();
  }, []);

  return (
    <div>
      <h1>Store Locator</h1>

      <LoadScript googleMapsApiKey="AIzaSyB33V6scRrJ6yK36qt-XD_DgshA_CHPZ6U">
        <GoogleMap
          mapContainerStyle={containerStyle}
          center={defaultCenter} // Default center, adjust dynamically if needed
          zoom={12}
        >
          {/* Display Markers */}
          {locations.map((location, index) => (
            <Marker
              key={index}
              position={location.coords} // Use the coordinates from backend
              onClick={() => setSelectedLocation(location)} // Open info window on click
            />
          ))}

          {/* Display InfoWindow when a marker is selected */}
          {selectedLocation && (
            <InfoWindow
              position={selectedLocation.coords}
              onCloseClick={() => setSelectedLocation(null)} // Close info window
            >
              <div>
                <h2>{selectedLocation.title}</h2>
                <h3>{selectedLocation.address1}</h3>
                <h3>{selectedLocation.address2}</h3>
                <div>
                  <h3>Meals:</h3>
                  <ul>
                    {selectedLocation.meals && selectedLocation.meals.length > 0 ? (
                      selectedLocation.meals.map((meal, index) => (
                        <li key={index}>
                          <h4>{meal.dishName} ({meal.mealType}): {meal.quantity}</h4>
                        </li>
                      ))
                    ) : (
                      <p>No meals available</p>
                    )}
                  </ul>
                </div>
                {/* Button to open in Google Maps */}
                <button
                  style={{
                    marginTop: "10px",
                    padding: "10px",
                    backgroundColor: "#4285F4",
                    color: "white",
                    border: "none",
                    borderRadius: "5px",
                    cursor: "pointer",
                  }}
                  onClick={() => {
                    const lat = selectedLocation.coords.lat;
                    const lng = selectedLocation.coords.lng;
                    const googleMapsURL = `https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}`;
                    window.open(googleMapsURL, "_blank");
                  }}
                >
                  Navigate in Google Maps
                </button>
              </div>
            </InfoWindow>
          )}
        </GoogleMap>
      </LoadScript>
    </div>
  );
};

export default StoreLocator;
