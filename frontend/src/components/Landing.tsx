/* src/components/Landing.tsx — Professional Hero + Features + Testimonials + CTA */
import { IconSparkles, IconFileText, IconSearch, IconTarget, IconVideo, IconMic, IconRocket, IconCheck, IconStar, IconZap, IconGlobe, IconShield, IconArrowRight, IconPlay } from './Icons';

interface LandingProps {
  onGetStarted: () => void;
  onViewPricing: () => void;
}

export default function Landing({ onGetStarted, onViewPricing }: LandingProps) {
  return (
    <div className="landing">
      {/* ─── Navigation ─── */}
      <nav className="landing-nav">
        <div className="nav-brand">
          <div className="nav-logo">
            <IconSparkles size={22} />
            <span>AI Content Gen</span>
          </div>
        </div>
        <div className="nav-links">
          <a href="#features">Tính năng</a>
          <a href="#how-it-works">Cách hoạt động</a>
          <a href="#pricing">Bảng giá</a>
        </div>
        <div className="nav-actions">
          <button className="nav-btn-ghost" onClick={onViewPricing}>Bảng giá</button>
          <button className="nav-btn-primary" onClick={onGetStarted}>
            Bắt đầu miễn phí
            <IconArrowRight size={16} />
          </button>
        </div>
      </nav>

      {/* ─── Hero ─── */}
      <section className="hero">
        <div className="hero-grid">
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
                Bắt đầu miễn phí — Không cần thẻ
              </button>
              <button className="btn-hero-secondary" onClick={onViewPricing}>
                <IconPlay size={16} />
                Xem bảng giá
              </button>
            </div>
            <div className="hero-trust">
              <div className="trust-avatars">
                <div className="avatar">L</div>
                <div className="avatar">M</div>
                <div className="avatar">T</div>
                <div className="avatar">H</div>
                <div className="avatar">+</div>
              </div>
              <div className="trust-text">
                <div className="trust-stars">
                  {[...Array(5)].map((_, i) => <IconStar key={i} size={14} />)}
                </div>
                <span>Được tin dùng bởi <strong>500+</strong> người bán hàng</span>
              </div>
            </div>
          </div>
          <div className="hero-visual">
            <div className="hero-dashboard-mockup">
              <div className="mockup-header">
                <div className="mockup-dots">
                  <span className="dot red" /><span className="dot yellow" /><span className="dot green" />
                </div>
                <div className="mockup-title">AI Content Generator</div>
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
                    <div className="mockup-card-header">
                      <span className="mockup-card-title">✨ Mô Tả Sản Phẩm</span>
                      <span className="mockup-badge">Pro</span>
                    </div>
                    <div className="mockup-form">
                      <div className="mockup-input" />
                      <div className="mockup-input short" />
                      <div className="mockup-textarea" />
                    </div>
                    <div className="mockup-btn">Tạo nội dung →</div>
                  </div>
                  <div className="mockup-result">
                    <div className="mockup-result-header">
                      <span>Kết quả</span>
                      <span className="mockup-copy">📋 Copy</span>
                    </div>
                    <div className="mockup-result-lines">
                      <div className="mockup-line" />
                      <div className="mockup-line" />
                      <div className="mockup-line short" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="hero-floating-card card-1">
              <IconZap size={18} />
              <span>Tạo trong 3 giây</span>
            </div>
            <div className="hero-floating-card card-2">
              <IconCheck size={18} />
              <span>SEO tối ưu</span>
            </div>
          </div>
        </div>

        <div className="hero-stats">
          <div className="stat">
            <div className="stat-icon-wrap purple">
              <IconFileText size={20} />
            </div>
            <span className="stat-number">4+</span>
            <span className="stat-label">Loại Nội Dung</span>
          </div>
          <div className="stat">
            <div className="stat-icon-wrap blue">
              <IconGlobe size={20} />
            </div>
            <span className="stat-number">2</span>
            <span className="stat-label">Ngôn Ngữ (EN + VI)</span>
          </div>
          <div className="stat">
            <div className="stat-icon-wrap green">
              <IconTarget size={20} />
            </div>
            <span className="stat-number">6+</span>
            <span className="stat-label">Nền Tảng Hỗ Trợ</span>
          </div>
          <div className="stat">
            <div className="stat-icon-wrap orange">
              <IconShield size={20} />
            </div>
            <span className="stat-number">Miễn phí</span>
            <span className="stat-label">Mô Hình AI</span>
          </div>
        </div>
      </section>

      {/* ─── Logos / Platforms ─── */}
      <section className="platforms-bar">
        <p className="platforms-label">Tối ưu cho các nền tảng</p>
        <div className="platforms-logos">
          <div className="platform-logo">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
            <span>Shopee</span>
          </div>
          <div className="platform-logo">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
            <span>Lazada</span>
          </div>
          <div className="platform-logo">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
            <span>Amazon</span>
          </div>
          <div className="platform-logo">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
            <span>TikTok Shop</span>
          </div>
          <div className="platform-logo">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
            <span>Etsy</span>
          </div>
          <div className="platform-logo">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
            <span>Instagram</span>
          </div>
          <div className="platform-logo">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
            <span>Facebook Ads</span>
          </div>
          <div className="platform-logo">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
            <span>Google Ads</span>
          </div>
        </div>
      </section>

      {/* ─── Features ─── */}
      <section className="features" id="features">
        <div className="section-header">
          <div className="section-badge">Tính năng</div>
          <h2 className="section-title">Tất cả những gì bạn cần để bán nhiều hơn</h2>
          <p className="section-subtitle">Không cần viết từ đầu. Để AI làm phần nặng.</p>
        </div>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon-wrap purple">
              <IconFileText size={24} />
            </div>
            <h3>Mô Tả Sản Phẩm</h3>
            <p>Tiêu đề, bullet points, mô tả đầy đủ, từ khóa SEO — tùy chỉnh cho sản phẩm và nền tảng của bạn.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon-wrap blue">
              <IconSearch size={24} />
            </div>
            <h3>Caption & SEO</h3>
            <p>Tiêu đề tối ưu, caption, hashtag cho Shopee, Lazada, Amazon, TikTok Shop, Instagram.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon-wrap red">
              <IconTarget size={24} />
            </div>
            <h3>Quảng Cáo</h3>
            <p>3 phiên bản mỗi lần tạo — phong cách PAS, BAB, Story. Thử và chọn phiên bản tốt nhất.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon-wrap green">
              <IconVideo size={24} />
            </div>
            <h3>Kịch Bản Video + TTS</h3>
            <p>Kịch bản video ngắn với lời thoại từng cảnh. Tự động tạo giọng nói bằng TTS.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon-wrap orange">
              <IconMic size={24} />
            </div>
            <h3>Giọng Nói AI (TTS)</h3>
            <p>Đa ngôn ngữ, giọng nam/nữ, tốc độ điều chỉnh được. Edge-TTS (miễn phí) hoặc ElevenLabs (cao cấp).</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon-wrap pink">
              <IconPlay size={24} />
            </div>
            <h3>Tạo Video AI</h3>
            <p>Tạo video ngắn từ mô tả văn bản. Hỗ trợ Seedance, Kling, Veo qua fal.ai & Replicate.</p>
          </div>
        </div>
      </section>

      {/* ─── How it works ─── */}
      <section className="how-it-works" id="how-it-works">
        <div className="section-header">
          <div className="section-badge">Cách hoạt động</div>
          <h2 className="section-title">Chỉ 3 bước để có nội dung chuyên nghiệp</h2>
        </div>
        <div className="steps">
          <div className="step">
            <div className="step-number">1</div>
            <div className="step-icon-wrap">
              <IconFileText size={28} />
            </div>
            <h3>Nhập Thông Tin Sản Phẩm</h3>
            <p>Tên, danh mục, tính năng — chỉ vậy thôi.</p>
          </div>
          <div className="step-connector">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </div>
          <div className="step">
            <div className="step-number">2</div>
            <div className="step-icon-wrap">
              <IconZap size={28} />
            </div>
            <h3>AI Tạo Nội Dung</h3>
            <p>Nhiều phiên bản trong vài giây.</p>
          </div>
          <div className="step-connector">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
          </div>
          <div className="step">
            <div className="step-number">3</div>
            <div className="step-icon-wrap">
              <IconCheck size={28} />
            </div>
            <h3>Sao Chép & Đăng Bán</h3>
            <p>Một click sao chép. Dán vào gian hàng.</p>
          </div>
        </div>
      </section>

      {/* ─── Testimonials ─── */}
      <section className="testimonials">
        <div className="section-header">
          <div className="section-badge">Đánh giá</div>
          <h2 className="section-title">Người bán hàng nói gì?</h2>
        </div>
        <div className="testimonials-grid">
          <div className="testimonial-card">
            <div className="testimonial-stars">
              {[...Array(5)].map((_, i) => <IconStar key={i} size={16} />)}
            </div>
            <p className="testimonial-text">
              "Trước đây tôi mất 2 giờ để viết mô tả cho 1 sản phẩm. Giờ chỉ cần 3 giây. AI Content Gen đã giúp tôi tăng doanh số 40% trên Shopee."
            </p>
            <div className="testimonial-author">
              <div className="author-avatar">L</div>
              <div>
                <div className="author-name">Lan Nguyễn</div>
                <div className="author-role">Chủ shop thời trang, Shopee</div>
              </div>
            </div>
          </div>
          <div className="testimonial-card">
            <div className="testimonial-stars">
              {[...Array(5)].map((_, i) => <IconStar key={i} size={16} />)}
            </div>
            <p className="testimonial-text">
              "Caption SEO tạo ra cực kỳ chính xác. Sản phẩm của tôi lên top search nhanh hơn hẳn. Gói miễn phí đã đủ dùng cho shop nhỏ."
            </p>
            <div className="testimonial-author">
              <div className="author-avatar">M</div>
              <div>
                <div className="author-name">Minh Trần</div>
                <div className="author-role">Seller Lazada, 3 năm kinh nghiệm</div>
              </div>
            </div>
          </div>
          <div className="testimonial-card">
            <div className="testimonial-stars">
              {[...Array(5)].map((_, i) => <IconStar key={i} size={16} />)}
            </div>
            <p className="testimonial-text">
              "Tính năng tạo kịch bản video là game-changer. Tôi không cần thuê copywriter nữa. Tiết kiệt 5 triệu/tháng."
            </p>
            <div className="testimonial-author">
              <div className="author-avatar">H</div>
              <div>
                <div className="author-name">Hùng Phạm</div>
                <div className="author-role">TikTok Shop Creator</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ─── CTA ─── */}
      <section className="cta-section" id="pricing">
        <div className="cta-content">
          <div className="cta-badge">
            <IconRocket size={16} />
            <span>Sẵn sàng bắt đầu?</span>
          </div>
          <h2>Sẵn Sàng Tăng 10x Nội Dung?</h2>
          <p>Bắt đầu tạo nội dung chuyển đổi cao miễn phí. Không cần thẻ tín dụng.</p>
          <div className="cta-actions">
            <button className="btn-hero-primary" onClick={onGetStarted}>
              <IconZap size={18} />
              Bắt Đầu Miễn Phí →
            </button>
            <button className="btn-hero-secondary" onClick={onViewPricing}>
              Xem Bảng Giá
            </button>
          </div>
          <div className="cta-trust">
            <IconShield size={14} />
            <span>Miễn phí mãi mãi • Không cần thẻ • Hủy bất cứ lúc nào</span>
          </div>
        </div>
      </section>

      {/* ─── Footer ─── */}
      <footer className="landing-footer">
        <div className="footer-content">
          <div className="footer-brand">
            <div className="footer-logo">
              <IconSparkles size={20} />
              <span>AI Content Gen</span>
            </div>
            <p>Công cụ AI tạo nội dung cho người bán hàng e-commerce.</p>
          </div>
          <div className="footer-links">
            <div className="footer-col">
              <h4>Sản phẩm</h4>
              <a href="#features">Tính năng</a>
              <a href="#pricing">Bảng giá</a>
              <a href="#">API</a>
            </div>
            <div className="footer-col">
              <h4>Hỗ trợ</h4>
              <a href="#">Tài liệu</a>
              <a href="#">Liên hệ</a>
              <a href="#">FAQ</a>
            </div>
            <div className="footer-col">
              <h4>Pháp lý</h4>
              <a href="#">Điều khoản</a>
              <a href="#">Bảo mật</a>
            </div>
          </div>
        </div>
        <div className="footer-bottom">
          <p>© 2025 AI Content Generator • Được tạo với ❤️ cho người bán hàng e-commerce</p>
        </div>
      </footer>
    </div>
  );
}
