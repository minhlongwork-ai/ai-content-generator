/* src/components/CaptionSEO.tsx (Tiếng Việt) */
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
  const [form, setForm] = useState({ product_name: '', category: '', features: '', platform: 'shopee', language: 'Vietnamese' });
  const [result, setResult] = useState<CaptionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); setLoading(true); setError(''); setResult(null);
    try {
      const data = await apiGenerate('caption-seo', form);
      if (data.success) setResult(data.content);
      else setError(data.error || 'Tạo thất bại');
    } catch { setError('Không thể kết nối đến backend.'); }
    finally { setLoading(false); }
  };

  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text); setCopied(label); setTimeout(() => setCopied(''), 2000);
  };

  return (
    <div className="card">
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <div className="form-group"><label>Tên Sản Phẩm *</label><input name="product_name" value={form.product_name} onChange={handleChange} placeholder="VD: Váy Hoa Mùa Hè" required /></div>
          <div className="form-group"><label>Danh Mục *</label><input name="category" value={form.category} onChange={handleChange} placeholder="VD: Thời trang Nữ" required /></div>
        </div>
        <div className="form-group"><label>Tính Năng Chính * (phân cách bằng dấu phẩy)</label><textarea name="features" value={form.features} onChange={handleChange} placeholder="VD: Nhẹ, thoáng khí, hoa in, đầu gối" required /></div>
        <div className="form-row">
          <div className="form-group">
            <label>Nền Tảng</label>
            <select name="platform" value={form.platform} onChange={handleChange}>
              <option value="shopee">Shopee</option><option value="lazada">Lazada</option><option value="amazon">Amazon</option>
              <option value="tiktok">TikTok Shop</option><option value="instagram">Instagram</option><option value="etsy">Etsy</option>
            </select>
          </div>
          <div className="form-group">
            <label>Ngôn Ngữ</label>
            <select name="language" value={form.language} onChange={handleChange}>
              <option value="Vietnamese">Tiếng Việt</option><option value="English">Tiếng Anh</option>
            </select>
          </div>
        </div>
        <button type="submit" className="btn btn-primary" disabled={loading}>{loading ? 'Đang tạo...' : '✨ Tạo Caption & SEO'}</button>
      </form>
      {loading && (<div className="loading"><div className="spinner" /><p>Đang tối ưu hóa listing...</p></div>)}
      {error && <div className="error">⚠️ {error}</div>}
      {result && (
        <div className="result">
          <h3>🔍 Nội Dung Tối Ưu SEO</h3>
          {result.seo_title && (<div className="result-section"><h4>Tiêu Đề SEO</h4><p><strong>{result.seo_title}</strong></p><button className="copy-btn" onClick={() => copyToClipboard(result.seo_title!, 'title')}>{copied === 'title' ? '✓ Đã sao chép!' : '📋 Sao chép'}</button></div>)}
          {result.caption && (<div className="result-section"><h4>Caption / Mô Tả Ngắn</h4><p>{result.caption}</p><button className="copy-btn" onClick={() => copyToClipboard(result.caption!, 'caption')}>{copied === 'caption' ? '✓ Đã sao chép!' : '📋 Sao chép'}</button></div>)}
          {result.hashtags && result.hashtags.length > 0 && (<div className="result-section"><h4>Hashtags</h4><div className="hashtags">{result.hashtags.map((h, i) => <span key={i} className="hashtag">#{h}</span>)}</div><button className="copy-btn" onClick={() => copyToClipboard(result.hashtags!.map(h => '#' + h).join(' '), 'tags')}>{copied === 'tags' ? '✓ Đã sao chép!' : '📋 Sao chép Tất cả'}</button></div>)}
          {result.seo_keywords && result.seo_keywords.length > 0 && (<div className="result-section"><h4>Từ Khóa SEO Dài</h4><div className="hashtags">{result.seo_keywords.map((k, i) => <span key={i} className="hashtag">{k}</span>)}</div></div>)}
        </div>
      )}
    </div>
  );
}
