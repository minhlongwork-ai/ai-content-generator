/* src/components/Landing.tsx — Hero + Features + CTA */

interface LandingProps {
  onGetStarted: () => void;
  onViewPricing: () => void;
}

export default function Landing({ onGetStarted, onViewPricing }: LandingProps) {

  return (
    <div className="landing">
      {/* Hero */}
      <section className="hero">
        <div className="hero-badge">🚀 AI-Powered • Built for E-Commerce</div>
        <h1 className="hero-title">
          Generate High-Converting
          <span className="gradient-text"> E-Commerce Content</span>
          <br />in Seconds
        </h1>
        <p className="hero-subtitle">
          Product descriptions, SEO captions, ad copies, video scripts — all powered by AI.
          Built for Shopee, Lazada, TikTok Shop sellers.
        </p>
        <div className="hero-cta">
          <button className="btn-hero-primary" onClick={onGetStarted}>
            Start Free — No Credit Card
          </button>
          <button className="btn-hero-secondary" onClick={onViewPricing}>
            View Pricing
          </button>
        </div>
        <div className="hero-stats">
          <div className="stat">
            <span className="stat-number">4+</span>
            <span className="stat-label">Content Types</span>
          </div>
          <div className="stat">
            <span className="stat-number">2</span>
            <span className="stat-label">Languages (EN + VI)</span>
          </div>
          <div className="stat">
            <span className="stat-number">6+</span>
            <span className="stat-label">Platforms Supported</span>
          </div>
          <div className="stat">
            <span className="stat-number">Free</span>
            <span className="stat-label">AI Models Included</span>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="features">
        <h2 className="section-title">Everything You Need to Sell More</h2>
        <p className="section-subtitle">Stop writing from scratch. Let AI do the heavy lifting.</p>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">📝</div>
            <h3>Product Descriptions</h3>
            <p>Headlines, bullet points, full descriptions, and SEO keywords — tailored for your product and platform.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🔍</div>
            <h3>Caption & SEO</h3>
            <p>Optimized titles, captions, and hashtags for Shopee, Lazada, Amazon, TikTok Shop, Instagram.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🎯</div>
            <h3>Ad Copy</h3>
            <p>3 variations per generation — PAS, BAB, and Story styles. Test and pick the winner.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🎬</div>
            <h3>Video Scripts + TTS</h3>
            <p>Short-form video scripts with scene-by-scene narration. Auto-generate voice-over with TTS.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🎙️</div>
            <h3>AI Voice (TTS)</h3>
            <p>Multiple languages, male/female voices, adjustable speed. Edge-TTS (free) or ElevenLabs (premium).</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🎥</div>
            <h3>AI Video Generation</h3>
            <p>Generate short videos from text prompts. Supports Seedance, Kling, Veo via fal.ai & Replicate.</p>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="how-it-works">
        <h2 className="section-title">How It Works</h2>
        <div className="steps">
          <div className="step">
            <div className="step-number">1</div>
            <h3>Enter Product Info</h3>
            <p>Name, category, features — that's it.</p>
          </div>
          <div className="step-arrow">→</div>
          <div className="step">
            <div className="step-number">2</div>
            <h3>AI Generates Content</h3>
            <p>Multiple variations in seconds.</p>
          </div>
          <div className="step-arrow">→</div>
          <div className="step">
            <div className="step-number">3</div>
            <h3>Copy & Publish</h3>
            <p>One-click copy. Paste to your store.</p>
          </div>
        </div>
      </section>

      {/* Platforms */}
      <section className="platforms">
        <h2 className="section-title">Optimized For</h2>
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
        <h2>Ready to 10x Your Content?</h2>
        <p>Start generating high-converting content for free.</p>
        <button className="btn-hero-primary" onClick={onGetStarted}>
          Get Started Free →
        </button>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <p>© 2025 AI Content Generator • Built with ❤️ for e-commerce sellers</p>
      </footer>
    </div>
  );
}
