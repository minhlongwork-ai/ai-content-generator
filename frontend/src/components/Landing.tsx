/* src/components/Landing.tsx — Hero + Features + CTA (Tiếng Việt) */

interface LandingProps {
  onGetStarted: () => void;
  onViewPricing: () => void;
}

export default function Landing({ onGetStarted, onViewPricing }: LandingProps) {
  return (
    <div className="landing">
      {/* Hero */}
      <section className="hero">
        <div className="hero-badge">🚀 Công cụ AI • Dành cho E-Commerce</div>
        <h1 className="hero-title">
          Tạo Nội Dung Chuyển Đổi Cao
          <span className="gradient-text"> Cho E-Commerce</span>
          <br />trong Vài Giây
        </h1>
        <p className="hero-subtitle">
          Mô tả sản phẩm, caption SEO, quảng cáo, kịch bản video — tất cả đều được tạo bởi AI.
          Dành cho người bán Shopee, Lazada, TikTok Shop.
        </p>
        <div className="hero-cta">
          <button className="btn-hero-primary" onClick={onGetStarted}>
            Bắt Đầu Miễn Phí — Không Cần Thẻ
          </button>
          <button className="btn-hero-secondary" onClick={onViewPricing}>
            Xem Bảng Giá
          </button>
        </div>
        <div className="hero-stats">
          <div className="stat">
            <span className="stat-number">4+</span>
            <span className="stat-label">Loại Nội Dung</span>
          </div>
          <div className="stat">
            <span className="stat-number">2</span>
            <span className="stat-label">Ngôn Ngữ (EN + VI)</span>
          </div>
          <div className="stat">
            <span className="stat-number">6+</span>
            <span className="stat-label">Nền Tảng Hỗ Trợ</span>
          </div>
          <div className="stat">
            <span className="stat-number">Miễn phí</span>
            <span className="stat-label">Mô Hình AI</span>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="features">
        <h2 className="section-title">Tất Cả Những Gì Bạn Cần Để Bán Nhiều Hơn</h2>
        <p className="section-subtitle">Không cần viết từ đầu. Để AI làm phần nặng.</p>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">📝</div>
            <h3>Mô Tả Sản Phẩm</h3>
            <p>Tiêu đề, bullet points, mô tả đầy đủ, từ khóa SEO — tùy chỉnh cho sản phẩm và nền tảng của bạn.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🔍</div>
            <h3>Caption & SEO</h3>
            <p>Tiêu đề tối ưu, caption, hashtag cho Shopee, Lazada, Amazon, TikTok Shop, Instagram.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🎯</div>
            <h3>Quảng Cáo</h3>
            <p>3 phiên bản mỗi lần tạo — phong cách PAS, BAB, Story. Thử và chọn phiên bản tốt nhất.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🎬</div>
            <h3>Kịch Bản Video + TTS</h3>
            <p>Kịch bản video ngắn với lời thoại từng cảnh. Tự động tạo giọng nói bằng TTS.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🎙️</div>
            <h3>Giọng Nói AI (TTS)</h3>
            <p>Đa ngôn ngữ, giọng nam/nữ, tốc độ điều chỉnh được. Edge-TTS (miễn phí) hoặc ElevenLabs (cao cấp).</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🎥</div>
            <h3>Tạo Video AI</h3>
            <p>Tạo video ngắn từ mô tả văn bản. Hỗ trợ Seedance, Kling, Veo qua fal.ai & Replicate.</p>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="how-it-works">
        <h2 className="section-title">Cách Hoạt Động</h2>
        <div className="steps">
          <div className="step">
            <div className="step-number">1</div>
            <h3>Nhập Thông Tin Sản Phẩm</h3>
            <p>Tên, danh mục, tính năng — chỉ vậy thôi.</p>
          </div>
          <div className="step-arrow">→</div>
          <div className="step">
            <div className="step-number">2</div>
            <h3>AI Tạo Nội Dung</h3>
            <p>Nhiều phiên bản trong vài giây.</p>
          </div>
          <div className="step-arrow">→</div>
          <div className="step">
            <div className="step-number">3</div>
            <h3>Sao Chép & Đăng Bán</h3>
            <p>Một click sao chép. Dán vào gian hàng.</p>
          </div>
        </div>
      </section>

      {/* Platforms */}
      <section className="platforms">
        <h2 className="section-title">Tối Ưu Cho</h2>
        <div className="platform-logos">
          <span className="platform-tag">Shopee</span>
          <span className="platform-tag">Lazada</span>
          <span className="platform-tag">Amazon</span>
          <span className="platform-tag">TikTok Shop</span>
          <span className="platform-tag">Etsy</span>
          <span className="platform-tag">Instagram</span>
          <span className="platform-tag">Facebook Ads</span>
          <span className="platform-tag">Google Ads</span>
        </div>
      </section>

      {/* CTA */}
      <section className="cta-section">
        <h2>Sẵn Sàng Tăng 10x Nội Dung?</h2>
        <p>Bắt đầu tạo nội dung chuyển đổi cao miễn phí.</p>
        <button className="btn-hero-primary" onClick={onGetStarted}>
          Bắt Đầu Miễn Phí →
        </button>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <p>© 2025 AI Content Generator • Được tạo với ❤️ cho người bán hàng e-commerce</p>
      </footer>
    </div>
  );
}
