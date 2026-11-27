# FrontierAtlas AI — Cloud Deployment & Production Operations Guide

## 1. Production Architecture Overview

The FrontierAtlas AI platform is designed for zero-friction cloud deployment using modern serverless frontend hosting (Vercel) coupled with containerized or PaaS Python backend hosting (Render, Railway, or Fly.io).

```
[User Browser]
      │
      ▼ (HTTPS)
[Vercel Global Edge CDN]
  └─ Next.js 14 Web Application (Static SSR / RSC)
      │
      ▼ (REST JSON / CORS)
[Render / Railway / Fly.io Application Service]
  └─ FastAPI (Python 3.11+, Uvicorn Async Workers)
      │
      ▼ (ACID Read / Write)
[Persistent Storage Layer]
  ├─ Embedded SQLite with persistent volume mount (or)
  └─ Managed PostgreSQL (Neon / Supabase / AWS RDS)
```

---

## 2. Option A: Cloud Deployment (Vercel + Render) [Recommended]

### 2.1 Backend Deployment on Render
1. **Repository Setup:** Ensure your GitHub repository is connected to [Render](https://render.com).
2. **New Web Service:**
   - **Environment:** `Python`
   - **Root Directory:** `.` (repository root)
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free or Starter
3. **Environment Variables on Render:**
   - `PYTHON_VERSION`: `3.11.9`
   - `DATABASE_URL`: `sqlite:///data/frontier_atlas.db` (or connection string to PostgreSQL)
   - `CORS_ORIGINS`: `https://frontieratlas-frontend.vercel.app,http://localhost:3000`
4. **Copy Public Backend URL:** (e.g. `https://frontieratlas-api.onrender.com`).

### 2.2 Frontend Deployment on Vercel
1. **New Project on Vercel:** Import your GitHub repository into [Vercel](https://vercel.com).
2. **Root Directory Configuration:** Set **Root Directory** to `frontend`.
3. **Framework Preset:** `Next.js` (automatically detected).
4. **Build & Output Settings:**
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Install Command: `npm install`
5. **Environment Variables:**
   - `NEXT_PUBLIC_API_BASE_URL`: `https://frontieratlas-api.onrender.com` (your backend URL)
6. **Deploy:** Click **Deploy**. Vercel will build and assign an SSL-enabled production URL (e.g., `https://frontieratlas-frontend.vercel.app/`).

---

## 3. Option B: Containerized Deployment (Docker & Docker Compose)

A complete production `Dockerfile` and `docker-compose.yml` are provided in the repository root for self-hosted or Kubernetes environments.

### 3.1 Dockerfile Build & Execution
```bash
# Build the multi-stage unified production image
docker build -t frontieratlas-ai:latest .

# Run container with volume mount for persistent data
docker run -d \
  -p 8000:8000 \
  -p 3000:3000 \
  -v $(pwd)/data:/app/data \
  --name frontieratlas-prod \
  frontieratlas-ai:latest
```

### 3.2 Docker Compose
```bash
# Launch both backend and frontend services with persistent networking
docker compose up -d --build

# Verify container health
docker compose ps
docker compose logs -f
```

---

## 4. Option C: Local Production Verification

To run both services locally in production mode on a developer workstation:

```bash
# Terminal 1: Launch FastAPI Backend
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000

# Terminal 2: Build & Launch Next.js Frontend
cd frontend
npm install
npm run build
npm run start
```
- Frontend: `http://localhost:3000`
- Backend API Docs: `http://localhost:8000/docs`

---

## 5. Continuous Deployment & Health Monitoring

- **Health Endpoint:** `GET /api/v1/health` provides automatic uptime pinging for Render/K8s liveness probes.
- **Rollback Strategy:** Git branch-based deployments trigger automatic atomic deployments; rolling back the `master` commit restores the previous verified image within seconds.
- **Data Persistence:** If using SQLite in production, attach a persistent disk volume to `/app/data` to ensure crawled records and logs persist across container restarts.
