/* src/components/SkillMarketplace.tsx — Trang marketplace duyệt và cài skills */
import { useState, useEffect, useCallback } from 'react';
import SkillCard, { type SkillListing } from './SkillCard';
import QualityReport from './QualityReport';
import { IconSparkles, IconSearch, IconCheck } from './Icons';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface SkillMarketplaceProps {
  token?: string | null;
}

const CATEGORIES = [
  { id: '', label: 'Tất Cả' },
  { id: 'ecommerce', label: '🛒 E-commerce' },
  { id: 'social-media', label: '📱 Social Media' },
  { id: 'advertising', label: '🎯 Advertising' },
  { id: 'video', label: '🎬 Video' },
];

const SORTS = [
  { id: 'featured', label: 'Nổi Bật' },
  { id: 'rating', label: 'Đánh Giá Cao' },
  { id: 'price_asc', label: 'Giá Thấp → Cao' },
  { id: 'price_desc', label: 'Giá Cao → Thấp' },
];

// Detail panel for a single skill
function SkillDetailPanel({
  listing,
  token,
  onInstall,
  onClose,
  installing,
}: {
  listing: SkillListing;
  token?: string | null;
  onInstall: (l: SkillListing) => void;
  onClose: () => void;
  installing: boolean;
}) {
  const isFree = listing.price === 0 && !listing.is_premium;

  return (
    <div className="skill-detail-overlay" onClick={onClose}>
      <div className="skill-detail-panel" onClick={(e) => e.stopPropagation()}>
        <button className="skill-detail-close" onClick={onClose}>✕</button>

        <div className="skill-detail-header">
          <span className="skill-detail-emoji">{listing.cover_emoji || '🤖'}</span>
          <div>
            <h2>{listing.title}</h2>
            <p className="skill-detail-author">by {listing.author_name}</p>
          </div>
          <div className="skill-detail-price">
            {listing.coming_soon ? (
              <span className="price-badge coming-soon">Sắp Ra Mắt</span>
            ) : listing.price === 0 ? (
              <span className="price-badge free">Miễn Phí</span>
            ) : (
              <span className="price-badge premium">${listing.price}</span>
            )}
          </div>
        </div>

        {/* Rating */}
        {listing.rating_count > 0 && (
          <div className="skill-detail-rating">
            <span className="rating-big">{listing.avg_rating.toFixed(1)}</span>
            <div>
              <div className="stars-row">
                {[1,2,3,4,5].map(s => (
                  <span key={s} className={`star ${s <= Math.round(listing.avg_rating) ? 'filled' : ''}`}>★</span>
                ))}
              </div>
              <span className="rating-count-label">{listing.rating_count} đánh giá</span>
            </div>
          </div>
        )}

        {/* Long description */}
        <div className="skill-detail-desc">
          {(listing.long_desc || listing.short_desc).split('\n').map((line, i) => (
            <p key={i}>{line}</p>
          ))}
        </div>

        {/* Tags */}
        <div className="skill-detail-tags">
          {listing.tags.map(t => <span key={t} className="skill-tag">#{t}</span>)}
        </div>

        {/* Quality preview — show mock if free */}
        {isFree && (
          <div className="skill-detail-quality">
            <div className="skill-detail-quality-title">
              <IconSparkles size={14} /> Quality Check System
            </div>
            <QualityReport
              score={listing.avg_rating > 0 ? Math.round(listing.avg_rating * 20) : 90}
              skillName={listing.skill_name}
              compact={true}
            />
          </div>
        )}

        {/* CTA */}
        <div className="skill-detail-cta">
          {listing.is_installed ? (
            <div className="installed-full">
              <IconCheck size={18} /> Đã cài đặt — Sẵn sàng sử dụng
            </div>
          ) : listing.coming_soon ? (
            <button className="btn btn-primary btn-full" disabled>
              Sắp Ra Mắt — Chờ Chút Nhé 🙏
            </button>
          ) : !token ? (
            <button
              className="btn btn-primary btn-full"
              onClick={() => window.dispatchEvent(new CustomEvent('navigate', { detail: 'auth' }))}
            >
              Đăng Nhập Để Cài Đặt
            </button>
          ) : isFree ? (
            <button
              className="btn btn-primary btn-full"
              disabled={installing}
              onClick={() => onInstall(listing)}
            >
              {installing ? (
                <><span className="spinner-small" /> Đang cài...</>
              ) : (
                <><IconSparkles size={16} /> Cài Miễn Phí Ngay</>
              )}
            </button>
          ) : (
            <button
              className="btn btn-premium btn-full"
              onClick={() => onInstall(listing)}
              disabled={installing}
            >
              Mua ${listing.price} — Thanh Toán Qua Stripe
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default function SkillMarketplace({ token }: SkillMarketplaceProps) {
  const [listings, setListings] = useState<SkillListing[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [sort, setSort] = useState('featured');
  const [selectedListing, setSelectedListing] = useState<SkillListing | null>(null);
  const [installingSkill, setInstallingSkill] = useState<string | null>(null);
  const [installedSkills, setInstalledSkills] = useState<Set<string>>(new Set());
  const [successMsg, setSuccessMsg] = useState('');
  const [total, setTotal] = useState(0);

  const fetchListings = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const params = new URLSearchParams();
      if (category) params.set('category', category);
      if (search) params.set('search', search);
      if (sort) params.set('sort', sort);
      params.set('page_size', '20');

      const res = await fetch(`${API_URL}/api/marketplace?${params}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      if (res.ok) {
        const data = await res.json();
        setListings(data.listings || []);
        setTotal(data.total || 0);
      } else {
        setError('Không thể tải marketplace');
      }
    } catch {
      setError('Không thể kết nối đến server');
    } finally {
      setLoading(false);
    }
  }, [category, search, sort, token]);

  useEffect(() => {
    fetchListings();
  }, [fetchListings]);

  // Fetch user installs
  useEffect(() => {
    if (!token) return;
    fetch(`${API_URL}/api/marketplace/my/installs`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(r => r.ok ? r.json() : null)
      .then(data => {
        if (data?.installs) {
          setInstalledSkills(new Set(data.installs.map((i: SkillListing) => i.skill_name)));
        }
      })
      .catch(() => {});
  }, [token]);

  const handleInstall = async (listing: SkillListing) => {
    if (!token) {
      window.dispatchEvent(new CustomEvent('navigate', { detail: 'auth' }));
      return;
    }
    setInstallingSkill(listing.skill_name);
    try {
      const endpoint = listing.price === 0
        ? `/api/marketplace/${listing.skill_name}/install`
        : `/api/marketplace/${listing.skill_name}/purchase`;

      const res = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({}),
      });
      const data = await res.json();
      if (res.ok && data.success) {
        setInstalledSkills(prev => new Set([...prev, listing.skill_name]));
        setSuccessMsg(`✅ ${listing.title} đã cài thành công!`);
        setTimeout(() => setSuccessMsg(''), 3000);
        if (selectedListing?.skill_name === listing.skill_name) {
          setSelectedListing({ ...listing, is_installed: true });
        }
      } else {
        setError(data.detail || 'Cài đặt thất bại');
        setTimeout(() => setError(''), 3000);
      }
    } catch {
      setError('Lỗi kết nối server');
      setTimeout(() => setError(''), 3000);
    } finally {
      setInstallingSkill(null);
    }
  };

  const featuredListings = listings.filter(l => l.is_featured);
  const otherListings = listings.filter(l => !l.is_featured);

  return (
    <div className="marketplace">
      {/* Hero */}
      <div className="marketplace-hero">
        <div className="marketplace-hero-text">
          <h1>
            <IconSparkles size={28} /> Skill Marketplace
          </h1>
          <p>Khám phá và cài đặt các skill AI để tạo nội dung chất lượng cao hơn</p>
        </div>
        <div className="marketplace-hero-stats">
          <div className="hero-stat">
            <span className="hero-stat-val">{total}</span>
            <span className="hero-stat-label">Skills</span>
          </div>
          <div className="hero-stat">
            <span className="hero-stat-val">{installedSkills.size}</span>
            <span className="hero-stat-label">Đã Cài</span>
          </div>
          <div className="hero-stat">
            <span className="hero-stat-val">4.8★</span>
            <span className="hero-stat-label">Avg Rating</span>
          </div>
        </div>
      </div>

      {/* Toast messages */}
      {successMsg && <div className="marketplace-toast success">{successMsg}</div>}
      {error && <div className="marketplace-toast error">⚠️ {error}</div>}

      {/* Filters */}
      <div className="marketplace-filters">
        <div className="marketplace-search">
          <IconSearch size={16} />
          <input
            type="text"
            placeholder="Tìm skill..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>

        <div className="filter-row">
          <div className="category-tabs">
            {CATEGORIES.map(c => (
              <button
                key={c.id}
                className={`category-tab ${category === c.id ? 'active' : ''}`}
                onClick={() => setCategory(c.id)}
              >
                {c.label}
              </button>
            ))}
          </div>

          <select
            className="sort-select"
            value={sort}
            onChange={e => setSort(e.target.value)}
          >
            {SORTS.map(s => (
              <option key={s.id} value={s.id}>{s.label}</option>
            ))}
          </select>
        </div>
      </div>

      {loading && (
        <div className="marketplace-loading">
          <div className="loading-spinner" />
          <span>Đang tải marketplace...</span>
        </div>
      )}

      {!loading && listings.length === 0 && (
        <div className="empty-result">
          <div className="empty-icon purple"><IconSparkles size={32} /></div>
          <h3>Không tìm thấy skill nào</h3>
          <p>Thử thay đổi bộ lọc hoặc tìm kiếm khác.</p>
        </div>
      )}

      {!loading && listings.length > 0 && (
        <>
          {/* Featured section */}
          {featuredListings.length > 0 && !search && !category && (
            <div className="marketplace-section">
              <div className="marketplace-section-header">
                <h2>⭐ Nổi Bật</h2>
                <span className="section-count">{featuredListings.length} skills</span>
              </div>
              <div className="skill-grid skill-grid-featured">
                {featuredListings.map(l => (
                  <SkillCard
                    key={l.skill_name}
                    listing={{ ...l, is_installed: installedSkills.has(l.skill_name) }}
                    onClick={setSelectedListing}
                    onInstall={handleInstall}
                    installing={installingSkill === l.skill_name}
                  />
                ))}
              </div>
            </div>
          )}

          {/* All / Other */}
          {(otherListings.length > 0 || search || category) && (
            <div className="marketplace-section">
              {!search && !category && (
                <div className="marketplace-section-header">
                  <h2>Tất Cả Skills</h2>
                  <span className="section-count">{total} skills</span>
                </div>
              )}
              <div className="skill-grid">
                {(search || category ? listings : otherListings).map(l => (
                  <SkillCard
                    key={l.skill_name}
                    listing={{ ...l, is_installed: installedSkills.has(l.skill_name) }}
                    onClick={setSelectedListing}
                    onInstall={handleInstall}
                    installing={installingSkill === l.skill_name}
                  />
                ))}
              </div>
            </div>
          )}
        </>
      )}

      {/* Skill Detail Overlay */}
      {selectedListing && (
        <SkillDetailPanel
          listing={{ ...selectedListing, is_installed: installedSkills.has(selectedListing.skill_name) }}
          token={token}
          onInstall={handleInstall}
          onClose={() => setSelectedListing(null)}
          installing={installingSkill === selectedListing.skill_name}
        />
      )}
    </div>
  );
}
