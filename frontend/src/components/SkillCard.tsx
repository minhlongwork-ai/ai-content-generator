/* src/components/SkillCard.tsx — Card hiển thị một skill trong marketplace */
import { IconCheck } from './Icons';

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
    <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>
      <span style={{ color: '#ffbd2e' }}>★</span>
      <span>{rating.toFixed(1)}</span>
      <span>({count})</span>
    </div>
  );
}

function CategoryLabel({ category }: { category: string }) {
  const map: Record<string, string> = {
    ecommerce: '🛒 E-commerce',
    'social-media': '📱 Social Media',
    advertising: '🎯 Advertising',
    video: '🎬 Video',
  };
  return <span className="skill-category-badge">{map[category] || category}</span>;
}

export default function SkillCard({ listing, onClick, onInstall, installing }: SkillCardProps) {
  return (
    <div className={`skill-card-modern ${listing.is_featured ? 'is-featured' : ''}`} onClick={() => onClick?.(listing)}>
      <div className="skill-card-icon-wrap">
        <span style={{ fontSize: '1.5rem' }}>{listing.cover_emoji || '🤖'}</span>
      </div>
      
      <div className="skill-card-content">
        <div className="skill-card-header">
          <h3 className="skill-title-text">{listing.title}</h3>
          <CategoryLabel category={listing.category} />
        </div>
        
        <p className="skill-desc-text">{listing.short_desc}</p>
        
        <div className="skill-card-footer">
          <StarRating rating={listing.avg_rating} count={listing.rating_count} />
          
          <div className="skill-action-area" onClick={e => e.stopPropagation()}>
            {listing.is_installed ? (
              <div className="installed-indicator"><IconCheck size={14} /></div>
            ) : (
              <button 
                className="btn-install-small"
                onClick={() => onInstall?.(listing)}
                disabled={installing}
              >
                {installing ? '...' : (listing.price === 0 ? 'Free' : `$${listing.price}`)}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
