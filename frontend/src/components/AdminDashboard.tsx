/* src/components/AdminDashboard.tsx — Admin Dashboard with stats & user management */
import { useState, useEffect } from 'react';
import { apiFetch } from '../api';
import { IconUsers, IconZap, IconTrendingUp, IconBarChart, IconShield, IconCheck, IconX, IconSettings } from './Icons';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface AdminStats {
  total_users: number;
  total_generations: number;
  today_generations: number;
  new_users_week: number;
  plan_distribution: { free: number; pro: number; business: number };
}

interface AdminUser {
  id: string;
  email: string;
  name: string;
  plan: string;
  role: string;
  generations_today: number;
  generations_total: number;
  created_at: number;
  last_generation_date: string;
}

export default function AdminDashboard({ token }: { token: string }) {
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const [editingUser, setEditingUser] = useState<string | null>(null);
  const [editRole, setEditRole] = useState('');
  const [editPlan, setEditPlan] = useState('');
  const [activeTab, setActiveTab] = useState<'overview' | 'users'>('overview');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      const [statsRes, usersRes] = await Promise.all([
        apiFetch('/api/admin/stats', { headers: { Authorization: `Bearer ${token}` } }),
        apiFetch('/api/admin/users', { headers: { Authorization: `Bearer ${token}` } }),
      ]);
      setStats(statsRes);
      setUsers(usersRes.users || []);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch admin data');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateUser = async (email: string) => {
    try {
      const body: any = {};
      if (editRole) body.role = editRole;
      if (editPlan) body.plan = editPlan;
      
      await fetch(`${API_URL}/api/admin/users/${encodeURIComponent(email)}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify(body),
      });
      setEditingUser(null);
      fetchData();
    } catch (err: any) {
      alert('Error updating user: ' + err.message);
    }
  };

  const handleDeleteUser = async (email: string) => {
    if (!confirm(`Bạn có chắc muốn xóa user ${email}?`)) return;
    try {
      await fetch(`${API_URL}/api/admin/users/${encodeURIComponent(email)}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchData();
    } catch (err: any) {
      alert('Error deleting user: ' + err.message);
    }
  };

  const filteredUsers = users.filter(u => 
    u.email.toLowerCase().includes(search.toLowerCase()) ||
    u.name.toLowerCase().includes(search.toLowerCase())
  );

  const formatDate = (timestamp: number) => {
    if (!timestamp) return '—';
    return new Date(timestamp * 1000).toLocaleDateString('vi-VN');
  };

  if (loading) {
    return (
      <div className="admin-dashboard">
        <div className="loading-state">
          <div className="loading-spinner" />
          <p>Đang tải dữ liệu admin...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="admin-dashboard">
        <div className="error-state">
          <span className="error-icon">⚠️</span>
          <p>{error}</p>
          <button className="btn btn-primary" onClick={fetchData}>Thử lại</button>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-dashboard">
      {/* Header */}
      <div className="admin-header">
        <div className="admin-header-left">
          <div className="admin-badge">
            <IconShield size={16} />
            <span>Admin Panel</span>
          </div>
          <h1>Dashboard Quản Trị</h1>
          <p>Tổng quan hệ thống và quản lý người dùng</p>
        </div>
        <button className="btn-refresh" onClick={fetchData}>🔄 Làm mới</button>
      </div>

      {/* Tabs */}
      <div className="admin-tabs">
        <button className={`admin-tab ${activeTab === 'overview' ? 'active' : ''}`} onClick={() => setActiveTab('overview')}>
          <IconBarChart size={16} /> Tổng quan
        </button>
        <button className={`admin-tab ${activeTab === 'users' ? 'active' : ''}`} onClick={() => setActiveTab('users')}>
          <IconUsers size={16} /> Quản lý User ({users.length})
        </button>
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && stats && (
        <div className="admin-overview">
          {/* Stats Grid */}
          <div className="admin-stats-grid">
            <div className="admin-stat-card">
              <div className="admin-stat-icon blue">
                <IconUsers size={24} />
              </div>
              <div className="admin-stat-info">
                <span className="admin-stat-value">{stats.total_users}</span>
                <span className="admin-stat-label">Tổng người dùng</span>
              </div>
            </div>
            <div className="admin-stat-card">
              <div className="admin-stat-icon purple">
                <IconZap size={24} />
              </div>
              <div className="admin-stat-info">
                <span className="admin-stat-value">{stats.total_generations.toLocaleString()}</span>
                <span className="admin-stat-label">Tổng lần tạo</span>
              </div>
            </div>
            <div className="admin-stat-card">
              <div className="admin-stat-icon green">
                <IconTrendingUp size={24} />
              </div>
              <div className="admin-stat-info">
                <span className="admin-stat-value">{stats.today_generations}</span>
                <span className="admin-stat-label">Tạo hôm nay</span>
              </div>
            </div>
            <div className="admin-stat-card">
              <div className="admin-stat-icon orange">
                <IconBarChart size={24} />
              </div>
              <div className="admin-stat-info">
                <span className="admin-stat-value">{stats.new_users_week}</span>
                <span className="admin-stat-label">User mới 7 ngày</span>
              </div>
            </div>
          </div>

          {/* Plan Distribution */}
          <div className="admin-card">
            <h3><IconSettings size={18} /> Phân bố gói</h3>
            <div className="plan-distribution">
              <div className="plan-bar">
                <div className="plan-bar-fill free" style={{ width: `${stats.total_users ? (stats.plan_distribution.free / stats.total_users) * 100 : 0}%` }} />
              </div>
              <div className="plan-legend">
                <div className="plan-legend-item">
                  <span className="dot free" />
                  <span>Miễn phí: {stats.plan_distribution.free}</span>
                </div>
                <div className="plan-legend-item">
                  <span className="dot pro" />
                  <span>Pro: {stats.plan_distribution.pro}</span>
                </div>
                <div className="plan-legend-item">
                  <span className="dot business" />
                  <span>Doanh nghiệp: {stats.plan_distribution.business}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Users Tab */}
      {activeTab === 'users' && (
        <div className="admin-users">
          <div className="admin-card">
            <div className="admin-card-header">
              <h3>Danh sách người dùng ({filteredUsers.length})</h3>
              <input
                type="text"
                className="admin-search"
                placeholder="Tìm kiếm email, tên..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>

            <div className="admin-table-wrapper">
              <table className="admin-table">
                <thead>
                  <tr>
                    <th>Người dùng</th>
                    <th>Vai trò</th>
                    <th>Gói</th>
                    <th>Tạo hôm nay</th>
                    <th>Tổng tạo</th>
                    <th>Ngày đăng ký</th>
                    <th>Hành động</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredUsers.map((user) => (
                    <tr key={user.id}>
                      <td>
                        <div className="user-cell">
                          <div className="user-cell-avatar">{user.name?.[0]?.toUpperCase() || '?'}</div>
                          <div>
                            <div className="user-cell-name">{user.name}</div>
                            <div className="user-cell-email">{user.email}</div>
                          </div>
                        </div>
                      </td>
                      <td>
                        {editingUser === user.email ? (
                          <select value={editRole} onChange={(e) => setEditRole(e.target.value)} className="admin-select">
                            <option value="user">User</option>
                            <option value="admin">Admin</option>
                          </select>
                        ) : (
                          <span className={`role-badge ${user.role}`}>{user.role}</span>
                        )}
                      </td>
                      <td>
                        {editingUser === user.email ? (
                          <select value={editPlan} onChange={(e) => setEditPlan(e.target.value)} className="admin-select">
                            <option value="free">Free</option>
                            <option value="pro">Pro</option>
                            <option value="business">Business</option>
                          </select>
                        ) : (
                          <span className={`plan-badge ${user.plan}`}>{user.plan}</span>
                        )}
                      </td>
                      <td>{user.generations_today}</td>
                      <td>{user.generations_total}</td>
                      <td>{formatDate(user.created_at)}</td>
                      <td>
                        {editingUser === user.email ? (
                          <div className="action-btns">
                            <button className="btn-save" onClick={() => handleUpdateUser(user.email)}>
                              <IconCheck size={14} /> Lưu
                            </button>
                            <button className="btn-cancel" onClick={() => setEditingUser(null)}>
                              <IconX size={14} /> Hủy
                            </button>
                          </div>
                        ) : (
                          <div className="action-btns">
                            <button className="btn-edit" onClick={() => {
                              setEditingUser(user.email);
                              setEditRole(user.role);
                              setEditPlan(user.plan);
                            }}>
                              ✏️ Sửa
                            </button>
                            {user.role !== 'admin' && (
                              <button className="btn-delete" onClick={() => handleDeleteUser(user.email)}>
                                🗑️ Xóa
                              </button>
                            )}
                          </div>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
