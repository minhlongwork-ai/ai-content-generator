/* src/components/ProductDescription.tsx */
import { useState } from 'react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface ProductResult {
  headline?: string;
  bullets?: string[];
  description?: string;
  seo_keywords?: string[];
  raw_content?: string;
}

export default function ProductDescription({ token: _token }: { token?: string | null }) {
  const [form, setForm] = useState({
    product_name: '',
    category: '',
    features: '',
    target_audience: 'general',
    language: 'English',
    tone: 'professional'
  });
  const [result, setResult] = useState<ProductResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const res = await fetch(`${API_URL}/api/generate/product-description`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      });
      const data = await res.json();
      if (data.success) {
        setResult(data.content);
      } else {
        setError(data.error || 'Generation failed');
      }
    } catch (err) {
      setError('Cannot connect to backend. Make sure it\'s running on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    setCopied(label);
    setTimeout(() => setCopied(''), 2000);
  };

  return (
    <div className="card">
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <div className="form-group">
            <label>Product Name *</label>
            <input name="product_name" value={form.product_name} onChange={handleChange} placeholder="e.g. Wireless Bluetooth Earbuds" required />
          </div>
          <div className="form-group">
            <label>Category *</label>
            <input name="category" value={form.category} onChange={handleChange} placeholder="e.g. Electronics, Fashion" required />
          </div>
        </div>

        <div className="form-group">
          <label>Key Features * (comma-separated)</label>
          <textarea name="features" value={form.features} onChange={handleChange} placeholder="e.g. Noise cancellation, 30hr battery, IPX5 waterproof" required />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Target Audience</label>
            <input name="target_audience" value={form.target_audience} onChange={handleChange} placeholder="e.g. Young professionals" />
          </div>
          <div className="form-group">
            <label>Language</label>
            <select name="language" value={form.language} onChange={handleChange}>
              <option value="English">English</option>
              <option value="Vietnamese">Vietnamese</option>
              <option value="Both">Both (EN + VI)</option>
            </select>
          </div>
        </div>

        <div className="form-group">
          <label>Tone</label>
          <select name="tone" value={form.tone} onChange={handleChange}>
            <option value="professional">Professional</option>
            <option value="casual">Casual</option>
            <option value="luxury">Luxury</option>
            <option value="fun">Fun / Playful</option>
            <option value="urgent">Urgent / FOMO</option>
          </select>
        </div>

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Generating...' : '✨ Generate Product Description'}
        </button>
      </form>

      {loading && (
        <div className="loading">
          <div className="spinner" />
          <p>AI is crafting your content...</p>
        </div>
      )}

      {error && <div className="error">⚠️ {error}</div>}

      {result && (
        <div className="result">
          <h3>📝 Generated Content</h3>

          {result.headline && (
            <div className="result-section">
              <h4>Headline</h4>
              <p><strong>{result.headline}</strong></p>
              <button className="copy-btn" onClick={() => copyToClipboard(result.headline!, 'headline')}>
                {copied === 'headline' ? '✓ Copied!' : '📋 Copy'}
              </button>
            </div>
          )}

          {result.bullets && result.bullets.length > 0 && (
            <div className="result-section">
              <h4>Key Benefits</h4>
              <ul>
                {result.bullets.map((b, i) => <li key={i}>{b}</li>)}
              </ul>
              <button className="copy-btn" onClick={() => copyToClipboard(result.bullets!.join('\n'), 'bullets')}>
                {copied === 'bullets' ? '✓ Copied!' : '📋 Copy All'}
              </button>
            </div>
          )}

          {result.description && (
            <div className="result-section">
              <h4>Description</h4>
              <p>{result.description}</p>
              <button className="copy-btn" onClick={() => copyToClipboard(result.description!, 'desc')}>
                {copied === 'desc' ? '✓ Copied!' : '📋 Copy'}
              </button>
            </div>
          )}

          {result.seo_keywords && result.seo_keywords.length > 0 && (
            <div className="result-section">
              <h4>SEO Keywords</h4>
              <div className="hashtags">
                {result.seo_keywords.map((k, i) => <span key={i} className="hashtag">{k}</span>)}
              </div>
            </div>
          )}

          {result.raw_content && (
            <div className="result-section">
              <h4>Raw Output</h4>
              <p>{result.raw_content}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
