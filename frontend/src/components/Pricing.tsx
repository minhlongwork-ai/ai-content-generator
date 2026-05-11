/* src/components/Pricing.tsx — Subscription Plans with Stripe Checkout */
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
    name: 'Free',
    price: '0',
    period: 'forever',
    description: 'Perfect for trying out',
    features: [
      '5 generations/day',
      'Product descriptions',
      'Caption & SEO',
      'Ad copy (1 variation)',
      'Free AI models only',
      'Community support',
    ],
    cta: 'Current Plan',
    popular: false,
    disabled: false,
  },
  {
    id: 'pro',
    name: 'Pro',
    price: '299K',
    period: '/month',
    description: 'For serious sellers',
    features: [
      'Unlimited text generation',
      'All content types',
      'Ad copy (3 variations)',
      'Video scripts + TTS',
      'All AI models (free + paid)',
      'Priority support',
      'Export to CSV/JSON',
      'API access',
    ],
    cta: 'Upgrade to Pro',
    popular: true,
    disabled: false,
  },
  {
    id: 'business',
    name: 'Business',
    price: '599K',
    period: '/month',
    description: 'For teams & agencies',
    features: [
      'Everything in Pro',
      'AI video generation',
      'Bulk generation (CSV upload)',
      'Team members (up to 5)',
      'White-label option',
      'Dedicated support',
      'Custom integrations',
      'Usage analytics',
    ],
    cta: 'Upgrade to Business',
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
      showToast('warning', 'Please sign in to upgrade');
      onSelectPlan('auth');
      return;
    }

    if (userPlan === planId) {
      showToast('info', 'You are already on this plan');
      return;
    }

    setLoading(planId);
    try {
      const res = await fetch(`${API_URL}/api/payment/checkout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ plan: planId }),
      });

      const data = await res.json();

      if (data.checkout_url) {
        window.location.href = data.checkout_url;
      } else if (data.error) {
        if (data.available === false) {
          showToast('info', 'Stripe not configured yet. Contact admin to upgrade.');
        } else {
          showToast('error', data.error);
        }
      }
    } catch (err: any) {
      showToast('error', 'Failed to create checkout session');
    } finally {
      setLoading(null);
    }
  };

  return (
    <div className="pricing-page">
      <div className="pricing-header">
        <h1>Simple, Transparent Pricing</h1>
        <p>Start free. Scale when you're ready.</p>

        <div className="pricing-toggle">
          <span className={!annual ? 'active' : ''}>Monthly</span>
          <button
            className={`toggle-switch ${annual ? 'annual' : ''}`}
            onClick={() => setAnnual(!annual)}
          >
            <div className="toggle-knob" />
          </button>
          <span className={annual ? 'active' : ''}>
            Annual <span className="save-badge">Save 20%</span>
          </span>
        </div>
      </div>

      <div className="pricing-grid">
        {plans.map((plan) => {
          const isCurrentPlan = userPlan === plan.id;
          return (
            <div
              key={plan.id}
              className={`pricing-card ${plan.popular ? 'popular' : ''} ${isCurrentPlan ? 'current' : ''}`}
            >
              {plan.popular && <div className="popular-badge">⭐ Most Popular</div>}
              {isCurrentPlan && <div className="current-badge">✓ Current Plan</div>}
              <div className="plan-name">{plan.name}</div>
              <div className="plan-description">{plan.description}</div>
              <div className="plan-price">
                <span className="currency">₫</span>
                <span className="amount">
                  {annual && plan.price !== '0'
                    ? Math.round(parseInt(plan.price.replace('K', '')) * 0.8) + 'K'
                    : plan.price}
                </span>
                <span className="period">{plan.period}</span>
              </div>
              <ul className="plan-features">
                {plan.features.map((feature, i) => (
                  <li key={i}>
                    <span className="check">✓</span>
                    {feature}
                  </li>
                ))}
              </ul>
              <button
                className={`btn-pricing ${plan.popular ? 'btn-popular' : ''} ${isCurrentPlan ? 'btn-current' : ''}`}
                onClick={() => handleSelectPlan(plan.id)}
                disabled={plan.disabled || isCurrentPlan || loading === plan.id}
              >
                {loading === plan.id ? '⏳ Processing...' : isCurrentPlan ? '✓ Current Plan' : plan.cta}
              </button>
            </div>
          );
        })}
      </div>

      {/* FAQ */}
      <div className="pricing-faq">
        <h2>Frequently Asked Questions</h2>
        <div className="faq-grid">
          <div className="faq-item">
            <h4>Can I cancel anytime?</h4>
            <p>Yes. No contracts, no hidden fees. Cancel with one click from your settings.</p>
          </div>
          <div className="faq-item">
            <h4>What payment methods do you accept?</h4>
            <p>International cards via Stripe (Visa, Mastercard, Amex). Vietnamese bank transfer coming soon.</p>
          </div>
          <div className="faq-item">
            <h4>Is there a free trial?</h4>
            <p>The Free plan is always free — 5 generations/day. No credit card required.</p>
          </div>
          <div className="faq-item">
            <h4>Can I switch plans later?</h4>
            <p>Yes. Upgrade or downgrade anytime. Changes take effect immediately.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
