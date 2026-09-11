import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { api } from '../api';
import './ProviderUpdate.css';

function ProviderUpdate() {
  const navigate = useNavigate();
  const [username, setUsername] = useState(null);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({ dishName: '', mealType: '', quantity: '' });
  const [meals, setMeals] = useState([]);
  const [editingIndex, setEditingIndex] = useState(null);
  const [newQuantity, setNewQuantity] = useState('');

  useEffect(() => {
    const controller = new AbortController();
    async function load() {
      try {
        const identity = await api.get('/api/session', { signal: controller.signal });
        if (identity.data.role !== 'business' || !identity.data.username) {
          navigate('/businesslogin', { replace: true });
          return;
        }
        const owner = identity.data.username;
        const response = await api.get(`/business/updatemeals/${encodeURIComponent(owner)}`, { signal: controller.signal });
        if (!controller.signal.aborted) {
          setUsername(owner);
          setMeals(response.data);
        }
      } catch (failure) {
        if (!controller.signal.aborted) setError('Unable to load your meals. Please sign in again or retry.');
      } finally {
        if (!controller.signal.aborted) setLoading(false);
      }
    }
    load();
    return () => controller.abort();
  }, [navigate]);

  async function save(path, method, data, onSaved) {
    if (busy || !username) return;
    setBusy(true);
    setError('');
    let saved = false;
    try {
      await api.request({ url: path, method, data });
      saved = true;
      onSaved();
      const response = await api.get(`/business/updatemeals/${encodeURIComponent(username)}`);
      setMeals(response.data);
    } catch (failure) {
      if (failure.response?.status === 401) {
        setUsername(null);
        setMeals([]);
        setError('Your session has expired. Please sign in again.');
      } else if (saved) {
        setError('Your changes were saved, but the list could not refresh. Reload this page to see them.');
      } else setError(failure.response?.data?.message || 'Unable to confirm your changes. Reload your meals before retrying.');
    } finally {
      setBusy(false);
    }
  }

  function addMeal(event) {
    event.preventDefault();
    save(`/meals/available/${encodeURIComponent(username)}`, 'POST', formData,
      () => setFormData({ dishName: '', mealType: '', quantity: '' }));
  }

  if (loading) return <p role="status">Loading your meals…</p>;
  return (
    <section className="meal-manager" aria-label="Manage your meals">
      {error && <p role="alert">{error} {!username && <Link to="/businesslogin">Sign in</Link>}</p>}
      {username && <>
        <p>Signed in as {username}</p>
        <form onSubmit={addMeal}>
          {['dishName', 'mealType', 'quantity'].map((name) => (
            <label key={name} htmlFor={name}>
              {{ dishName: 'Dish name', mealType: 'Meal type', quantity: 'Quantity' }[name]}
              <input id={name} name={name} type={name === 'quantity' ? 'number' : 'text'} min={name === 'quantity' ? '0' : undefined}
                step={name === 'quantity' ? '1' : undefined} value={formData[name]} disabled={busy}
                onChange={(event) => setFormData({ ...formData, [name]: event.target.value })} required />
            </label>
          ))}
          <button type="submit" disabled={busy}>{busy ? 'Saving…' : 'Add Meal'}</button>
        </form>
        <h3>Available meals</h3>
        {meals.length === 0 && <p>No meals added yet.</p>}
        <ul>
          {meals.map((meal, index) => (
            <li key={index}>
              <span>{meal.dishName} ({meal.mealType}) — Quantity: </span>
              {editingIndex === index ? <>
                <input type="number" min="0" step="1" aria-label={`Quantity for ${meal.dishName}`} value={newQuantity}
                  onChange={(event) => setNewQuantity(event.target.value)} disabled={busy} />
                <button disabled={busy} onClick={() => save(`/business/updatemeals/${encodeURIComponent(username)}`, 'PUT',
                  { dishName: meal.dishName, newQuantity }, () => setEditingIndex(null))}>Save</button>
                <button disabled={busy} onClick={() => setEditingIndex(null)}>Cancel</button>
              </> : <>
                <span>{meal.quantity}</span>
                <button aria-label={`Edit ${meal.dishName}`} disabled={busy} onClick={() => {
                  setEditingIndex(index); setNewQuantity(meal.quantity);
                }}>Edit</button>
              </>}
            </li>
          ))}
        </ul>
      </>}
    </section>
  );
}

export default ProviderUpdate;
