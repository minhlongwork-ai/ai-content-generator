/* src/components/Pricing.tsx — Bảng giá (Tiếng Việt) */
import { useState } from 'react';
import { showToast } from './Toast';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface PricingProps {
  onSelectPlan: (plan: string) => void;
  userPlan?: string;
  token?: string;
}

const plans = [
  {
    id: 'free',
    name: 'Miễn Phí',
    price: '0',
    period: 'mãi mãi',
    description: 'Phù hợp để thử nghiệm',
    features: [
      '5 lần tạo/ngày',
      'Mô tả sản phẩm',
      'Caption & SEO',
      'Quảng cáo (1 phiên bản)',
      'Chỉ mô hình AI miễn phí',
      'Hỗ trợ cộng đồng',
    ],
    cta: 'Gói Hiện Tại',
    popular: false,
    disabled: false,
  },
  {
    id: 'pro',
    name: 'Pro',
    price: '299K',
    period: '/tháng',
    description: 'Cho người bán nghiêm túc',
    features: [
      'Tạo nội dung không giới hạn',
      'Tất cả loại nội dung',
      'Quảng cáo (3 phiên bản)',
      'Kịch bản video + TTS',
      'Tất cả mô hình AI (miễn phí + trả phí)',
      'Hỗ trợ ưu tiên',
      'Xuất CSV/JSON',
      'Truy cập API',
    ],
    cta: 'Nâng Cấp Pro',
    popular: true,
    disabled: false,
  },
  {
    id: 'business',
    name: 'Doanh Nghiệp',
    price: '599K',
    period: '/tháng',
    description: 'Cho đội nhóm & công ty',
    features: [
      'Tất cả trong Pro',
      'Tạo video AI',
      'Tạo hàng loạt (CSV)',
      'Thành viên nhóm (tối đa 5)',
      'Tùy chỉnh nhãn hiệu',
      'Hỗ trợ riêng',
      'Tích hợp tùy chỉnh',
      'Thống kê sử dụng',
    ],
    cta: 'Nâng Cấp Doanh Nghiệp',
    popular: false,
    disabled: false,
  },
];

export default function Pricing({ onSelectPlan, userPlan, token }: PricingProps) {
  const [annual, setAnnual] = useState(false);
  const [loading, setLoading] = useState<string | null>(null);

  const handleSelectPlan = async (planId: string) => {
    if (planId === 'free') return;
    if (!token) {
      showToast('warning', 'Vui lòng đăng nhập để nâng cấp');
      onSelectPlan('auth');
      return;
    }
    if (userPlan === planId) {
      showToast('info', 'Bạn đang ở gói này');
      return;
    }
    setLoading(planId);
    try {
      const res = await fetch(`${API_URL}/api/payment/checkout`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({ plan: planId }),
      });
      const data = await res.json();
      if (data.checkout_url) {
        window.location.href = data.checkout_url;
      } else if (data.error) {
        showToast('info', 'Stripe chưa được cấu hình. Liên hệ admin để nâng cấp.');
      }
    } catch (err: any) {
      showToast('error', 'Không thể tạo phiên thanh toán');
    } finally {
      setLoading(null);
    }
  };

  return (
    <div className="pricing-page">
      <div className="pricing-header">
        <h1>Bảng Giá Đơn Giản, Minh Bạch</h1>
        <p>Bắt đầu miễn phí. Nâng cấp khi bạn sẵn sàng.</p>
        <div className="pricing-toggle">
          <span className={!annual ? 'active' : ''}>Hàng tháng</span>
          <button className={`toggle-switch ${annual ? 'annual' : ''}`} onClick={() => setAnnual(!annual)}>
            <div className="toggle-knob" />
          </button>
          <span className={annual ? 'active' : ''}>Hàng năm <span className="save-badge">Tiết kiệm 20%</span></span>
        </div>
      </div>

      <div className="pricing-grid">
        {plans.map((plan) => {
          const isCurrentPlan = userPlan === plan.id;
          return (
            <div key={plan.id} className={`pricing-card ${plan.popular ? 'popular' : ''} ${isCurrentPlan ? 'current' : ''}`}>
              {plan.popular && <div className="popular-badge">⭐ Phổ Biến Nhất</div>}
              {isCurrentPlan && <div className="current-badge">✓ Gói Hiện Tại</div>}
              <div className="plan-name">{plan.name}</div>
              <div className="plan-description">{plan.description}</div>
              <div className="plan-price">
                <span className="currency">₫</span>
                <span className="amount">{annual && plan.price !== '0' ? Math.round(parseInt(plan.price.replace('K', '')) * 0.8) + 'K' : plan.price}</span>
                <span className="period">{plan.period}</span>
              </div>
              <ul className="plan-features">
                {plan.features.map((feature, i) => (
                  <li key={i}><span className="check">✓</span>{feature}</li>
                ))}
              </ul>
              <button
                className={`btn-pricing ${plan.popular ? 'btn-popular' : ''} ${isCurrentPlan ? 'btn-current' : ''}`}
                onClick={() => handleSelectPlan(plan.id)}
                disabled={plan.disabled || isCurrentPlan || loading === plan.id}
              >
                {loading === plan.id ? '⏳ Đang xử lý...' : isCurrentPlan ? '✓ Gói Hiện Tại' : plan.cta}
              </button>
            </div>
          );
        })}
      </div>

      <div className="pricing-faq">
        <h2>Câu Hỏi Thường Gặp</h2>
        <div className="faq-grid">
          <div className="faq-item">
            <h4>Tôi có thể hủy bất cứ lúc nào không?</h4>
            <p>Có. Không hợp đồng, không phí ẩn. Hủy với một click trong cài đặt.</p>
          </div>
          <div className="faq-item">
            <h4>Bạn chấp nhận phương thức thanh toán nào?</h4>
            <p>Thẻ quốc tế qua Stripe (Visa, Mastercard, Amex). Chuyển khoản ngân hàng Việt Nam sắp ra mắt.</p>
          </div>
          <div className="faq-item">
            <h4>Có bản dùng thử miễn phí không?</h4>
            <p>Gói Miễn Phí luôn miễn phí — 5 lần tạo/ngày. Không cần thẻ tín dụng.</p>
          </div>
          <div className="faq-item">
            <h4>Tôi có thể đổi gói sau không?</h4>
            <p>Có. Nâng cấp hoặc hạ gói bất cứ lúc nào. Thay đổi có hiệu lực ngay lập tức.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
