/* src/api.ts — Shared API client with auth token */
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function getAuthToken(): string | null {
  return localStorage.getItem('token');
}

export async function apiFetch(
  endpoint: string,
  options: RequestInit = {}
): Promise<any> {
  const token = getAuthToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });
  return res.json();
}

export async function apiGenerate(
  type: string,
  body: Record<string, any>
): Promise<any> {
  return apiFetch(`/api/generate/${type}`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}
