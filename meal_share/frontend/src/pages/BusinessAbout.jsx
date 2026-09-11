import React, { useState } from 'react';
import ProviderUpdate from '../components/ProviderUpdate';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';
import './BusinessAbout.css';

function BusinessAbout() {
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
  return <div className="containerBusiness">
    <h2>Your meals</h2>
    <ProviderUpdate />
    {error && <p role="alert">{error}</p>}
    <button onClick={logout} className="business_logout">Logout</button>
  </div>;
}

export default BusinessAbout;
