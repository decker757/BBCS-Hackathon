import React from 'react';
import ProviderUpdate from '../components/ProviderUpdate';
import { useLocation, useNavigate } from 'react-router-dom';

function BusinessAbout({username}) {
    const location = useLocation();
    const navigate = useNavigate();

    const handleLogout =() => {
        navigate('/');
    };
    return (
        <div>
            <h2>Welcome {username}</h2>
            <ProviderUpdate/>
            <button onClick={handleLogout}>Logout</button>
        </div>
    ); 
}

export default BusinessAbout;