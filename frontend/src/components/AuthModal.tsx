/* src/components/AuthModal.tsx — Đăng ký / Đăng nhập (Tiếng Việt) */
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
      const body = mode === 'register' ? { email, password, name } : { email, password };
      const res = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Xác thực thất bại');
      if (data.success) {
        localStorage.setItem('token', data.token);
        showToast('success', mode === 'register' ? 'Tạo tài khoản thành công! Chào mừng!' : 'Chào mừng quay lại!');
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
          <h2>{mode === 'register' ? '✨ Tạo Tài Khoản' : '👋 Chào Mừng Quay Lại'}</h2>
          <p>{mode === 'register' ? 'Bắt đầu tạo nội dung miễn phí' : 'Đăng nhập vào tài khoản'}</p>
        </div>
        <form onSubmit={handleSubmit}>
          {mode === 'register' && (
            <div className="form-group">
              <label>Tên</label>
              <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Tên của bạn" />
            </div>
          )}
          <div className="form-group">
            <label>Email</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" required />
          </div>
          <div className="form-group">
            <label>Mật khẩu</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder={mode === 'register' ? 'Tối thiểu 6 ký tự' : 'Mật khẩu'} required minLength={6} />
          </div>
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? '⏳ Vui lòng chờ...' : mode === 'register' ? 'Tạo Tài Khoản' : 'Đăng Nhập'}
          </button>
        </form>
        <div className="modal-footer">
          {mode === 'register' ? (
            <p>Đã có tài khoản? <button className="link-btn" onClick={() => setMode('login')}>Đăng Nhập</button></p>
          ) : (
            <p>Chưa có tài khoản? <button className="link-btn" onClick={() => setMode('register')}>Tạo Tài Khoản</button></p>
          )}
        </div>
      </div>
    </div>
  );
}
