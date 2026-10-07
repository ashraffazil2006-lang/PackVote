// src/services/api.js
const rawBase = import.meta.env.VITE_API_URL !== undefined
  ? import.meta.env.VITE_API_URL
  : '';
const API_BASE = rawBase ? rawBase.replace(/\/+$/, '') : '';

function handleNetworkError(err) {
  if (err.name === 'TypeError' || err.message === 'Failed to fetch') {
    const target = API_BASE || 'backend server';
    return new Error(`Cannot connect to PACKVOTE backend (${target}). Please ensure the backend is running.`);
  }
  return err;
}

export async function checkHealth() {
  try {
    const res = await fetch(`${API_BASE}/api/health`);
    if (!res.ok) throw new Error('Backend unavailable');
    return await res.json();
  } catch (err) {
    throw handleNetworkError(err);
  }
}

export async function getRecommendations(payload) {
  try {
    const res = await fetch(`${API_BASE}/api/recommend`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(err.detail || `API error ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    throw handleNetworkError(err);
  }
}

export async function getDestinationDetails(name) {
  try {
    const res = await fetch(`${API_BASE}/api/destination/${encodeURIComponent(name)}`);
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Destination not found' }));
      throw new Error(err.detail || `API error ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    throw handleNetworkError(err);
  }
}

export async function getSimilarDestinations(name) {
  try {
    const res = await fetch(`${API_BASE}/api/destination/${encodeURIComponent(name)}/similar`);
    if (!res.ok) return { similar: [] };
    return await res.json();
  } catch (err) {
    return { similar: [] };
  }
}

export async function getMLAnalytics() {
  try {
    const res = await fetch(`${API_BASE}/api/analytics`);
    if (!res.ok) throw new Error('Failed to load ML analytics data');
    return await res.json();
  } catch (err) {
    throw handleNetworkError(err);
  }
}

export async function sendAssistantMessage(message, context = null) {
  try {
    const res = await fetch(`${API_BASE}/api/assistant/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, context }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Assistant service unavailable' }));
      throw new Error(err.detail || `API error ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    throw handleNetworkError(err);
  }
}


