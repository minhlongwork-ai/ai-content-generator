/* src/components/QualityReport.tsx — Hiển thị Quality Score từ Skill System */
import { IconCheck, IconSparkles, IconTrendingUp } from './Icons';

interface QualityCheck {
  name: string;
  passed: boolean;
  message?: string;
}

interface QualityReportProps {
  score: number;              // 0-100
  checks?: QualityCheck[];   // danh sách các check đã chạy
  skillName?: string;        // tên skill đã dùng
  compact?: boolean;         // mode thu gọn (dùng trong tool page)
}

function ScoreRing({ score }: { score: number }) {
  const radius = 36;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  const color =
    score >= 80 ? '#22c55e' :   // green
    score >= 60 ? '#f59e0b' :   // yellow
    '#ef4444';                   // red

  return (
    <div className="quality-score-ring">
      <svg width="96" height="96" viewBox="0 0 96 96">
        {/* Track */}
        <circle
          cx="48" cy="48" r={radius}
          fill="none"
          stroke="rgba(255,255,255,0.08)"
          strokeWidth="8"
        />
        {/* Progress */}
        <circle
          cx="48" cy="48" r={radius}
          fill="none"
          stroke={color}
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          transform="rotate(-90 48 48)"
          style={{ transition: 'stroke-dashoffset 0.8s ease' }}
        />
      </svg>
      <div className="score-number" style={{ color }}>
        {score}
      </div>
    </div>
  );
}

function ScoreLabel({ score }: { score: number }) {
  if (score >= 90) return <span className="score-label excellent">Xuất Sắc ✨</span>;
  if (score >= 80) return <span className="score-label good">Tốt ✅</span>;
  if (score >= 60) return <span className="score-label fair">Khá 📝</span>;
  return <span className="score-label poor">Cần Cải Thiện ⚠️</span>;
}

export default function QualityReport({ score, checks = [], skillName, compact = false }: QualityReportProps) {
  const passed = checks.filter(c => c.passed).length;
  const total = checks.length;

  if (compact) {
    // Mode thu gọn: chỉ hiện score badge nhỏ
    const color = score >= 80 ? 'green' : score >= 60 ? 'yellow' : 'red';
    return (
      <div className={`quality-badge quality-badge-${color}`}>
        <IconSparkles size={12} />
        <span>Điểm chất lượng: <strong>{score}/100</strong></span>
        {total > 0 && <span className="quality-badge-checks">{passed}/{total} checks</span>}
      </div>
    );
  }

  return (
    <div className="quality-report">
      {/* Header */}
      <div className="quality-report-header">
        <div className="quality-score-area">
          <ScoreRing score={score} />
          <div className="quality-meta">
            <h3>Báo Cáo Chất Lượng</h3>
            <ScoreLabel score={score} />
            {skillName && (
              <span className="quality-skill-badge">
                <IconSparkles size={12} /> {skillName}
              </span>
            )}
          </div>
        </div>

        {total > 0 && (
          <div className="quality-stats-row">
            <div className="quality-stat">
              <span className="quality-stat-val green">{passed}</span>
              <span className="quality-stat-label">Đạt</span>
            </div>
            <div className="quality-stat">
              <span className="quality-stat-val red">{total - passed}</span>
              <span className="quality-stat-label">Chưa đạt</span>
            </div>
            <div className="quality-stat">
              <span className="quality-stat-val">{total}</span>
              <span className="quality-stat-label">Tổng checks</span>
            </div>
          </div>
        )}
      </div>

      {/* Check list */}
      {checks.length > 0 && (
        <div className="quality-checks">
          <div className="quality-checks-title">Chi Tiết Kiểm Tra</div>
          <div className="quality-checks-list">
            {checks.map((check, i) => (
              <div key={i} className={`quality-check-item ${check.passed ? 'passed' : 'failed'}`}>
                <span className="check-icon">
                  {check.passed ? <IconCheck size={14} /> : '✗'}
                </span>
                <div className="check-info">
                  <span className="check-name">{check.name}</span>
                  {check.message && (
                    <span className="check-message">{check.message}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tips nếu score thấp */}
      {score < 80 && (
        <div className="quality-tips">
          <div className="quality-tips-title">
            <IconTrendingUp size={14} /> Gợi ý cải thiện
          </div>
          <ul>
            {score < 60 && <li>Cung cấp thêm thông tin chi tiết về sản phẩm</li>}
            <li>Thử chọn phong cách khác (tone) phù hợp hơn</li>
            <li>Thêm tính năng nổi bật và đối tượng mục tiêu rõ ràng</li>
          </ul>
        </div>
      )}
    </div>
  );
}
