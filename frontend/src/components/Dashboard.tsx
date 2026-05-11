/* src/components/Dashboard.tsx — Thống kê + Hành động nhanh (Tiếng Việt) */
import { useState, useEffect } from 'react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface DashboardStats {
  totalGenerations: number;
  todayGenerations: number;
  remainingToday: number;
  plan: string;
  favoriteType: string;
}

interface RecentItem {
  type: string;
  product: string;
  timestamp: string;
}

interface DashboardProps {
  token?: string | null;
  user?: any;
}

export default function Dashboard({ user }: DashboardProps) {
  const [stats] = useState<DashboardStats>({
    totalGenerations: 0,
    todayGenerations: 0,
    remainingToday: 5,
    plan: 'Miễn Phí',
    favoriteType: 'Mô Tả Sản Phẩm',
  });
  const [recentItems] = useState<RecentItem[]>([
    { type: '📝', product: 'Tai Nghe Không Dây Pro', timestamp: '2 phút trước' },
    { type: '🔍', product: 'Váy Hoa Mùa Hè', timestamp: '15 phút trước' },
    { type: '🎯', product: 'Đồng Hồ Thông Minh', timestamp: '1 giờ trước' },
    { type: '🎬', product: 'Bộ Dưỡng Da Hữu Cơ', timestamp: '3 giờ trước' },
  ]);
  const [backendStatus, setBackendStatus] = useState<'online' | 'offline' | 'checking'>('checking');

  useEffect(() => {
    checkBackend();
  }, []);

  const checkBackend = async () => {
    try {
      const res = await fetch(`${API_URL}/api/health`, { signal: AbortSignal.timeout(3000) });
      setBackendStatus(res.ok ? 'online' : 'offline');
    } catch {
      setBackendStatus('offline');
    }
  };

  return (
    <div className="dashboard">
      <div className="dashboard-welcome">
        <h1>👋 Chào mừng quay lại{user?.name ? `, ${user.name}` : ''}!</h1>
        <p>Đây là tổng quan tạo nội dung của bạn.</p>
      </div>

      <div className={`backend-status ${backendStatus}`}>
        <span className="status-dot" />
        Backend: {backendStatus === 'checking' ? 'Đang kiểm tra...' : backendStatus === 'online' ? 'Online' : 'Offline'}
        {backendStatus === 'offline' && <button className="retry-btn" onClick={checkBackend}>Thử lại</button>}
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">⚡</div>
          <div className="stat-value">{stats.todayGenerations}</div>
          <div className="stat-label">Tạo Hôm Nay</div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-value">{stats.totalGenerations}</div>
          <div className="stat-label">Tổng Số Đã Tạo</div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">🎯</div>
          <div className="stat-value">{stats.remainingToday}</div>
          <div className="stat-label">Còn Lại Hôm Nay</div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">💎</div>
          <div className="stat-value">{stats.plan}</div>
          <div className="stat-label">Gói Hiện Tại</div>
        </div>
      </div>

      <div className="quick-actions">
        <h2>Hành Động Nhanh</h2>
        <div className="actions-grid">
          <button className="action-card" onClick={() => window.dispatchEvent(new CustomEvent('navigate', { detail: 'product' }))}>
            <span className="action-icon">📝</span>
            <span className="action-label">Tạo Mô Tả SP</span>
          </button>
          <button className="action-card" onClick={() => window.dispatchEvent(new CustomEvent('navigate', { detail: 'caption' }))}>
            <span className="action-icon">🔍</span>
            <span className="action-label">Tạo Caption SEO</span>
          </button>
          <button className="action-card" onClick={() => window.dispatchEvent(new CustomEvent('navigate', { detail: 'ad' }))}>
            <span className="action-icon">🎯</span>
            <span className="action-label">Tạo Quảng Cáo</span>
          </button>
          <button className="action-card" onClick={() => window.dispatchEvent(new CustomEvent('navigate', { detail: 'video' }))}>
            <span className="action-icon">🎬</span>
            <span className="action-label">Tạo Kịch Bản</span>
          </button>
        </div>
      </div>

      <div className="recent-activity">
        <h2>Hoạt Động Gần Đây</h2>
        {recentItems.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📭</div>
            <p>Chưa có nội dung nào. Bắt đầu tạo!</p>
          </div>
        ) : (
          <div className="activity-list">
            {recentItems.map((item, i) => (
              <div key={i} className="activity-item">
                <span className="activity-type">{item.type}</span>
                <span className="activity-product">{item.product}</span>
                <span className="activity-time">{item.timestamp}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="upgrade-cta">
        <div className="upgrade-content">
          <h3>🚀 Mở Khóa Tạo Không Giới Hạn</h3>
          <p>Nâng cấp Pro để tạo nội dung không giới hạn, kịch bản video, và truy cập API.</p>
        </div>
        <button className="btn-upgrade" onClick={() => window.dispatchEvent(new CustomEvent('navigate', { detail: 'pricing' }))}>
          Xem Gói
        </button>
      </div>
    </div>
  );
}
