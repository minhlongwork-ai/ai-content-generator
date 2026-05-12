# Production Deploy Guide — AI Content Generator v2.1 (Skill System)

Bản cập nhật này bao gồm **Skill-based Architecture** và **Marketplace**. Để hệ thống hoạt động trên Production, bạn cần thực hiện các bước sau:

## 1. Cấu hình Backend (Render.com)

### Biến môi trường (Environment Variables)
Hãy đảm bảo các biến sau đã được thiết lập trên Render Dashboard:
- `DATABASE_URL`: URL của Render Postgres (ví dụ: `postgres://user:pass@host/db`).
- `JWT_SECRET`: Khóa bí mật để tạo token (nên đổi so với bản dev).
- `STRIPE_SECRET_KEY`: Lấy từ Stripe Dashboard (để bán premium skills).
- `AI_BACKEND`: `openrouter`
- `OPENROUTER_API_KEY`: Key của bạn.

### Chạy Migration Database
Vì production dùng Postgres, bạn cần chạy 2 file SQL sau vào database của Render (có thể dùng tab "Shell" trên Render hoặc công cụ `psql` từ máy tính):
1. `backend/migrations/001_add_skill_system_tables.sql`
2. `backend/migrations/002_add_marketplace_tables.sql`

Hoặc chạy lệnh sau từ máy local (nếu đã cài `psql`):
```bash
psql $DATABASE_URL -f backend/migrations/001_add_skill_system_tables.sql
psql $DATABASE_URL -f backend/migrations/002_add_marketplace_tables.sql
```

## 2. Cấu hình Frontend (Vercel)

Vercel sẽ tự động deploy khi nhận được code mới trên nhánh `main`.
Đảm bảo biến môi trường `VITE_API_URL` trỏ về domain backend của Render.

## 3. Seed dữ liệu Marketplace
Sau khi deploy backend thành công, bạn có thể chạy script seed để tạo danh sách skill trên marketplace:
```bash
# Trên Render Shell
python backend/seed_marketplace.py
```

---
*Lưu ý: SQLite chỉ dùng để test local. Production BẮT BUỘC dùng Postgres để đảm bảo dữ liệu không bị mất khi restart server.*
