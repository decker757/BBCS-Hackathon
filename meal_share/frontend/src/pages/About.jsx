import React from 'react';
import { Link } from 'react-router-dom';

export default function About() {
  return <main style={{ maxWidth: 720, margin: '0 auto', padding: '32px 16px', lineHeight: 1.6 }}>
    <h1>About NomNomNetwork</h1>
    <p>NomNomNetwork connects food businesses and delivery riders through shared meals and mutual appreciation.</p>
    <h2>For food businesses</h2>
    <p>Add the meals you can offer and keep their available quantities up to date. Your account manages your own meal listings.</p>
    <Link to="/businesslogin">Business sign in</Link>
    <h2>For delivery riders</h2>
    <p>Browse participating businesses and their available meals through the store locator.</p>
    <Link to="/driverlogin">Rider sign in</Link>
    <p><Link to="/">Back to home</Link></p>
  </main>;
}
