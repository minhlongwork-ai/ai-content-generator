/* src/components/CaptionSEO.tsx */
import { useState } from 'react';
import { apiGenerate } from '../api';

interface CaptionResult {
  seo_title?: string;
  caption?: string;
  hashtags?: string[];
  seo_keywords?: string[];
  raw_content?: string;
}

export default function CaptionSEO({ token: _token }: { token?: string | null }) {
  const [form, setForm] = useState({
    product_name: '',
    category: '',
    features: '',
    platform: 'shopee',
    language: 'English'
  });
  const [result, setResult] = useState<CaptionResult | null>(null);
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
      const data = await apiGenerate('caption-seo', form);
      if (data.success) {
        setResult(data.content);
      } else {
        setError(data.error || 'Generation failed');
      }
    } catch (err) {
      setError('Cannot connect to backend. Make sure it\'s running.');
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
            <input name="product_name" value={form.product_name} onChange={handleChange} placeholder="e.g. Summer Floral Dress" required />
          </div>
          <div className="form-group">
            <label>Category *</label>
            <input name="category" value={form.category} onChange={handleChange} placeholder="e.g. Women's Fashion" required />
          </div>
        </div>

        <div className="form-group">
          <label>Key Features * (comma-separated)</label>
          <textarea name="features" value={form.features} onChange={handleChange} placeholder="e.g. Lightweight, breathable, floral print, knee-length" required />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Platform</label>
            <select name="platform" value={form.platform} onChange={handleChange}>
              <option value="shopee">Shopee</option>
              <option value="lazada">Lazada</option>
              <option value="amazon">Amazon</option>
              <option value="etsy">Etsy</option>
              <option value="tiktok">TikTok Shop</option>
              <option value="instagram">Instagram</option>
            </select>
          </div>
          <div className="form-group">
            <label>Language</label>
            <select name="language" value={form.language} onChange={handleChange}>
              <option value="English">English</option>
              <option value="Vietnamese">Vietnamese</option>
            </select>
          </div>
        </div>

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Generating...' : '✨ Generate Caption & SEO'}
        </button>
      </form>

      {loading && (
        <div className="loading">
          <div className="spinner" />
          <p>Optimizing your listing...</p>
        </div>
      )}

      {error && <div className="error">⚠️ {error}</div>}

      {result && (
        <div className="result">
          <h3>🔍 SEO-Optimized Content</h3>

          {result.seo_title && (
            <div className="result-section">
              <h4>SEO Title</h4>
              <p><strong>{result.seo_title}</strong></p>
              <button className="copy-btn" onClick={() => copyToClipboard(result.seo_title!, 'title')}>
                {copied === 'title' ? '✓ Copied!' : '📋 Copy'}
              </button>
            </div>
          )}

          {result.caption && (
            <div className="result-section">
              <h4>Caption / Short Description</h4>
              <p>{result.caption}</p>
              <button className="copy-btn" onClick={() => copyToClipboard(result.caption!, 'caption')}>
                {copied === 'caption' ? '✓ Copied!' : '📋 Copy'}
              </button>
            </div>
          )}

          {result.hashtags && result.hashtags.length > 0 && (
            <div className="result-section">
              <h4>Hashtags</h4>
              <div className="hashtags">
                {result.hashtags.map((h, i) => <span key={i} className="hashtag">#{h}</span>)}
              </div>
              <button className="copy-btn" onClick={() => copyToClipboard(result.hashtags!.map(h => '#' + h).join(' '), 'tags')}>
                {copied === 'tags' ? '✓ Copied!' : '📋 Copy All'}
              </button>
            </div>
          )}

          {result.seo_keywords && result.seo_keywords.length > 0 && (
            <div className="result-section">
              <h4>Long-tail SEO Keywords</h4>
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
