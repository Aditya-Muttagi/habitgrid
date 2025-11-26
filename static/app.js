/* Shared JS utilities and API client for HabitGrid static UI.
   Edit API_BASE to point where your FastAPI backend serves API endpoints. */
const API_BASE = ""; // <-- change to e.g. "http://localhost:8000/api" if needed

// Lightweight wrapper for API calls
async function apiRequest(path, method = 'GET', body = null, token = null) {
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = 'Bearer ' + token;
  const resp = await fetch(API_BASE + path, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null
  });
  const isJson = resp.headers.get('content-type') && resp.headers.get('content-type').includes('application/json');
  const data = isJson ? await resp.json() : null;
  if (!resp.ok) {
    // Try to normalize common error shapes
    if (data && data.detail) throw data;
    const err = data || { message: resp.statusText || 'Request failed' };
    throw err;
  }
  return data;
}

// Token helpers (localStorage)
function saveToken(token) { localStorage.setItem('hg_token', token); }
function getToken() { return localStorage.getItem('hg_token'); }
function clearToken() { localStorage.removeItem('hg_token'); }

// Navigation helpers
function requireAuth() {
  const t = getToken();
  if (!t) window.location.href = 'login.html';
}
function protectIfAuthed() {
  const t = getToken();
  if (t) window.location.href = 'habits.html';
}
