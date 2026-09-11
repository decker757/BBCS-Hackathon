import { fireEvent, render, screen } from '@testing-library/react';
import App from './App';

test('opens the business sign-in flow from the actual meal-sharing homepage', () => {
  window.history.replaceState({}, '', '/');
  render(<App />);
  expect(screen.getByRole('heading', { name: 'NomNomNetwork' })).toBeInTheDocument();
  const login = screen.getAllByRole('link', { name: 'Login' }).find((link) => link.getAttribute('href') === '/businesslogin');
  fireEvent.click(login);
  expect(screen.getByLabelText('Username:')).toBeInTheDocument();
  expect(screen.getByLabelText('Password:')).toBeInTheDocument();
});

test('renders the existing About route with a path back to the homepage', () => {
  window.history.replaceState({}, '', '/about');
  render(<App />);
  expect(screen.getByRole('heading', { name: 'About NomNomNetwork' })).toBeInTheDocument();
  fireEvent.click(screen.getByRole('link', { name: 'Back to home' }));
  expect(screen.getByRole('heading', { name: 'NomNomNetwork' })).toBeInTheDocument();
});
