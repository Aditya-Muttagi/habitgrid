const API_BASE = "";

// Lightweight wrapper for API calls
async function apiRequest(path, method = 'GET', body = null, token = null) {
  // use provided token or fall back to stored session token
  token = token ?? getToken();

  const headers = {};
  if (body !== null && body !== undefined) {
    headers['Content-Type'] = 'application/json';
  }
  if (token) {
    headers['Authorization'] = 'Bearer ' + token;
  }

  let resp;
  try {
    resp = await fetch(API_BASE + path, {
      method,
      headers,
      body: body !== null && body !== undefined ? JSON.stringify(body) : null,
    });
  } catch (networkErr) {
    // network-level failure (DNS / connection / CORS, etc.)
    throw { message: networkErr.message || 'Network request failed' };
  }

  // handle 204 No Content
  if (resp.status === 204) return null;

  const contentType = resp.headers.get('content-type') || '';
  const isJson = contentType.includes('application/json');
  const data = isJson ? await resp.json() : null;

  if (!resp.ok) {
    // Normalize common error shapes
    if (data && data.detail) throw data;
    const err = data || { message: resp.statusText || 'Request failed' };
    throw err;
  }

  return data;
}

// Token helpers (sessionStorage so closing tab/browser clears session)
function setToken(token) {
  sessionStorage.setItem('token', token);
}

function getToken() {
  return sessionStorage.getItem('token');
}

function clearToken() {
  sessionStorage.removeItem('token');
}

// Navigation helpers
function requireAuth() {
  const t = getToken();
  if (!t) window.location.href = 'login.html';
}

function protectIfAuthed() {
  const t = getToken();
  if (t) window.location.href = 'habits.html';
}
