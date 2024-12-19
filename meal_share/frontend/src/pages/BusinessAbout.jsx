import React from 'react';
import ProviderUpdate from '../components/ProviderUpdate';
import { useLocation, useNavigate } from 'react-router-dom';
import "./BusinessAbout.css"

function BusinessAbout({username}) {
    const location = useLocation();
    const navigate = useNavigate();

    const handleLogout =() => {
        navigate('/');
    };
    return (
        <div className='containerBusiness'>
            <h2>Welcome {username}</h2>
            <ProviderUpdate/>
            <button onClick={handleLogout} className='business_logout'>Logout</button>
        </div>
    ); 
}

export default BusinessAbout;