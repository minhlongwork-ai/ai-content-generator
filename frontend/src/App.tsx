/* src/App.tsx — Main App with Sidebar + Auth + Routing + Admin + User Profile */
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
import AdminDashboard from './components/AdminDashboard';
import UserProfile from './components/UserProfile';
import GenerationHistory from './components/GenerationHistory';
import SkillMarketplace from './components/SkillMarketplace';
import { ToastContainer } from './components/Toast';
import { IconSparkles, IconFileText, IconSearch, IconTarget, IconVideo, IconSettings, IconLogOut, IconBarChart, IconShield, IconUsers as IconUser } from './components/Icons';
import './App.css';

type Page = 'landing' | 'dashboard' | 'product' | 'caption' | 'ad' | 'video' | 'settings' | 'pricing' | 'admin' | 'profile' | 'history' | 'marketplace';

const navItems: { id: Page; label: string; icon: React.ReactNode; group: string; adminOnly?: boolean }[] = [
  { id: 'dashboard', label: 'Tổng Quan', icon: <IconBarChart size={18} />, group: 'main' },
  { id: 'product', label: 'Mô Tả SP', icon: <IconFileText size={18} />, group: 'tools' },
  { id: 'caption', label: 'Caption & SEO', icon: <IconSearch size={18} />, group: 'tools' },
  { id: 'ad', label: 'Quảng Cáo', icon: <IconTarget size={18} />, group: 'tools' },
  { id: 'video', label: 'Video AI', icon: <IconVideo size={18} />, group: 'tools' },
  { id: 'history', label: 'Lịch Sử', icon: <IconBarChart size={18} />, group: 'tools' },
  { id: 'marketplace', label: 'Marketplace', icon: <IconSparkles size={18} />, group: 'tools' },
  { id: 'admin', label: 'Admin', icon: <IconShield size={18} />, group: 'admin', adminOnly: true },
  { id: 'pricing', label: 'Bảng Giá', icon: <IconSparkles size={18} />, group: 'account' },
  { id: 'profile', label: 'Hồ Sơ', icon: <IconUser size={18} />, group: 'account' },
  { id: 'settings', label: 'Cài Đặt', icon: <IconSettings size={18} />, group: 'account' },
];

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function App() {
  const [page, setPage] = useState<Page>('landing');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [user, setUser] = useState<any>(null);
  const [showAuth, setShowAuth] = useState(false);
  const [authMode, setAuthMode] = useState<'login' | 'register'>('register');
  const [darkMode, setDarkMode] = useState(true);

  const isLanding = page === 'landing';
  const isAdmin = user?.role === 'admin';

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
      case 'landing': return <Landing onGetStarted={() => { setAuthMode('register'); token ? setPage('dashboard') : setShowAuth(true); }} onLogin={() => { setAuthMode('login'); setShowAuth(true); }} onViewPricing={() => setPage('pricing')} />;
      case 'dashboard': return <Dashboard token={token} user={user} />;
      case 'product': return <ProductDescription token={token} />;
      case 'caption': return <CaptionSEO token={token} />;
      case 'ad': return <AdCopy token={token} />;
      case 'video': return <VideoScript token={token} />;
      case 'settings': return <Settings token={token} user={user} onLogout={handleLogout} />;
      case 'pricing': return <Pricing onSelectPlan={(p) => p === 'auth' ? setShowAuth(true) : setPage('pricing')} userPlan={user?.plan} token={token || undefined} />;
      case 'admin': return isAdmin ? <AdminDashboard token={token || ''} /> : <Dashboard token={token} user={user} />;
      case 'profile': return <UserProfile token={token || ''} user={user} onLogout={handleLogout} />;
      case 'history': return <GenerationHistory token={token} limit={30} />;
      case 'marketplace': return <SkillMarketplace token={token} />;
      default: return <Dashboard token={token} user={user} />;
    }
  };

  const mainNav = navItems.filter((n) => (n.group === 'main' || n.group === 'tools') && (!n.adminOnly || isAdmin));
  const adminNav = navItems.filter((n) => n.group === 'admin' && n.adminOnly && isAdmin);
  const accountNav = navItems.filter((n) => n.group === 'account');

  // Landing page has its own nav, no sidebar needed
  if (isLanding) {
    return (
      <div className="app-landing">
        <main className="main-content-full">{renderPage()}</main>
        {showAuth && <AuthModal onClose={() => setShowAuth(false)} onAuthSuccess={handleAuthSuccess} initialMode={authMode} />}
        <ToastContainer />
      </div>
    );
  }

  return (
    <div className="app-layout">
      <aside className={`sidebar ${sidebarOpen ? 'open' : 'collapsed'}`}>
        <div className="sidebar-header">
          <div className="logo" onClick={() => setPage('landing')}>
            <div className="logo-icon">
              <IconSparkles size={20} />
            </div>
            {sidebarOpen && <span className="logo-text">AI Content Gen</span>}
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

          {adminNav.length > 0 && (
            <>
              {sidebarOpen && <div className="nav-divider" />}
              <div className="nav-group">
                <div className="nav-section-label">Quản trị</div>
                {adminNav.map((item) => (
                  <button key={item.id} className={`nav-item admin-nav-item ${page === item.id ? 'active' : ''}`} onClick={() => setPage(item.id)} title={item.label}>
                    <span className="nav-icon">{item.icon}</span>
                    {sidebarOpen && <span className="nav-label">{item.label}</span>}
                  </button>
                ))}
              </div>
            </>
          )}

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
            <button className="theme-toggle" onClick={() => setDarkMode(!darkMode)}>
              {darkMode ? '☀️ Sáng' : '🌙 Tối'}
            </button>

            {user ? (
              <>
                <div className="user-info">
                  <div className="user-avatar">
                    {user.role === 'admin' && <IconShield size={14} />}
                    {user.role !== 'admin' && (user.name?.[0]?.toUpperCase() || '?')}
                  </div>
                  <div className="user-name">{user.name}</div>
                  <div className="user-email">{user.email}</div>
                </div>
                <div className="plan-badge">{user.plan || 'Miễn Phí'}</div>
                <button className="btn-sidebar-logout" onClick={handleLogout}>
                  <IconLogOut size={14} />
                  <span>Đăng Xuất</span>
                </button>
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

      <main className="main-content">
        <div className="content-wrapper">
          {renderPage()}
        </div>
      </main>

      {showAuth && <AuthModal onClose={() => setShowAuth(false)} onAuthSuccess={handleAuthSuccess} />}
      <ToastContainer />
    </div>
  );
}
