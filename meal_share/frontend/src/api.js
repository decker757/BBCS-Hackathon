import axios from 'axios';

// Use the same origin in production, or an explicitly configured API origin.
// CRA's development proxy forwards these relative paths to the local backend.
export const api = axios.create({
  baseURL: (process.env.REACT_APP_API_BASE_URL || '').replace(/\/$/, ''),
  withCredentials: true,
  timeout: 10000,
  headers: { 'X-Meal-Share-Request': '1' },
});

// Existing forms share the cookie, timeout and origin configuration.
export async function apiFetch(path, options = {}) {
  const response = await api.request({
    url: path,
    method: options.method || 'GET',
    data: options.body ? JSON.parse(options.body) : undefined,
    headers: options.headers,
    signal: options.signal,
    validateStatus: () => true,
  });
  return { ok: response.status >= 200 && response.status < 300, status: response.status, json: async () => response.data };
}
