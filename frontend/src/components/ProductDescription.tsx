/* src/components/ProductDescription.tsx — Professional Layout */
import { useState } from 'react';
import { apiGenerate } from '../api';
import { IconFileText, IconCheck, IconCopy, IconSparkles } from './Icons';

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
    <div className="tool-page">
      <div className="tool-header">
        <div className="tool-header-icon purple">
          <IconFileText size={24} />
        </div>
        <div>
          <h1>Mô Tả Sản Phẩm</h1>
          <p>Tạo mô tả sản phẩm chuyên nghiệp, tối ưu SEO cho mọi nền tảng.</p>
        </div>
      </div>

      <div className="tool-grid">
        <div className="tool-form-card">
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
            <button type="submit" className="btn btn-primary btn-full" disabled={loading}>
              {loading ? (
                <><span className="spinner-small" /> Đang tạo...</>
              ) : (
                <><IconSparkles size={16} /> Tạo Mô Tả Sản Phẩm</>
              )}
            </button>
          </form>
        </div>

        <div className="tool-result-card">
          {loading && (
            <div className="loading-state">
              <div className="loading-spinner" />
              <p>AI đang tạo nội dung...</p>
              <span className="loading-hint">Thường mất 3-10 giây</span>
            </div>
          )}

          {error && (
            <div className="error-state">
              <span className="error-icon">⚠️</span>
              <p>{error}</p>
            </div>
          )}

          {!loading && !error && !result && (
            <div className="empty-result">
              <div className="empty-icon purple">
                <IconFileText size={32} />
              </div>
              <h3>Nội dung đã tạo sẽ hiển thị ở đây</h3>
              <p>Điền thông tin sản phẩm và nhấn "Tạo" để bắt đầu.</p>
            </div>
          )}

          {result && (
            <div className="result-content">
              <div className="result-header">
                <h3><IconCheck size={18} /> Nội Dung Đã Tạo</h3>
              </div>

              {result.headline && (
                <div className="result-block">
                  <div className="result-block-header">
                    <h4>Tiêu Đề</h4>
                    <button className="copy-btn" onClick={() => copyToClipboard(result.headline!, 'headline')}>
                      {copied === 'headline' ? <><IconCheck size={14} /> Đã sao chép!</> : <><IconCopy size={14} /> Sao chép</>}
                    </button>
                  </div>
                  <p className="result-headline">{result.headline}</p>
                </div>
              )}

              {result.bullets && result.bullets.length > 0 && (
                <div className="result-block">
                  <div className="result-block-header">
                    <h4>Lợi Ích Chính</h4>
                    <button className="copy-btn" onClick={() => copyToClipboard(result.bullets!.join('\n'), 'bullets')}>
                      {copied === 'bullets' ? <><IconCheck size={14} /> Đã sao chép!</> : <><IconCopy size={14} /> Sao chép Tất cả</>}
                    </button>
                  </div>
                  <ul className="result-bullets">
                    {result.bullets.map((b, i) => <li key={i}>{b}</li>)}
                  </ul>
                </div>
              )}

              {result.description && (
                <div className="result-block">
                  <div className="result-block-header">
                    <h4>Mô Tả</h4>
                    <button className="copy-btn" onClick={() => copyToClipboard(result.description!, 'desc')}>
                      {copied === 'desc' ? <><IconCheck size={14} /> Đã sao chép!</> : <><IconCopy size={14} /> Sao chép</>}
                    </button>
                  </div>
                  <p className="result-description">{result.description}</p>
                </div>
              )}

              {result.seo_keywords && result.seo_keywords.length > 0 && (
                <div className="result-block">
                  <h4>Từ Khóa SEO</h4>
                  <div className="hashtags">
                    {result.seo_keywords.map((k, i) => <span key={i} className="hashtag">{k}</span>)}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
