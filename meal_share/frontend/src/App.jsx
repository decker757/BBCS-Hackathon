import logo from './logo.svg';
import './App.css'
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

// Import pages
import About from './pages/About';
import DriverAbout from './pages/DriverAbout';
import StoreLocator from './components/StoreLocator';
import BusinessAbout from './pages/BusinessAbout';
import ProviderUpdate from './components/ProviderUpdate';
import Home from './pages/Home';
import DriverLogin from './pages/DriverLogin';
import DriverSignUp from './pages/DriverSignUp';
import BusinessSignUp from './pages/BusinessSignUp';
import BusinessLogin from './pages/BusinessLogin';

function App() {
  const [loggedInUsername, setLoggedInUsername] = useState(null);
  return (
    <Router>
      <Routes>
      <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/driverlogin" element={<DriverLogin />} />
        <Route path="/driversignup" element={<DriverSignUp />} />
        <Route path="/businesssignup" element={<BusinessSignUp />} />
        <Route path="/businesslogin" element={<BusinessLogin setLoggedInUsername={setLoggedInUsername} />} />
        <Route path="/storelocator" element={<StoreLocator />} />
        <Route path="/providerupdate" element={<ProviderUpdate username={loggedInUsername}/>} />
        <Route path="/driverabout" element={<DriverAbout />} />
        <Route path="/businessabout" element={<BusinessAbout username={loggedInUsername} />} />
      </Routes>
    </Router>
  );
}

export default App;

/* hi */