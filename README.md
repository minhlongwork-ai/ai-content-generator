# 🚀 AI Content Generator

Generate high-converting e-commerce content with AI.

## Features

- 📝 **Product Description** — Headline, bullets, description, SEO keywords
- 🔍 **Caption & SEO** — Optimized titles, captions, hashtags
- 🎯 **Ad Copy** — 3 variations (PAS, BAB, Story styles)

## Tech Stack

- **Backend:** Python FastAPI + OpenRouter API (free models)
- **Frontend:** React + TypeScript + Vite
- **Deploy:** Render (backend) + Vercel (frontend)

## Quick Start

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set your OpenRouter API key
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY

uvicorn main:app --reload
```

Backend runs at `http://localhost:8000`

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

### 3. Test

Open `http://localhost:5173` in browser and try generating content!

## Deploy

### Backend (Render)

1. Push to GitHub
2. Create new Web Service on Render
3. Connect repo → `backend/` directory
4. Set env var: `OPENROUTER_API_KEY`
5. Deploy!

### Frontend (Vercel)

1. Push to GitHub
2. Import project on Vercel
3. Set root directory: `frontend/`
4. Set env var: `VITE_API_URL` = your Render URL
5. Deploy!

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/generate/product-description` | POST | Generate product description |
| `/api/generate/caption-seo` | POST | Generate SEO caption |
| `/api/generate/ad-copy` | POST | Generate ad copy variations |

## Free Models (Auto-fallback)

1. `google/gemini-2.0-flash-exp:free`
2. `google/gemini-2.0-flash-lite-preview-02-05:free`
3. `qwen/qwen-vl-plus:free`
4. `openchat/openchat-7b:free`
5. `meta-llama/llama-3.1-8b-instruct:free`

## License

MIT
