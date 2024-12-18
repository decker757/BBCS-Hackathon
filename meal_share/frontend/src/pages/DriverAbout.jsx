import React from 'react';
import StoreLocator from "../components/StoreLocator";
import { useLocation, useNavigate } from 'react-router-dom';

function DriverAbout() {
    const location = useLocation();
    const navigate = useNavigate();

    const username = location.state?.username || 'User';

    const handleLogout =() => {
        navigate('/');
    };
    return (
        <div>
            <h2>Welcome, {username}!</h2>
            <h1>Free Meals Locator</h1>
            <StoreLocator/>
            <button onClick={handleLogout}>Logout</button>
        </div>
    ); 
}

export default DriverAbout;
