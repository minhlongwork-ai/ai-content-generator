/* src/components/Dashboard.tsx — Usage Stats + Quick Actions */
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
    plan: 'Free',
    favoriteType: 'Product Description',
  });
  const [recentItems, setRecentItems] = useState<RecentItem[]>([]);
  const [backendStatus, setBackendStatus] = useState<'online' | 'offline' | 'checking'>('checking');

  useEffect(() => {
    checkBackend();
    // TODO: Load real stats from backend when auth is implemented
    setRecentItems([
      { type: '📝', product: 'Wireless Earbuds Pro', timestamp: '2 min ago' },
      { type: '🔍', product: 'Summer Floral Dress', timestamp: '15 min ago' },
      { type: '🎯', product: 'Smart Fitness Watch', timestamp: '1 hour ago' },
      { type: '🎬', product: 'Organic Skincare Set', timestamp: '3 hours ago' },
    ]);
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
      {/* Welcome */}
      <div className="dashboard-welcome">
        <h1>👋 Welcome back{user?.name ? `, ${user.name}` : ''}!</h1>
        <p>Here's your content generation overview.</p>
      </div>

      {/* Backend Status */}
      <div className={`backend-status ${backendStatus}`}>
        <span className="status-dot" />
        Backend: {backendStatus === 'checking' ? 'Checking...' : backendStatus === 'online' ? 'Online' : 'Offline'}
        {backendStatus === 'offline' && (
          <button className="retry-btn" onClick={checkBackend}>Retry</button>
        )}
      </div>

      {/* Stats Grid */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">⚡</div>
          <div className="stat-value">{stats.todayGenerations}</div>
          <div className="stat-label">Today's Generations</div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-value">{stats.totalGenerations}</div>
          <div className="stat-label">Total Generations</div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">🎯</div>
          <div className="stat-value">{stats.remainingToday}</div>
          <div className="stat-label">Remaining Today</div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">💎</div>
          <div className="stat-value">{stats.plan}</div>
          <div className="stat-label">Current Plan</div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="quick-actions">
        <h2>Quick Actions</h2>
        <div className="actions-grid">
          <button className="action-card" onClick={() => window.dispatchEvent(new CustomEvent('navigate', { detail: 'product' }))}>
            <span className="action-icon">📝</span>
            <span className="action-label">New Product Description</span>
          </button>
          <button className="action-card" onClick={() => window.dispatchEvent(new CustomEvent('navigate', { detail: 'caption' }))}>
            <span className="action-icon">🔍</span>
            <span className="action-label">New Caption & SEO</span>
          </button>
          <button className="action-card" onClick={() => window.dispatchEvent(new CustomEvent('navigate', { detail: 'ad' }))}>
            <span className="action-icon">🎯</span>
            <span className="action-label">New Ad Copy</span>
          </button>
          <button className="action-card" onClick={() => window.dispatchEvent(new CustomEvent('navigate', { detail: 'video' }))}>
            <span className="action-icon">🎬</span>
            <span className="action-label">New Video Script</span>
          </button>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="recent-activity">
        <h2>Recent Activity</h2>
        {recentItems.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📭</div>
            <p>No generations yet. Start creating!</p>
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

      {/* Upgrade CTA */}
      <div className="upgrade-cta">
        <div className="upgrade-content">
          <h3>🚀 Unlock Unlimited Generations</h3>
          <p>Upgrade to Pro for unlimited text generation, video scripts, and API access.</p>
        </div>
        <button
          className="btn-upgrade"
          onClick={() => window.dispatchEvent(new CustomEvent('navigate', { detail: 'pricing' }))}
        >
          View Plans
        </button>
      </div>
    </div>
  );
}
