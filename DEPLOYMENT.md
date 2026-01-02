# Production Deployment Guide

Complete step-by-step guide to deploy the Quiz Management System to production.

> 💡 **Looking for FREE options only?** See [DEPLOYMENT_FREE.md](./DEPLOYMENT_FREE.md) for a guide using 100% free services (Render + Vercel).

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Backend Deployment](#backend-deployment)
3. [Frontend Deployment](#frontend-deployment)
4. [Database Setup](#database-setup)
5. [Environment Variables](#environment-variables)
6. [Deployment Platforms](#deployment-platforms)
7. [Post-Deployment Checklist](#post-deployment-checklist)

---

## Prerequisites

- Git repository (GitHub, GitLab, etc.)
- Domain name (optional but recommended)
- PostgreSQL database (production)
- Deployment platform account (Render, Railway, Vercel, etc.)

---

## Backend Deployment

### Option 1: Render.com (Recommended for Backend)

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create PostgreSQL Database**
   - Dashboard → New → PostgreSQL
   - Name: `quizdb-prod`
   - Region: Choose closest to your users
   - PostgreSQL Version: 18
   - Click "Create Database"
   - **Save the Internal Database URL** (you'll need it)

3. **Create Web Service**
   - Dashboard → New → Web Service
   - Connect your GitHub repository
   - Select the repository
   - Configure:
     - **Name**: `quiz-app-backend`
     - **Region**: Same as database
     - **Branch**: `main` (or your production branch)
     - **Root Directory**: `backend`
     - **Environment**: `Python 3`
     - **Build Command**: 
       ```bash
       pip install -r requirements.txt
       ```
     - **Start Command**: 
       ```bash
       gunicorn -w 4 -b 0.0.0.0:$PORT app:app
       ```
     - **Instance Type**: Free tier or paid

4. **Add Environment Variables**
   - Go to Environment tab
   - Add these variables:
     ```
     DATABASE_URL=<your-postgres-internal-url>
     SECRET_KEY=<generate-a-random-secret-key>
     JWT_SECRET_KEY=<generate-a-different-random-secret-key>
     JWT_ACCESS_TOKEN_EXPIRES=3600
     CORS_ORIGINS=https://your-frontend-domain.com
     PORT=10000
     FLASK_ENV=production
     ```
   - Generate secret keys:
     ```bash
     python -c "import secrets; print(secrets.token_urlsafe(32))"
     ```

5. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy automatically
   - Wait for deployment to complete
   - **Save the service URL** (e.g., `https://quiz-app-backend.onrender.com`)

6. **Run Database Migrations**
   - Go to your service → Shell
   - Run:
     ```bash
     flask db upgrade
     python seed.py
     python seed_quizzes.py
     ```

### Option 2: Railway.app

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create New Project**
   - New Project → Deploy from GitHub repo
   - Select your repository

3. **Add PostgreSQL**
   - New → Database → PostgreSQL
   - Railway auto-creates the database

4. **Deploy Backend**
   - New → GitHub Repo → Select repo
   - Set Root Directory: `backend`
   - Railway auto-detects Python
   - Add environment variables (same as Render)
   - Railway will auto-deploy

5. **Run Migrations**
   - Use Railway CLI or web console
   ```bash
   railway run flask db upgrade
   railway run python seed.py
   ```

### Option 3: Heroku

1. **Install Heroku CLI**
   ```bash
   brew install heroku/brew/heroku  # macOS
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create quiz-app-backend
   ```

3. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
   heroku config:set JWT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
   heroku config:set CORS_ORIGINS=https://your-frontend-domain.com
   heroku config:set FLASK_ENV=production
   ```

5. **Create Procfile**
   Create `backend/Procfile`:
   ```
   web: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
   ```

6. **Deploy**
   ```bash
   cd backend
   git add .
   git commit -m "Prepare for production"
   git push heroku main
   ```

7. **Run Migrations**
   ```bash
   heroku run flask db upgrade
   heroku run python seed.py
   ```

---

## Frontend Deployment

### Option 1: Vercel (Recommended for Frontend)

1. **Create Vercel Account**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub

2. **Import Project**
   - Dashboard → Add New → Project
   - Import your GitHub repository
   - Configure:
     - **Framework Preset**: Vite
     - **Root Directory**: `frontend`
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`

3. **Add Environment Variables**
   - Go to Settings → Environment Variables
   - Add:
     ```
     VITE_API_URL=https://your-backend-url.com/api
     ```
   - Update `frontend/src/utils/api.js`:
     ```javascript
     const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001/api';
     ```

4. **Deploy**
   - Click "Deploy"
   - Vercel will build and deploy
   - You'll get a URL like `https://quiz-app.vercel.app`

5. **Custom Domain (Optional)**
   - Settings → Domains
   - Add your domain
   - Follow DNS instructions

### Option 2: Netlify

1. **Create Netlify Account**
   - Go to [netlify.com](https://netlify.com)
   - Sign up with GitHub

2. **Deploy Site**
   - Add new site → Import from Git
   - Select repository
   - Configure:
     - **Base directory**: `frontend`
     - **Build command**: `npm run build`
     - **Publish directory**: `frontend/dist`

3. **Add Environment Variables**
   - Site settings → Environment variables
   - Add `VITE_API_URL`

4. **Deploy**
   - Click "Deploy site"

### Option 3: Render.com (Frontend)

1. **Create Static Site**
   - New → Static Site
   - Connect GitHub repo
   - Configure:
     - **Root Directory**: `frontend`
     - **Build Command**: `npm install && npm run build`
     - **Publish Directory**: `dist`

2. **Add Environment Variables**
   - Same as Vercel

---

## Database Setup

### Production PostgreSQL Configuration

1. **Connection String Format**
   ```
   postgresql://username:password@host:port/database
   ```

2. **Security Best Practices**
   - Use strong passwords
   - Enable SSL connections
   - Restrict IP access if possible
   - Regular backups

3. **Backup Strategy**
   - Automated daily backups (most platforms do this)
   - Manual backup command:
     ```bash
     pg_dump -h host -U username -d database > backup.sql
     ```

---

## Environment Variables

### Backend (.env or Platform Settings)

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# Security (generate strong random keys)
SECRET_KEY=your-very-long-random-secret-key-here
JWT_SECRET_KEY=your-very-long-random-jwt-secret-key-here

# JWT
JWT_ACCESS_TOKEN_EXPIRES=3600

# CORS (your frontend domain)
CORS_ORIGINS=https://your-frontend-domain.com,https://www.your-frontend-domain.com

# Server
PORT=10000
FLASK_ENV=production
```

### Frontend (Build-time Variables)

```bash
# API URL
VITE_API_URL=https://your-backend-domain.com/api
```

**Important**: Vite requires `VITE_` prefix for environment variables.

---

## Update Code for Production

### 1. Update Frontend API URL

Edit `frontend/src/utils/api.js`:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001/api';
```

### 2. Add Gunicorn to Backend

Update `backend/requirements.txt`:

```txt
gunicorn==21.2.0
```

### 3. Create Production Config

Create `backend/config_prod.py` (optional):

```python
import os
from config import Config

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    
    # Force HTTPS in production
    PREFERRED_URL_SCHEME = 'https'
```

### 4. Update CORS for Production

Make sure CORS allows your frontend domain:

```python
# In config.py, CORS_ORIGINS should include production domain
CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
```

---

## Deployment Platforms Comparison

| Platform | Backend | Frontend | Database | Free Tier | Best For |
|----------|---------|----------|----------|-----------|----------|
| **Render** | ✅ | ✅ | ✅ | Yes | Full-stack apps |
| **Railway** | ✅ | ✅ | ✅ | Limited | Quick deployment |
| **Vercel** | ❌ | ✅ | ❌ | Yes | Frontend only |
| **Netlify** | ❌ | ✅ | ❌ | Yes | Frontend only |
| **Heroku** | ✅ | ✅ | ✅ | No | Enterprise |
| **AWS** | ✅ | ✅ | ✅ | Limited | Scalability |
| **DigitalOcean** | ✅ | ✅ | ✅ | No | Control |

---

## Step-by-Step: Complete Deployment (Render + Vercel)

### Step 1: Prepare Backend

1. Add `gunicorn` to `backend/requirements.txt`
2. Create `backend/Procfile` (for Heroku) or use Render's start command
3. Test locally with production settings

### Step 2: Deploy Backend (Render)

1. Push code to GitHub
2. Create Render PostgreSQL database
3. Create Render Web Service
4. Add environment variables
5. Deploy
6. Run migrations: `flask db upgrade`
7. Seed data: `python seed.py`

### Step 3: Deploy Frontend (Vercel)

1. Update `frontend/src/utils/api.js` to use environment variable
2. Push code to GitHub
3. Import to Vercel
4. Set `VITE_API_URL` environment variable
5. Deploy

### Step 4: Update CORS

1. Go to Render backend settings
2. Update `CORS_ORIGINS` with Vercel URL
3. Redeploy backend

### Step 5: Test Production

1. Visit frontend URL
2. Test login
3. Test quiz creation
4. Test quiz taking
5. Check browser console for errors

---

## Post-Deployment Checklist

- [ ] Backend is running and accessible
- [ ] Frontend is deployed and accessible
- [ ] Database migrations completed
- [ ] Admin user created
- [ ] Sample quizzes seeded
- [ ] CORS configured correctly
- [ ] Environment variables set
- [ ] HTTPS enabled (automatic on most platforms)
- [ ] API endpoints working
- [ ] Frontend can connect to backend
- [ ] Login works
- [ ] Quiz creation works
- [ ] Quiz taking works
- [ ] Error handling works
- [ ] Logs are accessible
- [ ] Backups configured

---

## Troubleshooting

### Backend Issues

**Error: Database connection failed**
- Check `DATABASE_URL` is correct
- Verify database is running
- Check firewall/network settings

**Error: CORS blocked**
- Verify `CORS_ORIGINS` includes frontend URL
- Check for trailing slashes
- Ensure HTTPS URLs if using HTTPS

**Error: JWT token invalid**
- Check `JWT_SECRET_KEY` is set
- Verify token is being sent in headers
- Check token expiration

### Frontend Issues

**Error: API calls failing**
- Verify `VITE_API_URL` is set correctly
- Check CORS settings on backend
- Verify backend URL is accessible
- Check browser console for errors

**Error: Build fails**
- Check Node.js version compatibility
- Verify all dependencies installed
- Check for TypeScript/ESLint errors

---

## Security Checklist

- [ ] Strong secret keys (32+ characters, random)
- [ ] HTTPS enabled
- [ ] CORS restricted to your domain
- [ ] Database credentials secure
- [ ] Environment variables not in code
- [ ] Admin password changed from default
- [ ] Rate limiting (consider adding)
- [ ] Input validation on all endpoints
- [ ] SQL injection protection (SQLAlchemy handles this)
- [ ] XSS protection (React handles this)

---

## Monitoring & Maintenance

### Logs
- Render: Dashboard → Logs
- Vercel: Dashboard → Deployments → View Function Logs
- Railway: Dashboard → Deployments → Logs

### Updates
1. Make changes locally
2. Test thoroughly
3. Commit and push to GitHub
4. Platform auto-deploys (or manual deploy)
5. Verify in production

### Database Backups
- Most platforms auto-backup
- Download backups regularly
- Test restore process

---

## Cost Estimation

### Free Tier (Small Projects)
- **Render**: Free tier available (spins down after inactivity)
- **Vercel**: Free tier for frontend
- **Railway**: $5/month minimum
- **Total**: ~$0-5/month

### Paid Tier (Production)
- **Render**: $7/month per service
- **Vercel**: Free tier usually sufficient
- **Database**: $7-20/month
- **Total**: ~$14-27/month

---

## Quick Start Commands

### Local Production Test

```bash
# Backend
cd backend
export DATABASE_URL="postgresql://..."
export SECRET_KEY="..."
export JWT_SECRET_KEY="..."
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5001 app:app

# Frontend
cd frontend
export VITE_API_URL="http://localhost:5001/api"
npm run build
npm run preview
```

---

## Support & Resources

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **Railway Docs**: https://docs.railway.app
- **Flask Deployment**: https://flask.palletsprojects.com/en/latest/deploying/
- **Vite Deployment**: https://vitejs.dev/guide/static-deploy.html

---

## Next Steps After Deployment

1. Set up custom domain
2. Configure SSL certificates (usually automatic)
3. Set up monitoring (Sentry, etc.)
4. Configure CDN for static assets
5. Set up CI/CD pipeline
6. Add error tracking
7. Performance optimization
8. SEO optimization

Good luck with your deployment! 🚀

