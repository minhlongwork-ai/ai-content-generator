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

// --- Skill System API ---

export async function apiGetSkills(): Promise<any> {
  return apiFetch('/api/skills');
}

export async function apiGetSkillConfig(skillName: string): Promise<any> {
  return apiFetch(`/api/skills/${skillName}/config`);
}

export async function apiUpdateSkillConfig(skillName: string, config: Record<string, any>): Promise<any> {
  return apiFetch(`/api/skills/${skillName}/config`, {
    method: 'POST',
    body: JSON.stringify(config),
  });
}

export async function apiGenerateWithSkill(skillName: string, body: Record<string, any>): Promise<any> {
  return apiFetch(`/api/skills/${skillName}/generate`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

export async function apiGetHistory(limit = 10): Promise<any> {
  return apiFetch(`/api/skills/generations/history?limit=${limit}`);
}

export async function apiGetAnalytics(): Promise<any> {
  return apiFetch('/api/skills/analytics');
}
