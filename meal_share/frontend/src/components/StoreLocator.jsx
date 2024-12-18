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
  const [locations, setLocations] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState(null);

  // Fetch locations from the backend
  useEffect(() => {
    const fetchLocations = async () => {
      try {
        const response = await fetch("/api/locations");
        const data = await response.json();
        setLocations(data);
      } catch (error) {
        console.error("Error fetching locations:", error);
      }
    };

    fetchLocations();
  }, []);

  return (
    <div>
      <h1>Store Locator</h1>
      <LoadScript googleMapsApiKey="YOUR_GOOGLE_MAPS_API_KEY">
        <GoogleMap
          mapContainerStyle={containerStyle}
          center={defaultCenter}
          zoom={12}
        >
          {/* Map Markers */}
          {locations.map((location, index) => (
            <Marker
              key={index}
              position={location.coords}
              onClick={() => setSelectedLocation(location)}
            />
          ))}

          {/* Info Window for Selected Location */}
          {selectedLocation && (
            <InfoWindow
              position={selectedLocation.coords}
              onCloseClick={() => setSelectedLocation(null)}
            >
              <div>
                <h2>{selectedLocation.title}</h2>
                <p>{selectedLocation.address1}</p>
                <p>{selectedLocation.address2}</p>
              </div>
            </InfoWindow>
          )}
        </GoogleMap>
      </LoadScript>
    </div>
  );
};

export default StoreLocator;
