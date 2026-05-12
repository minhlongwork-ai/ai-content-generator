# Database Configuration

## Environment Variables

Add to your `.env` file:

```bash
# PostgreSQL Database URL
DATABASE_URL=postgresql://username:password@host:port/database_name

# Example for local development
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_content_generator

# Example for Render.com (they provide this automatically)
# DATABASE_URL=postgresql://user:pass@dpg-xxxxx.oregon-postgres.render.com/dbname
```

## Setup Instructions

### 1. Local Development (PostgreSQL)

Install PostgreSQL:
```bash
# macOS
brew install postgresql
brew services start postgresql

# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql

# Windows
# Download from https://www.postgresql.org/download/windows/
```

Create database:
```bash
# Connect to PostgreSQL
psql postgres

# Create database
CREATE DATABASE ai_content_generator;

# Create user (optional)
CREATE USER ai_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ai_content_generator TO ai_user;

# Exit
\q
```

### 2. Initialize Database

Run migration:
```bash
cd backend

# Option 1: Run SQL migration directly
psql -U postgres -d ai_content_generator -f migrations/001_add_skill_system_tables.sql

# Option 2: Use Python script (creates tables + seeds data)
python3 database.py
```

### 3. Verify Setup

```bash
# Connect to database
psql -U postgres -d ai_content_generator

# List tables
\dt

# Check skills table
SELECT name, category, is_premium FROM skills;

# Exit
\q
```

Expected output:
```
         name          |    category     | is_premium 
-----------------------+-----------------+------------
 product-description   | e-commerce      | f
 caption-seo           | e-commerce      | f
 ad-copy               | marketing       | f
 video-script          | video-marketing | f
```

## Production Deployment (Render.com)

### 1. Create PostgreSQL Database

1. Go to Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Configure:
   - Name: `ai-content-generator-db`
   - Database: `ai_content_generator`
   - User: (auto-generated)
   - Region: Same as your web service
   - Plan: Free or Starter

4. Copy the **Internal Database URL** (starts with `postgresql://`)

### 2. Add to Web Service

1. Go to your web service settings
2. Environment → Add Environment Variable:
   - Key: `DATABASE_URL`
   - Value: (paste Internal Database URL)

3. Save changes (triggers redeploy)

### 3. Run Migration

Option A: Manual (one-time):
```bash
# SSH into Render shell (from dashboard)
cd backend
python3 database.py
```

Option B: Automatic (on every deploy):

Add to `render.yaml`:
```yaml
services:
  - type: web
    name: ai-content-generator-api
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "cd backend && python3 database.py && gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT"
```

Or add to `build.sh`:
```bash
#!/bin/bash
pip install -r requirements.txt
cd backend && python3 database.py
```

## Database Schema

### Tables

1. **skills** - Available content generation skills
2. **user_skill_configs** - Per-user skill customizations
3. **generations** - Generation history with quality scores
4. **skill_purchases** - Marketplace transactions
5. **skill_analytics** - Usage tracking events

### Views

1. **skill_usage_stats** - Aggregated usage statistics per skill
2. **user_generation_summary** - Per-user generation summary
3. **skill_revenue** - Revenue tracking for premium skills

## Maintenance

### Backup Database

```bash
# Local
pg_dump -U postgres ai_content_generator > backup.sql

# Restore
psql -U postgres ai_content_generator < backup.sql
```

### Reset Database

```bash
# Drop all tables
psql -U postgres -d ai_content_generator -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Re-run migration
python3 database.py
```

### View Analytics

```sql
-- Skill usage stats
SELECT * FROM skill_usage_stats;

-- User generation summary
SELECT * FROM user_generation_summary WHERE user_id = 1;

-- Revenue
SELECT * FROM skill_revenue;

-- Recent generations
SELECT 
    id, 
    user_id, 
    skill_name, 
    quality_score->>'score' as quality_score,
    created_at
FROM generations
ORDER BY created_at DESC
LIMIT 10;
```

## Troubleshooting

### Connection refused

```bash
# Check PostgreSQL is running
brew services list  # macOS
sudo systemctl status postgresql  # Linux

# Check connection
psql -U postgres -d ai_content_generator -c "SELECT 1;"
```

### Permission denied

```bash
# Grant permissions
psql postgres
GRANT ALL PRIVILEGES ON DATABASE ai_content_generator TO your_user;
\q
```

### Table already exists

This is normal - the migration script uses `CREATE TABLE IF NOT EXISTS`.

### Render deployment fails

1. Check DATABASE_URL is set correctly
2. Check database is in same region as web service
3. Use **Internal Database URL** (not External)
4. Check logs: `render logs -s your-service-name`

## Dependencies

Add to `requirements.txt`:
```
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
```

Install:
```bash
pip install sqlalchemy psycopg2-binary
```
