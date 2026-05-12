/* src/components/Landing.tsx — Professional Hero + Features + Testimonials + CTA */
import { IconSparkles, IconFileText, IconSearch, IconTarget, IconVideo, IconMic, IconRocket, IconCheck, IconStar, IconZap, IconGlobe, IconShield, IconArrowRight, IconPlay } from './Icons';

interface LandingProps {
  onGetStarted: () => void;
  onLogin: () => void;
  onViewPricing: () => void;
}

export default function Landing({ onGetStarted, onLogin, onViewPricing }: LandingProps) {
  return (
    <div className="landing">
      {/* ─── Navigation ─── */}
      <nav className="landing-nav">
        <div className="nav-brand">
          <div className="nav-logo">
            <IconSparkles size={22} color="#7170ff" />
            <span>AI Content Gen</span>
          </div>
        </div>
        <div className="nav-links">
          <a href="#features">Tính năng</a>
          <a href="#how-it-works">Cách hoạt động</a>
          <a href="#pricing">Bảng giá</a>
        </div>
        <div className="nav-actions">
          <button className="nav-btn-ghost" onClick={onLogin}>Đăng nhập</button>
          <button className="nav-btn-primary" onClick={onGetStarted}>
            Bắt đầu miễn phí
            <IconArrowRight size={16} />
          </button>
        </div>
      </nav>

      {/* ─── Hero ─── */}
      <section className="hero">
        <div className="hero-content">
          <div className="hero-badge">
            <IconRocket size={14} />
            <span>Công cụ AI cho E-Commerce</span>
          </div>
          <h1 className="hero-title">
            Tạo nội dung
            <span className="gradient-text"> chuyển đổi cao</span>
            <br />cho gian hàng của bạn
          </h1>
          <p className="hero-subtitle">
            Mô tả sản phẩm, caption SEO, quảng cáo, kịch bản video — tất cả được tạo bởi AI trong vài giây.
            Dành cho người bán Shopee, Lazada, TikTok Shop.
          </p>
          <div className="hero-cta">
            <button className="btn-hero-primary" onClick={onGetStarted}>
              <IconZap size={18} />
              Bắt đầu miễn phí
            </button>
            <button className="btn-hero-secondary" onClick={onViewPricing}>
              <IconPlay size={16} />
              Xem bảng giá
            </button>
          </div>
        </div>

        {/* ─── Dashboard Mockup Visual ─── */}
        <div className="hero-visual">
          <div className="hero-dashboard-mockup">
            <div className="mockup-header">
              <div className="mockup-dots">
                <span className="dot red" /><span className="dot yellow" /><span className="dot green" />
              </div>
              <div className="mockup-title">AI Content Generator</div>
              <div style={{ width: '40px' }} />
            </div>
            <div className="mockup-body">
              <div className="mockup-sidebar">
                <div className="mockup-nav-item active"><span className="mockup-icon">📊</span> Tổng Quan</div>
                <div className="mockup-nav-item"><span className="mockup-icon">📝</span> Mô Tả SP</div>
                <div className="mockup-nav-item"><span className="mockup-icon">🔍</span> Caption SEO</div>
                <div className="mockup-nav-item"><span className="mockup-icon">🎯</span> Quảng Cáo</div>
                <div className="mockup-nav-item"><span className="mockup-icon">🎬</span> Video AI</div>
              </div>
              <div className="mockup-main">
                <div className="mockup-card">
                  <div style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center' }}>
                    <span style={{ fontWeight: 600 }}>✨ Mô Tả Sản Phẩm</span>
                    <span className="mockup-badge">Pro</span>
                  </div>
                  <div className="mockup-form">
                    <div className="mockup-line" style={{ width: '80%' }} />
                    <div className="mockup-line" style={{ height: '60px', borderRadius: '6px' }} />
                  </div>
                </div>
                <div className="mockup-result">
                   <div style={{ color: '#8a8f98', fontSize: '0.8rem', marginBottom: '1rem' }}>Kết quả dự kiến:</div>
                   <div className="mockup-line" />
                   <div className="mockup-line" />
                   <div className="mockup-line short" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ─── Features ─── */}
      <section className="features" id="features">
        <div className="section-header">
          <div className="section-badge">Tính năng</div>
          <h2 className="section-title">Tất cả những gì bạn cần</h2>
          <p className="hero-subtitle">Để AI làm phần nặng. Bạn tập trung vào việc chốt đơn.</p>
        </div>
        <div className="features-grid">
          <div className="feature-card">
            <IconFileText size={28} color="#7170ff" />
            <h3>Mô Tả Sản Phẩm</h3>
            <p>Tiêu đề, bullet points, mô tả đầy đủ, từ khóa SEO — tùy chỉnh cho sản phẩm và nền tảng của bạn.</p>
          </div>
          <div className="feature-card">
            <IconSearch size={28} color="#7170ff" />
            <h3>Caption & SEO</h3>
            <p>Tiêu đề tối ưu, caption, hashtag cho Shopee, Lazada, Amazon, TikTok Shop, Instagram.</p>
          </div>
          <div className="feature-card">
            <IconTarget size={28} color="#7170ff" />
            <h3>Quảng Cáo</h3>
            <p>3 phiên bản mỗi lần tạo — phong cách PAS, BAB, Story. Thử và chọn phiên bản tốt nhất.</p>
          </div>
        </div>
      </section>

      {/* ─── Footer ─── */}
      <footer className="landing-footer" style={{ borderTop: '1px solid var(--border-subtle)', padding: '4rem 2rem', textAlign: 'center' }}>
        <div className="footer-logo" style={{ marginBottom: '1rem', justifyContent: 'center', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <IconSparkles size={20} color="#7170ff" />
          <span style={{ fontWeight: 600 }}>AI Content Gen</span>
        </div>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          © 2025 AI Content Generator • Built with precision for e-commerce sellers
        </p>
      </footer>
    </div>
  );
}
