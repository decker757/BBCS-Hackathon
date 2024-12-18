import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function BusinessAbout() {
    const location = useLocation();
    const navigate = useNavigate();

    const username = location.state?.username || 'User';

    const handleLogout =() => {
        navigate('/');
    };
    return (
        <div>
            <h2>Welcome, {username}!</h2>
            <button onClick={handleLogout}>Logout</button>
        </div>
    ); 
}

export default BusinessAbout;