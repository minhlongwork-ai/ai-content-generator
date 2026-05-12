/* src/components/SkillCard.tsx — Card hiển thị một skill trong marketplace */

import { IconSparkles, IconCheck } from './Icons';

export interface SkillListing {
  skill_name: string;
  title: string;
  short_desc: string;
  long_desc?: string;
  price: number;
  currency?: string;
  category: string;
  tags: string[];
  author_name: string;
  is_active: boolean;
  is_featured: boolean;
  is_premium?: boolean;
  coming_soon?: boolean;
  total_sales: number;
  avg_rating: number;
  rating_count: number;
  cover_emoji?: string;
  is_installed?: boolean;
}

interface SkillCardProps {
  listing: SkillListing;
  onClick?: (listing: SkillListing) => void;
  onInstall?: (listing: SkillListing) => void;
  installing?: boolean;
}

function StarRating({ rating, count }: { rating: number; count: number }) {
  return (
    <div className="skill-rating">
      {[1, 2, 3, 4, 5].map((s) => (
        <span key={s} className={`star ${s <= Math.round(rating) ? 'filled' : ''}`}>★</span>
      ))}
      {count > 0 && <span className="rating-count">({count})</span>}
    </div>
  );
}

function PriceBadge({ price, currency = 'USD', isPremium, comingSoon }: {
  price: number;
  currency?: string;
  isPremium?: boolean;
  comingSoon?: boolean;
}) {
  if (comingSoon) {
    return <span className="price-badge coming-soon">Sắp Ra Mắt</span>;
  }
  if (price === 0) {
    return <span className="price-badge free">Miễn Phí</span>;
  }
  return (
    <span className="price-badge premium">
      {currency === 'USD' ? '$' : currency}{price.toFixed(2)}
      {isPremium && ' ✦'}
    </span>
  );
}

function CategoryLabel({ category }: { category: string }) {
  const map: Record<string, { label: string; color: string }> = {
    ecommerce:    { label: '🛒 E-commerce',   color: 'blue' },
    'social-media': { label: '📱 Social Media', color: 'pink' },
    advertising:  { label: '🎯 Advertising',  color: 'red' },
    video:        { label: '🎬 Video',        color: 'green' },
  };
  const cat = map[category] || { label: category, color: 'gray' };
  return <span className={`category-label category-${cat.color}`}>{cat.label}</span>;
}

export default function SkillCard({ listing, onClick, onInstall, installing }: SkillCardProps) {
  const isFree = listing.price === 0 && !listing.is_premium;

  return (
    <div
      className={`skill-card ${listing.is_featured ? 'featured' : ''} ${listing.coming_soon ? 'coming-soon-card' : ''}`}
      onClick={() => onClick?.(listing)}
    >
      {/* Featured ribbon */}
      {listing.is_featured && !listing.coming_soon && (
        <div className="skill-card-ribbon">⭐ Nổi Bật</div>
      )}

      {/* Cover */}
      <div className="skill-card-cover">
        <span className="skill-card-emoji">{listing.cover_emoji || '🤖'}</span>
        <div className="skill-card-overlay">
          <CategoryLabel category={listing.category} />
        </div>
      </div>

      {/* Body */}
      <div className="skill-card-body">
        <div className="skill-card-top">
          <h3 className="skill-card-title">{listing.title}</h3>
          <PriceBadge
            price={listing.price}
            currency={listing.currency}
            isPremium={listing.is_premium}
            comingSoon={listing.coming_soon}
          />
        </div>

        <p className="skill-card-desc">{listing.short_desc}</p>

        {/* Tags */}
        <div className="skill-card-tags">
          {listing.tags.slice(0, 3).map((tag) => (
            <span key={tag} className="skill-tag">#{tag}</span>
          ))}
        </div>

        {/* Footer */}
        <div className="skill-card-footer">
          <StarRating rating={listing.avg_rating} count={listing.rating_count} />

          <div className="skill-card-action" onClick={(e) => e.stopPropagation()}>
            {listing.is_installed ? (
              <span className="installed-badge">
                <IconCheck size={13} /> Đã Cài
              </span>
            ) : listing.coming_soon ? (
              <button className="btn-skill btn-skill-disabled" disabled>
                Sắp Có
              </button>
            ) : isFree ? (
              <button
                className="btn-skill btn-skill-install"
                disabled={installing}
                onClick={() => onInstall?.(listing)}
              >
                {installing ? (
                  <><span className="spinner-tiny" /> Đang cài...</>
                ) : (
                  <><IconSparkles size={13} /> Cài Miễn Phí</>
                )}
              </button>
            ) : (
              <button
                className="btn-skill btn-skill-buy"
                onClick={() => onInstall?.(listing)}
              >
                Mua ${listing.price}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
