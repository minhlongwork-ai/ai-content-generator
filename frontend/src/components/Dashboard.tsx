/* src/components/Dashboard.tsx — Dashboard với real stats + GenerationHistory */
import { useState, useEffect } from 'react';
import { IconZap, IconBarChart, IconTarget, IconTrendingUp, IconFileText, IconSearch, IconTarget as IconTarget2, IconVideo } from './Icons';
import GenerationHistory from './GenerationHistory';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface DashboardStats {
  totalGenerations: number;
  todayGenerations: number;
  remainingToday: number;
  plan: string;
  favoriteType: string;
}

interface DashboardProps {
  token?: string | null;
  user?: any;
}

export default function Dashboard({ token, user }: DashboardProps) {
  const [stats, setStats] = useState<DashboardStats>({
    totalGenerations: 0,
    todayGenerations: 0,
    remainingToday: 5,
    plan: 'Miễn Phí',
    favoriteType: '—',
  });
  const [backendStatus, setBackendStatus] = useState<'online' | 'offline' | 'checking'>('checking');
  const [activeTab, setActiveTab] = useState<'overview' | 'history'>('overview');

  useEffect(() => {
    checkBackend();
    if (token) fetchStats();
  }, [token]);

  const checkBackend = async () => {
    try {
      const res = await fetch(`${API_URL}/api/health`, { signal: AbortSignal.timeout(3000) });
      setBackendStatus(res.ok ? 'online' : 'offline');
    } catch {
      setBackendStatus('offline');
    }
  };

  const fetchStats = async () => {
    try {
      // Thử lấy analytics từ skill system
      const res = await fetch(`${API_URL}/api/skills/analytics`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        const data = await res.json();
        setStats({
          totalGenerations: data.total_generations ?? 0,
          todayGenerations: data.today_generations ?? 0,
          remainingToday: data.remaining_today ?? 5,
          plan: user?.plan || 'Miễn Phí',
          favoriteType: data.favorite_skill ?? '—',
        });
      } else {
        // Fallback: dùng user info từ auth
        setStats(prev => ({ ...prev, plan: user?.plan || 'Miễn Phí' }));
      }
    } catch {
      // Backend offline — dùng defaults
      setStats(prev => ({ ...prev, plan: user?.plan || 'Miễn Phí' }));
    }
  };

  const quickActions = [
    { id: 'product', label: 'Tạo Mô Tả SP', icon: <IconFileText size={24} />, color: 'purple', desc: 'Mô tả sản phẩm chuyên nghiệp' },
    { id: 'caption', label: 'Tạo Caption SEO', icon: <IconSearch size={24} />, color: 'blue', desc: 'Caption & hashtag tối ưu' },
    { id: 'ad', label: 'Tạo Quảng Cáo', icon: <IconTarget2 size={24} />, color: 'red', desc: '3 phiên bản quảng cáo' },
    { id: 'video', label: 'Tạo Kịch Bản', icon: <IconVideo size={24} />, color: 'green', desc: 'Kịch bản video + TTS' },
  ];

  const navigate = (id: string) =>
    window.dispatchEvent(new CustomEvent('navigate', { detail: id }));

  return (
    <div className="dashboard">
      {/* Welcome */}
      <div className="dashboard-welcome">
        <div className="welcome-content">
          <h1>Chào mừng quay lại{user?.name ? `, ${user.name}` : ''}! 👋</h1>
          <p>Đây là tổng quan tạo nội dung của bạn hôm nay.</p>
        </div>
        <div className={`backend-status ${backendStatus}`}>
          <span className="status-dot" />
          <span>
            {backendStatus === 'checking'
              ? 'Đang kiểm tra...'
              : backendStatus === 'online'
              ? 'Backend Online'
              : 'Backend Offline'}
          </span>
          {backendStatus === 'offline' && (
            <button className="retry-btn" onClick={checkBackend}>Thử lại</button>
          )}
        </div>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-card-icon purple"><IconZap size={22} /></div>
          <div className="stat-card-value">{stats.todayGenerations}</div>
          <div className="stat-card-label">Tạo Hôm Nay</div>
        </div>
        <div className="stat-card">
          <div className="stat-card-icon blue"><IconBarChart size={22} /></div>
          <div className="stat-card-value">{stats.totalGenerations}</div>
          <div className="stat-card-label">Tổng Số Đã Tạo</div>
        </div>
        <div className="stat-card">
          <div className="stat-card-icon green"><IconTarget size={22} /></div>
          <div className="stat-card-value">{stats.remainingToday}</div>
          <div className="stat-card-label">Còn Lại Hôm Nay</div>
        </div>
        <div className="stat-card">
          <div className="stat-card-icon orange"><IconTrendingUp size={22} /></div>
          <div className="stat-card-value">{stats.plan}</div>
          <div className="stat-card-label">Gói Hiện Tại</div>
        </div>
      </div>

      {/* Tabs: Overview | History */}
      <div className="dashboard-tabs">
        <button
          className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Hành Động Nhanh
        </button>
        <button
          className={`tab-btn ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          Lịch Sử Gần Đây
        </button>
      </div>

      {activeTab === 'overview' && (
        <>
          {/* Quick Actions */}
          <div className="quick-actions">
            <div className="actions-grid">
              {quickActions.map((action) => (
                <button
                  key={action.id}
                  className="action-card"
                  onClick={() => navigate(action.id)}
                >
                  <div className={`action-icon-wrap ${action.color}`}>{action.icon}</div>
                  <div className="action-content">
                    <span className="action-label">{action.label}</span>
                    <span className="action-desc">{action.desc}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Recent History (compact) */}
          <div className="recent-activity">
            <div className="section-header-small">
              <h2>Hoạt Động Gần Đây</h2>
              {token && (
                <button className="btn-link" onClick={() => setActiveTab('history')}>
                  Xem tất cả →
                </button>
              )}
            </div>
            <GenerationHistory token={token} limit={5} compact={true} />
          </div>
        </>
      )}

      {activeTab === 'history' && (
        <GenerationHistory token={token} limit={20} compact={false} />
      )}

      {/* Upgrade CTA */}
      {(!user?.plan || user?.plan === 'free' || user?.plan === 'Miễn Phí') && (
        <div className="upgrade-cta">
          <div className="upgrade-icon"><IconTrendingUp size={28} /></div>
          <div className="upgrade-content">
            <h3>Mở Khóa Tạo Không Giới Hạn</h3>
            <p>Nâng cấp Pro để tạo nội dung không giới hạn, kịch bản video, và truy cập API.</p>
          </div>
          <button className="btn-upgrade" onClick={() => navigate('pricing')}>
            Xem Gói
          </button>
        </div>
      )}
    </div>
  );
}
