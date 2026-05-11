/* src/components/AdCopy.tsx */
import { useState } from 'react';
import { apiGenerate } from '../api';

interface AdVariation {
  style: string;
  hook: string;
  body: string;
  cta: string;
}

interface AdResult {
  variations?: AdVariation[];
  raw_content?: string;
}

export default function AdCopy({ token: _token }: { token?: string | null }) {
  const [form, setForm] = useState({
    product_name: '',
    category: '',
    selling_points: '',
    target_audience: 'general',
    platform: 'facebook',
    language: 'English',
    tone: 'persuasive'
  });
  const [result, setResult] = useState<AdResult | null>(null);
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
      const data = await apiGenerate('ad-copy', form);
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

  const copyVariation = (v: AdVariation) => {
    const text = `${v.hook}\n\n${v.body}\n\n${v.cta}`;
    navigator.clipboard.writeText(text);
    setCopied(v.style);
    setTimeout(() => setCopied(''), 2000);
  };

  return (
    <div className="card">
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <div className="form-group">
            <label>Product Name *</label>
            <input name="product_name" value={form.product_name} onChange={handleChange} placeholder="e.g. Smart Fitness Watch" required />
          </div>
          <div className="form-group">
            <label>Category *</label>
            <input name="category" value={form.category} onChange={handleChange} placeholder="e.g. Wearables, Health" required />
          </div>
        </div>

        <div className="form-group">
          <label>Key Selling Points * (comma-separated)</label>
          <textarea name="selling_points" value={form.selling_points} onChange={handleChange} placeholder="e.g. Heart rate monitor, 7-day battery, sleep tracking, waterproof" required />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Target Audience</label>
            <input name="target_audience" value={form.target_audience} onChange={handleChange} placeholder="e.g. Fitness enthusiasts 25-40" />
          </div>
          <div className="form-group">
            <label>Ad Platform</label>
            <select name="platform" value={form.platform} onChange={handleChange}>
              <option value="facebook">Facebook Ads</option>
              <option value="instagram">Instagram Ads</option>
              <option value="google">Google Ads</option>
              <option value="tiktok">TikTok Ads</option>
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Language</label>
            <select name="language" value={form.language} onChange={handleChange}>
              <option value="English">English</option>
              <option value="Vietnamese">Vietnamese</option>
            </select>
          </div>
          <div className="form-group">
            <label>Tone</label>
            <select name="tone" value={form.tone} onChange={handleChange}>
              <option value="persuasive">Persuasive</option>
              <option value="urgent">Urgent / FOMO</option>
              <option value="emotional">Emotional</option>
              <option value="humorous">Humorous</option>
              <option value="professional">Professional</option>
            </select>
          </div>
        </div>

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Generating...' : '✨ Generate Ad Copy (3 Variations)'}
        </button>
      </form>

      {loading && (
        <div className="loading">
          <div className="spinner" />
          <p>Creating high-converting ad copy...</p>
        </div>
      )}

      {error && <div className="error">⚠️ {error}</div>}

      {result && (
        <div className="result">
          <h3>🎯 Ad Copy Variations</h3>
          <p style={{ fontSize: '0.85rem', color: '#71717a', marginBottom: '1rem' }}>
            3 styles — test them all and pick the winner!
          </p>

          {result.variations && result.variations.map((v, i) => (
            <div key={i} className="ad-variation">
              <h5>{v.style}</h5>
              <p><span className="label">Hook:</span> {v.hook}</p>
              <p><span className="label">Body:</span> {v.body}</p>
              <p><span className="label">CTA:</span> {v.cta}</p>
              <button className="copy-btn" onClick={() => copyVariation(v)}>
                {copied === v.style ? '✓ Copied!' : '📋 Copy Variation'}
              </button>
            </div>
          ))}

          {result.raw_content && !result.variations && (
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
