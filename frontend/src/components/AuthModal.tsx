/* src/components/AuthModal.tsx — Register / Login Modal */
import { useState } from 'react';
import { showToast } from './Toast';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface AuthModalProps {
  onClose: () => void;
  onAuthSuccess: (token: string, user: any) => void;
}

export default function AuthModal({ onClose, onAuthSuccess }: AuthModalProps) {
  const [mode, setMode] = useState<'login' | 'register'>('register');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const endpoint = mode === 'register' ? '/api/auth/register' : '/api/auth/login';
      const body = mode === 'register'
        ? { email, password, name }
        : { email, password };

      const res = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || 'Authentication failed');
      }

      if (data.success) {
        localStorage.setItem('token', data.token);
        showToast('success', mode === 'register' ? 'Account created! Welcome!' : 'Welcome back!');
        onAuthSuccess(data.token, data.user);
      }
    } catch (err: any) {
      showToast('error', err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>×</button>

        <div className="modal-header">
          <h2>{mode === 'register' ? '✨ Create Account' : '👋 Welcome Back'}</h2>
          <p>{mode === 'register' ? 'Start generating content for free' : 'Sign in to your account'}</p>
        </div>

        <form onSubmit={handleSubmit}>
          {mode === 'register' && (
            <div className="form-group">
              <label>Name</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Your name"
              />
            </div>
          )}

          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder={mode === 'register' ? 'Min 6 characters' : 'Your password'}
              required
              minLength={6}
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? '⏳ Please wait...' : mode === 'register' ? 'Create Account' : 'Sign In'}
          </button>
        </form>

        <div className="modal-footer">
          {mode === 'register' ? (
            <p>Already have an account? <button className="link-btn" onClick={() => setMode('login')}>Sign In</button></p>
          ) : (
            <p>New here? <button className="link-btn" onClick={() => setMode('register')}>Create Account</button></p>
          )}
        </div>
      </div>
    </div>
  );
}
