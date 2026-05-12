/* src/components/GenerationHistory.tsx — Lịch sử tạo nội dung */
import { useState, useEffect } from 'react';
import { IconFileText, IconSearch, IconTarget, IconVideo, IconClock, IconSparkles, IconCopy, IconCheck } from './Icons';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface Generation {
  id: string;
  skill_name: string;
  content_type: string;
  input_data: Record<string, string>;
  output_content: Record<string, unknown>;
  quality_score: number;
  created_at: string;
}

interface GenerationHistoryProps {
  token?: string | null;
  limit?: number;        // bao nhiêu item hiển thị (default 10)
  compact?: boolean;     // dùng trong Dashboard
  onSelect?: (gen: Generation) => void;
}

function typeIcon(skill: string) {
  if (skill.includes('product')) return <IconFileText size={16} />;
  if (skill.includes('caption')) return <IconSearch size={16} />;
  if (skill.includes('ad')) return <IconTarget size={16} />;
  if (skill.includes('video')) return <IconVideo size={16} />;
  return <IconSparkles size={16} />;
}

function typeColor(skill: string) {
  if (skill.includes('product')) return 'purple';
  if (skill.includes('caption')) return 'blue';
  if (skill.includes('ad')) return 'red';
  if (skill.includes('video')) return 'green';
  return 'purple';
}

function typeName(skill: string) {
  if (skill.includes('product')) return 'Mô Tả SP';
  if (skill.includes('caption')) return 'Caption SEO';
  if (skill.includes('ad')) return 'Quảng Cáo';
  if (skill.includes('video')) return 'Kịch Bản';
  return skill;
}

function scoreColor(score: number) {
  if (score >= 80) return 'green';
  if (score >= 60) return 'yellow';
  return 'red';
}

function timeAgo(dateStr: string) {
  const date = new Date(dateStr);
  const diff = Math.floor((Date.now() - date.getTime()) / 1000);
  if (diff < 60) return `${diff} giây trước`;
  if (diff < 3600) return `${Math.floor(diff / 60)} phút trước`;
  if (diff < 86400) return `${Math.floor(diff / 3600)} giờ trước`;
  return `${Math.floor(diff / 86400)} ngày trước`;
}

function getPreview(gen: Generation): string {
  const o = gen.output_content;
  if (typeof o?.headline === 'string') return o.headline as string;
  if (typeof o?.caption === 'string') return (o.caption as string).slice(0, 100);
  if (Array.isArray(o?.versions) && o.versions[0]) {
    const v = o.versions[0] as Record<string, string>;
    return v.headline || v.body?.slice(0, 100) || '';
  }
  if (typeof o?.hook === 'string') return o.hook as string;
  return gen.input_data?.product_name || gen.input_data?.product || '—';
}

export default function GenerationHistory({ token, limit = 10, compact = false, onSelect }: GenerationHistoryProps) {
  const [generations, setGenerations] = useState<Generation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [copiedId, setCopiedId] = useState('');
  const [expanded, setExpanded] = useState<string | null>(null);

  useEffect(() => {
    if (token) fetchHistory();
  }, [token]);

  const fetchHistory = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${API_URL}/api/skills/generations/history?limit=${limit}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        const data = await res.json();
        setGenerations(data.generations || []);
      } else if (res.status === 404) {
        // API chưa có hoặc chưa migrate DB — fallback gracefully
        setGenerations([]);
      } else {
        setError('Không thể tải lịch sử');
      }
    } catch {
      // Backend offline hoặc route chưa tồn tại
      setGenerations([]);
    } finally {
      setLoading(false);
    }
  };

  const copyContent = (gen: Generation) => {
    const text = JSON.stringify(gen.output_content, null, 2);
    navigator.clipboard.writeText(text);
    setCopiedId(gen.id);
    setTimeout(() => setCopiedId(''), 2000);
  };

  if (!token) {
    return (
      <div className="history-login-prompt">
        <IconClock size={24} />
        <p>Đăng nhập để xem lịch sử tạo nội dung</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="history-loading">
        <div className="loading-spinner" />
        <span>Đang tải lịch sử...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-state">
        <span>⚠️ {error}</span>
        <button className="retry-btn" onClick={fetchHistory}>Thử lại</button>
      </div>
    );
  }

  if (generations.length === 0) {
    return (
      <div className="empty-result">
        <div className="empty-icon purple"><IconClock size={32} /></div>
        <h3>Chưa có lịch sử</h3>
        <p>Tạo nội dung đầu tiên để lịch sử xuất hiện ở đây.</p>
      </div>
    );
  }

  if (compact) {
    // Mode compact cho Dashboard — chỉ list, không expand
    return (
      <div className="activity-list">
        {generations.slice(0, 5).map((gen) => (
          <div
            key={gen.id}
            className="activity-item clickable"
            onClick={() => onSelect?.(gen)}
          >
            <div className={`activity-icon ${typeColor(gen.skill_name)}`}>
              {typeIcon(gen.skill_name)}
            </div>
            <div className="activity-info">
              <span className="activity-product">{getPreview(gen)}</span>
              <span className="activity-meta">
                <span className={`score-pill score-pill-${scoreColor(gen.quality_score)}`}>
                  {gen.quality_score}/100
                </span>
                <span className="activity-time">
                  <IconClock size={12} /> {timeAgo(gen.created_at)}
                </span>
              </span>
            </div>
          </div>
        ))}
      </div>
    );
  }

  // Full mode — standalone page
  return (
    <div className="generation-history">
      <div className="history-header">
        <h2>Lịch Sử Tạo Nội Dung</h2>
        <button className="btn btn-ghost" onClick={fetchHistory}>↻ Làm mới</button>
      </div>

      <div className="history-list">
        {generations.map((gen) => (
          <div key={gen.id} className={`history-item ${expanded === gen.id ? 'expanded' : ''}`}>
            {/* Row chính */}
            <div className="history-item-main" onClick={() => setExpanded(expanded === gen.id ? null : gen.id)}>
              <div className={`history-type-icon ${typeColor(gen.skill_name)}`}>
                {typeIcon(gen.skill_name)}
              </div>

              <div className="history-info">
                <span className="history-type-name">{typeName(gen.skill_name)}</span>
                <span className="history-preview">{getPreview(gen)}</span>
              </div>

              <div className="history-right">
                <span className={`score-pill score-pill-${scoreColor(gen.quality_score)}`}>
                  {gen.quality_score}/100
                </span>
                <span className="history-time">
                  <IconClock size={12} /> {timeAgo(gen.created_at)}
                </span>
                <span className="history-expand">{expanded === gen.id ? '▲' : '▼'}</span>
              </div>
            </div>

            {/* Expanded detail */}
            {expanded === gen.id && (
              <div className="history-detail">
                <div className="history-detail-header">
                  <span className="history-skill-tag">
                    <IconSparkles size={12} /> {gen.skill_name}
                  </span>
                  <button
                    className="copy-btn"
                    onClick={() => copyContent(gen)}
                  >
                    {copiedId === gen.id
                      ? <><IconCheck size={14} /> Đã sao chép!</>
                      : <><IconCopy size={14} /> Sao chép JSON</>
                    }
                  </button>
                </div>

                <div className="history-output">
                  <pre>{JSON.stringify(gen.output_content, null, 2)}</pre>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
