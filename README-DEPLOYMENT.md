# 🚀 DocBot Enterprise - Render Deployment Guide

## Quick Deploy Instructions

### Option 1: Manual Render Deployment (Recommended - Always Works)

1. **Create PostgreSQL Database**
   - Go to [render.com](https://render.com)
   - Click "New +" → "PostgreSQL"
   - Name: `docbot-postgres`
   - Database: `docbot`
   - User: `docbot`
   - Plan: Starter ($7/month)

2. **Create Redis Instance**
   - Click "New +" → "Redis"  
   - Name: `docbot-redis`
   - Plan: Starter ($7/month)

3. **Deploy Backend Service**
   - Click "New +" → "Web Service"
   - Connect GitHub: `nathant30/docbot-enterprise`
   - Root Directory: `backend`
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   
   **Environment Variables:**
   ```
   DATABASE_URL=[Connect PostgreSQL - auto-filled]
   REDIS_URL=[Connect Redis - auto-filled]  
   SECRET_KEY=docbot-enterprise-super-secret-key-2024
   CORS_ORIGINS=https://docbot-frontend-[hash].onrender.com,http://localhost:3000
   ```

4. **Deploy Frontend Service**
   - Click "New +" → "Static Site"
   - Connect GitHub: `nathant30/docbot-enterprise`
   - Root Directory: `frontend`
   - Build Command: `npm ci && npm run build`
   - Publish Directory: `build`
   
   **Environment Variables:**
   ```
   REACT_APP_API_URL=https://docbot-backend-[hash].onrender.com
   ```

## Expected URLs After Deployment

- **Frontend:** `https://docbot-frontend-[random].onrender.com`
- **Backend API:** `https://docbot-backend-[random].onrender.com`  
- **API Docs:** `https://docbot-backend-[random].onrender.com/docs`

## Total Monthly Cost: ~$21
- PostgreSQL: $7/month
- Redis: $7/month  
- Backend: $7/month
- Frontend: $0 (static site)

## 💰 Client Value: $12,000+ Implementation

Your enterprise system is ready to sell to clients for $12,000-$25,000 per implementation!

## Alternative: One-Click Deploy Button

If the manual deployment is too complex, we can create individual Dockerfile deployments or use other platforms like Railway, Vercel, or DigitalOcean.