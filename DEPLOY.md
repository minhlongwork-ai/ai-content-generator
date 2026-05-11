# 🚀 Deployment Guide — AI Content Generator

## Architecture

- **Frontend:** React + Vite → Deploy on Vercel
- **Backend:** Python FastAPI → Deploy on Render
- **Auth:** JWT (user self-registers, brings own OpenRouter API key)
- **Payment:** Stripe (optional — for subscription upgrades)

## Step 1: Deploy Backend (Render)

1. Go to https://dashboard.render.com → Sign in with GitHub
2. Click **"New +"** → **"Web Service"**
3. Connect repo: `minhlongwork-ai/ai-content-generator`
4. Configure:
   - **Name:** `ai-content-generator-api`
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variables:
   ```
   JWT_SECRET=your_random_secret_here_min_32_chars
   ```
6. Click **"Create Web Service"**
7. Wait for deploy → copy the URL (e.g., `https://ai-content-generator-api.onrender.com`)

## Step 2: Deploy Frontend (Vercel)

1. Go to https://vercel.com → Sign in with GitHub
2. Click **"Add New"** → **"Project"**
3. Import repo: `minhlongwork-ai/ai-content-generator`
4. Configure:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
5. Add Environment Variable:
   ```
   VITE_API_URL=https://ai-content-generator-api.onrender.com
   ```
6. Click **"Deploy"**
7. Wait for deploy → copy the URL (e.g., `https://ai-content-generator.vercel.app`)

## Step 3: Stripe Setup (Optional — for paid subscriptions)

1. Go to https://stripe.com → create account
2. Get API keys from Dashboard → Developers → API keys
3. Add to Render Environment Variables:
   ```
   STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxx
   STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxx
   ```
4. In Stripe Dashboard → Developers → Webhooks → Add endpoint:
   - URL: `https://ai-content-generator-api.onrender.com/api/payment/webhook`
   - Events: `checkout.session.completed`, `customer.subscription.deleted`

## Step 4: Update Frontend URL (if needed)

If you change the backend URL, update `VITE_API_URL` in Vercel and redeploy.

## How It Works

1. User visits landing page → clicks "Start Free"
2. User registers account (email + password)
3. User adds their OpenRouter API key in Settings
4. User generates content → API calls use THEIR key
5. User upgrades to Pro/Business via Stripe → unlimited generations

## Cost

- **OpenRouter:** User pays for their own API usage
- **Render:** Free tier (enough for demo)
- **Vercel:** Free tier (enough for demo)
- **Stripe:** No monthly fee, only transaction fees (2.9% + $0.30)

## Custom Domain (Optional)

- Vercel: Settings → Domains → Add your domain
- Render: Settings → Custom Domains → Add your domain
