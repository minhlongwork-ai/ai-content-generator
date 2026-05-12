/* src/components/Dashboard.tsx — Professional Dashboard with better visuals */
import { useState, useEffect } from 'react';
import { IconZap, IconBarChart, IconTarget, IconTrendingUp, IconFileText, IconSearch, IconTarget as IconTarget2, IconVideo, IconClock } from './Icons';

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
    { type: 'product', product: 'Tai Nghe Không Dây Pro', timestamp: '2 phút trước' },
    { type: 'caption', product: 'Váy Hoa Mùa Hè', timestamp: '15 phút trước' },
    { type: 'ad', product: 'Đồng Hồ Thông Minh', timestamp: '1 giờ trước' },
    { type: 'video', product: 'Bộ Dưỡng Da Hữu Cơ', timestamp: '3 giờ trước' },
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

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'product': return <IconFileText size={16} />;
      case 'caption': return <IconSearch size={16} />;
      case 'ad': return <IconTarget2 size={16} />;
      case 'video': return <IconVideo size={16} />;
      default: return <IconFileText size={16} />;
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'product': return 'purple';
      case 'caption': return 'blue';
      case 'ad': return 'red';
      case 'video': return 'green';
      default: return 'purple';
    }
  };

  const quickActions = [
    { id: 'product', label: 'Tạo Mô Tả SP', icon: <IconFileText size={24} />, color: 'purple', desc: 'Mô tả sản phẩm chuyên nghiệp' },
    { id: 'caption', label: 'Tạo Caption SEO', icon: <IconSearch size={24} />, color: 'blue', desc: 'Caption & hashtag tối ưu' },
    { id: 'ad', label: 'Tạo Quảng Cáo', icon: <IconTarget2 size={24} />, color: 'red', desc: '3 phiên bản quảng cáo' },
    { id: 'video', label: 'Tạo Kịch Bản', icon: <IconVideo size={24} />, color: 'green', desc: 'Kịch bản video + TTS' },
  ];

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
          <span>{backendStatus === 'checking' ? 'Đang kiểm tra...' : backendStatus === 'online' ? 'Backend Online' : 'Backend Offline'}</span>
          {backendStatus === 'offline' && <button className="retry-btn" onClick={checkBackend}>Thử lại</button>}
        </div>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-card-icon purple">
            <IconZap size={22} />
          </div>
          <div className="stat-card-value">{stats.todayGenerations}</div>
          <div className="stat-card-label">Tạo Hôm Nay</div>
        </div>
        <div className="stat-card">
          <div className="stat-card-icon blue">
            <IconBarChart size={22} />
          </div>
          <div className="stat-card-value">{stats.totalGenerations}</div>
          <div className="stat-card-label">Tổng Số Đã Tạo</div>
        </div>
        <div className="stat-card">
          <div className="stat-card-icon green">
            <IconTarget size={22} />
          </div>
          <div className="stat-card-value">{stats.remainingToday}</div>
          <div className="stat-card-label">Còn Lại Hôm Nay</div>
        </div>
        <div className="stat-card">
          <div className="stat-card-icon orange">
            <IconTrendingUp size={22} />
          </div>
          <div className="stat-card-value">{stats.plan}</div>
          <div className="stat-card-label">Gói Hiện Tại</div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="quick-actions">
        <div className="section-header-small">
          <h2>Hành Động Nhanh</h2>
          <p>Chọn loại nội dung bạn muốn tạo</p>
        </div>
        <div className="actions-grid">
          {quickActions.map((action) => (
            <button
              key={action.id}
              className="action-card"
              onClick={() => window.dispatchEvent(new CustomEvent('navigate', { detail: action.id }))}
            >
              <div className={`action-icon-wrap ${action.color}`}>
                {action.icon}
              </div>
              <div className="action-content">
                <span className="action-label">{action.label}</span>
                <span className="action-desc">{action.desc}</span>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Recent Activity */}
      <div className="recent-activity">
        <div className="section-header-small">
          <h2>Hoạt Động Gần Đây</h2>
        </div>
        {recentItems.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">
              <IconFileText size={32} />
            </div>
            <p>Chưa có nội dung nào. Bắt đầu tạo!</p>
          </div>
        ) : (
          <div className="activity-list">
            {recentItems.map((item, i) => (
              <div key={i} className="activity-item">
                <div className={`activity-icon ${getTypeColor(item.type)}`}>
                  {getTypeIcon(item.type)}
                </div>
                <div className="activity-info">
                  <span className="activity-product">{item.product}</span>
                  <span className="activity-time"><IconClock size={12} /> {item.timestamp}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Upgrade CTA */}
      <div className="upgrade-cta">
        <div className="upgrade-icon">
          <IconTrendingUp size={28} />
        </div>
        <div className="upgrade-content">
          <h3>Mở Khóa Tạo Không Giới Hạn</h3>
          <p>Nâng cấp Pro để tạo nội dung không giới hạn, kịch bản video, và truy cập API.</p>
        </div>
        <button className="btn-upgrade" onClick={() => window.dispatchEvent(new CustomEvent('navigate', { detail: 'pricing' }))}>
          Xem Gói
        </button>
      </div>
    </div>
  );
}
