/* src/App.tsx — Main App with Sidebar + Auth + Routing + Light Mode (Tiếng Việt) */
import { useState, useEffect } from 'react';
import Landing from './components/Landing';
import Pricing from './components/Pricing';
import Dashboard from './components/Dashboard';
import ProductDescription from './components/ProductDescription';
import CaptionSEO from './components/CaptionSEO';
import AdCopy from './components/AdCopy';
import VideoScript from './components/VideoScript';
import Settings from './components/Settings';
import AuthModal from './components/AuthModal';
import { ToastContainer } from './components/Toast';
import './App.css';

type Page = 'landing' | 'dashboard' | 'product' | 'caption' | 'ad' | 'video' | 'settings' | 'pricing';

const navItems: { id: Page; label: string; icon: string; group: string }[] = [
  { id: 'dashboard', label: 'Tổng Quan', icon: '📊', group: 'main' },
  { id: 'product', label: 'Mô Tả SP', icon: '📝', group: 'tools' },
  { id: 'caption', label: 'Caption & SEO', icon: '🔍', group: 'tools' },
  { id: 'ad', label: 'Quảng Cáo', icon: '🎯', group: 'tools' },
  { id: 'video', label: 'Video AI', icon: '🎬', group: 'tools' },
  { id: 'pricing', label: 'Bảng Giá', icon: '💎', group: 'account' },
  { id: 'settings', label: 'Cài Đặt', icon: '⚙️', group: 'account' },
];

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function App() {
  const [page, setPage] = useState<Page>('landing');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [user, setUser] = useState<any>(null);
  const [showAuth, setShowAuth] = useState(false);
  const [darkMode, setDarkMode] = useState(true);

  useEffect(() => {
    const handler = (e: Event) => {
      const detail = (e as CustomEvent).detail;
      if (detail === 'auth') setShowAuth(true);
      else if (detail) setPage(detail as Page);
    };
    window.addEventListener('navigate', handler);
    return () => window.removeEventListener('navigate', handler);
  }, []);

  useEffect(() => {
    if (token) fetchUser();
    else setUser(null);
  }, [token]);

  useEffect(() => {
    document.documentElement.classList.toggle('light-mode', !darkMode);
  }, [darkMode]);

  const fetchUser = async () => {
    try {
      const res = await fetch(`${API_URL}/api/auth/me`, { headers: { Authorization: `Bearer ${token}` } });
      if (res.ok) { const data = await res.json(); setUser(data.user); }
      else { localStorage.removeItem('token'); setToken(null); }
    } catch { /* backend offline */ }
  };

  const handleAuthSuccess = (newToken: string, newUser: any) => {
    setToken(newToken); setUser(newUser); setShowAuth(false); setPage('dashboard');
  };

  const handleLogout = () => { localStorage.removeItem('token'); setToken(null); setUser(null); setPage('landing'); };

  const renderPage = () => {
    switch (page) {
      case 'landing': return <Landing onGetStarted={() => token ? setPage('dashboard') : setShowAuth(true)} onViewPricing={() => setPage('pricing')} />;
      case 'dashboard': return <Dashboard token={token} user={user} />;
      case 'product': return <ProductDescription token={token} />;
      case 'caption': return <CaptionSEO token={token} />;
      case 'ad': return <AdCopy token={token} />;
      case 'video': return <VideoScript token={token} />;
      case 'settings': return <Settings token={token} user={user} onLogout={handleLogout} />;
      case 'pricing': return <Pricing onSelectPlan={(p) => p === 'auth' ? setShowAuth(true) : setPage('pricing')} userPlan={user?.plan} token={token || undefined} />;
      default: return <Dashboard token={token} user={user} />;
    }
  };

  const mainNav = navItems.filter((n) => n.group === 'main' || n.group === 'tools');
  const accountNav = navItems.filter((n) => n.group === 'account');

  return (
    <div className="app-layout">
      <aside className={`sidebar ${sidebarOpen ? 'open' : 'collapsed'}`}>
        <div className="sidebar-header">
          <div className="logo" onClick={() => setPage('landing')}>
            ✨ <span className="logo-text">AI Content Gen</span>
          </div>
          <button className="sidebar-toggle" onClick={() => setSidebarOpen(!sidebarOpen)}>
            {sidebarOpen ? '◀' : '▶'}
          </button>
        </div>

        <nav className="sidebar-nav">
          <div className="nav-group">
            {mainNav.map((item) => (
              <button key={item.id} className={`nav-item ${page === item.id ? 'active' : ''}`} onClick={() => setPage(item.id)} title={item.label}>
                <span className="nav-icon">{item.icon}</span>
                {sidebarOpen && <span className="nav-label">{item.label}</span>}
              </button>
            ))}
          </div>
          {sidebarOpen && <div className="nav-divider" />}
          <div className="nav-group">
            {accountNav.map((item) => (
              <button key={item.id} className={`nav-item ${page === item.id ? 'active' : ''}`} onClick={() => setPage(item.id)} title={item.label}>
                <span className="nav-icon">{item.icon}</span>
                {sidebarOpen && <span className="nav-label">{item.label}</span>}
              </button>
            ))}
          </div>
        </nav>

        {sidebarOpen && (
          <div className="sidebar-footer">
            {/* Theme Toggle */}
            <button className="theme-toggle" onClick={() => setDarkMode(!darkMode)} title={darkMode ? 'Chế độ sáng' : 'Chế độ tối'}>
              {darkMode ? '☀️ Sáng' : '🌙 Tối'}
            </button>

            {user ? (
              <>
                <div className="user-info">
                  <div className="user-avatar">{user.name?.[0]?.toUpperCase() || '?'}</div>
                  <div className="user-name">{user.name}</div>
                  <div className="user-email">{user.email}</div>
                </div>
                <div className="plan-badge">{user.plan || 'Miễn Phí'}</div>
                <button className="btn-sidebar-logout" onClick={handleLogout}>Đăng Xuất</button>
              </>
            ) : (
              <>
                <div className="plan-badge">Gói Miễn Phí</div>
                <p>5 lần tạo/ngày</p>
                <button className="btn-sidebar-upgrade" onClick={() => setShowAuth(true)}>Đăng Nhập / Đăng Ký</button>
              </>
            )}
          </div>
        )}
      </aside>

      <main className="main-content">{renderPage()}</main>

      {showAuth && <AuthModal onClose={() => setShowAuth(false)} onAuthSuccess={handleAuthSuccess} />}
      <ToastContainer />
    </div>
  );
}
