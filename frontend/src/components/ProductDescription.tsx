/* src/components/ProductDescription.tsx (Tiếng Việt) */
import { useState } from 'react';
import { apiGenerate } from '../api';

interface ProductResult {
  headline?: string;
  bullets?: string[];
  description?: string;
  seo_keywords?: string[];
  raw_content?: string;
}

export default function ProductDescription({ token: _token }: { token?: string | null }) {
  const [form, setForm] = useState({
    product_name: '', category: '', features: '', target_audience: 'general', language: 'Vietnamese', tone: 'professional'
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
      const data = await apiGenerate('product-description', form);
      if (data.success) { setResult(data.content); }
      else { setError(data.error || 'Tạo thất bại'); }
    } catch (err) {
      setError('Không thể kết nối đến backend.');
    } finally { setLoading(false); }
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
            <label>Tên Sản Phẩm *</label>
            <input name="product_name" value={form.product_name} onChange={handleChange} placeholder="VD: Tai Nghe Bluetooth" required />
          </div>
          <div className="form-group">
            <label>Danh Mục *</label>
            <input name="category" value={form.category} onChange={handleChange} placeholder="VD: Điện tử, Thời trang" required />
          </div>
        </div>
        <div className="form-group">
          <label>Tính Năng Chính * (phân cách bằng dấu phẩy)</label>
          <textarea name="features" value={form.features} onChange={handleChange} placeholder="VD: Chống ồn, Pin 30 giờ, Chống nước IPX5" required />
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>Đối Tượng</label>
            <input name="target_audience" value={form.target_audience} onChange={handleChange} placeholder="VD: Người trẻ chuyên nghiệp" />
          </div>
          <div className="form-group">
            <label>Ngôn Ngữ</label>
            <select name="language" value={form.language} onChange={handleChange}>
              <option value="Vietnamese">Tiếng Việt</option>
              <option value="English">Tiếng Anh</option>
              <option value="Both">Cả Hai (EN + VI)</option>
            </select>
          </div>
        </div>
        <div className="form-group">
          <label>Phong Cách</label>
          <select name="tone" value={form.tone} onChange={handleChange}>
            <option value="professional">Chuyên Nghiệp</option>
            <option value="casual">Thân Mật</option>
            <option value="luxury">Sang Trọng</option>
            <option value="fun">Vui Vẻ</option>
            <option value="urgent">Khẩn Cấp / FOMO</option>
          </select>
        </div>
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Đang tạo...' : '✨ Tạo Mô Tả Sản Phẩm'}
        </button>
      </form>

      {loading && (<div className="loading"><div className="spinner" /><p>AI đang tạo nội dung...</p></div>)}
      {error && <div className="error">⚠️ {error}</div>}

      {result && (
        <div className="result">
          <h3>📝 Nội Dung Đã Tạo</h3>
          {result.headline && (
            <div className="result-section">
              <h4>Tiêu Đề</h4>
              <p><strong>{result.headline}</strong></p>
              <button className="copy-btn" onClick={() => copyToClipboard(result.headline!, 'headline')}>
                {copied === 'headline' ? '✓ Đã sao chép!' : '📋 Sao chép'}
              </button>
            </div>
          )}
          {result.bullets && result.bullets.length > 0 && (
            <div className="result-section">
              <h4>Lợi Ích Chính</h4>
              <ul>{result.bullets.map((b, i) => <li key={i}>{b}</li>)}</ul>
              <button className="copy-btn" onClick={() => copyToClipboard(result.bullets!.join('\n'), 'bullets')}>
                {copied === 'bullets' ? '✓ Đã sao chép!' : '📋 Sao chép Tất cả'}
              </button>
            </div>
          )}
          {result.description && (
            <div className="result-section">
              <h4>Mô Tả</h4>
              <p>{result.description}</p>
              <button className="copy-btn" onClick={() => copyToClipboard(result.description!, 'desc')}>
                {copied === 'desc' ? '✓ Đã sao chép!' : '📋 Sao chép'}
              </button>
            </div>
          )}
          {result.seo_keywords && result.seo_keywords.length > 0 && (
            <div className="result-section">
              <h4>Từ Khóa SEO</h4>
              <div className="hashtags">{result.seo_keywords.map((k, i) => <span key={i} className="hashtag">{k}</span>)}</div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
