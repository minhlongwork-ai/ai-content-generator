/* src/components/UserProfile.tsx — User Profile & Usage Stats */
import { useState, useEffect } from 'react';
import { apiFetch } from '../api';
import { IconUsers as IconUser, IconMic as IconMail, IconClock as IconCalendar, IconZap, IconBarChart, IconTarget, IconSettings } from './Icons';

interface UserProfileData {
  user: {
    id: string;
    email: string;
    name: string;
    plan: string;
    role?: string;
  };
  stats: {
    today: number;
    total: number;
    remaining: number;
    plan: string;
  };
}

interface ProfileProps {
  token: string;
  user: any;
  onLogout: () => void;
}

export default function UserProfile({ token, onLogout }: ProfileProps) {
  const [profile, setProfile] = useState<UserProfileData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [editing, setEditing] = useState(false);
  const [newName, setNewName] = useState('');
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    setLoading(true);
    try {
      const data = await apiFetch('/api/auth/me', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setProfile(data);
      setNewName(data.user?.name || '');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveName = async () => {
    setSaving(true);
    try {
      // Note: Backend doesn't have update profile endpoint yet, this is a placeholder
      setEditing(false);
      fetchProfile();
    } catch (err: any) {
      alert('Error: ' + err.message);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="tool-page">
        <div className="loading-state">
          <div className="loading-spinner" />
          <p>Đang tải hồ sơ...</p>
        </div>
      </div>
    );
  }

  if (error || !profile) {
    return (
      <div className="tool-page">
        <div className="error-state">
          <span className="error-icon">⚠️</span>
          <p>{error || 'Không thể tải hồ sơ'}</p>
        </div>
      </div>
    );
  }

  const planLimits: Record<string, string> = {
    free: '5 lần/ngày',
    pro: 'Không giới hạn',
    business: 'Không giới hạn',
  };

  const planColors: Record<string, string> = {
    free: 'gray',
    pro: 'purple',
    business: 'orange',
  };

  return (
    <div className="tool-page">
      <div className="tool-header">
        <div className="tool-header-icon blue">
          <IconUser size={24} />
        </div>
        <div>
          <h1>Hồ Sơ Của Tôi</h1>
          <p>Thông tin tài khoản và thống kê sử dụng</p>
        </div>
      </div>

      <div className="profile-grid">
        {/* Profile Card */}
        <div className="profile-card">
          <div className="profile-card-header">
            <div className="profile-avatar-large">
              {profile.user.name?.[0]?.toUpperCase() || '?'}
            </div>
            <div className="profile-info">
              {editing ? (
                <div className="profile-edit-name">
                  <input
                    type="text"
                    value={newName}
                    onChange={(e) => setNewName(e.target.value)}
                    placeholder="Tên của bạn"
                  />
                  <div className="profile-edit-actions">
                    <button className="btn-save-sm" onClick={handleSaveName} disabled={saving}>
                      {saving ? '⏳...' : '✓ Lưu'}
                    </button>
                    <button className="btn-cancel-sm" onClick={() => { setEditing(false); setNewName(profile.user.name); }}>
                      ✕ Hủy
                    </button>
                  </div>
                </div>
              ) : (
                <>
                  <h2>{profile.user.name}</h2>
                  <button className="btn-edit-sm" onClick={() => setEditing(true)}>✏️ Sửa tên</button>
                </>
              )}
            </div>
          </div>

          <div className="profile-details">
            <div className="profile-detail-row">
              <div className="profile-detail-icon">
                <IconMail size={16} />
              </div>
              <div>
                <span className="profile-detail-label">Email</span>
                <span className="profile-detail-value">{profile.user.email}</span>
              </div>
            </div>
            <div className="profile-detail-row">
              <div className="profile-detail-icon">
                <IconSettings size={16} />
              </div>
              <div>
                <span className="profile-detail-label">Vai trò</span>
                <span className={`role-badge ${profile.user.role || 'user'}`}>
                  {profile.user.role === 'admin' ? 'Quản trị viên' : 'Người dùng'}
                </span>
              </div>
            </div>
            <div className="profile-detail-row">
              <div className="profile-detail-icon">
                <IconCalendar size={16} />
              </div>
              <div>
                <span className="profile-detail-label">ID</span>
                <span className="profile-detail-value">{profile.user.id}</span>
              </div>
            </div>
          </div>

          <button className="btn-logout-profile" onClick={onLogout}>
            🚪 Đăng xuất
          </button>
        </div>

        {/* Stats Card */}
        <div className="profile-stats-card">
          <div className="profile-plan-section">
            <div className={`plan-badge-large ${planColors[profile.stats.plan]}`}>
              {profile.stats.plan === 'free' ? '🆓 Miễn Phí' : profile.stats.plan === 'pro' ? '⚡ Pro' : '🏢 Doanh Nghiệp'}
            </div>
            <p className="plan-limit">Giới hạn: {planLimits[profile.stats.plan] || '5 lần/ngày'}</p>
          </div>

          <div className="profile-stats-grid">
            <div className="profile-stat">
              <div className="profile-stat-icon purple">
                <IconZap size={20} />
              </div>
              <span className="profile-stat-value">{profile.stats.today}</span>
              <span className="profile-stat-label">Tạo hôm nay</span>
            </div>
            <div className="profile-stat">
              <div className="profile-stat-icon blue">
                <IconBarChart size={20} />
              </div>
              <span className="profile-stat-value">{profile.stats.total}</span>
              <span className="profile-stat-label">Tổng đã tạo</span>
            </div>
            <div className="profile-stat">
              <div className="profile-stat-icon green">
                <IconTarget size={20} />
              </div>
              <span className="profile-stat-value">{profile.stats.remaining === Infinity ? '∞' : profile.stats.remaining}</span>
              <span className="profile-stat-label">Còn lại hôm nay</span>
            </div>
          </div>

          {/* Usage bar for free plan */}
          {profile.stats.plan === 'free' && (
            <div className="usage-bar-section">
              <div className="usage-bar-label">
                <span>Đã dùng {profile.stats.today}/5</span>
                <span>{Math.round((profile.stats.today / 5) * 100)}%</span>
              </div>
              <div className="usage-bar">
                <div className="usage-bar-fill" style={{ width: `${Math.min(100, (profile.stats.today / 5) * 100)}%` }} />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
