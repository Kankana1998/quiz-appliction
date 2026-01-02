# Free Production Deployment Guide

Complete step-by-step guide to deploy the Quiz Management System using **100% FREE** services.

## 🎯 Best Free Stack

- **Backend**: Render.com (Free Tier)
- **Database**: Render PostgreSQL (Free Tier)
- **Frontend**: Vercel (Free Tier)
- **Total Cost**: $0/month

---

## Prerequisites

- GitHub account (free)
- Email address
- 15-30 minutes

---

## Step 1: Prepare Your Code

### 1.1 Push to GitHub

```bash
# If not already on GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/quiz-app.git
git push -u origin main
```

### 1.2 Verify Files

Make sure you have:
- ✅ `backend/requirements.txt` (with gunicorn)
- ✅ `backend/Procfile` (for Heroku compatibility)
- ✅ `frontend/src/utils/api.js` (uses environment variable)

---

## Step 2: Deploy Backend (Render.com - FREE)

### 2.1 Create Render Account

1. Go to [render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with GitHub (easiest)
4. Authorize Render to access your repositories

### 2.2 Create PostgreSQL Database (FREE)

1. In Render Dashboard → Click **"New +"**
2. Select **"PostgreSQL"**
3. Configure:
   - **Name**: `quizdb-prod`
   - **Database**: `quizdb` (auto-filled)
   - **User**: `quizuser` (auto-filled)
   - **Region**: Choose closest to you (e.g., `Oregon (US West)`)
   - **PostgreSQL Version**: `18`
   - **Plan**: **Free** (512 MB RAM, shared CPU)
4. Click **"Create Database"**
5. ⚠️ **IMPORTANT**: Copy the **Internal Database URL** (starts with `postgresql://`)
   - It looks like: `postgresql://quizuser:password@dpg-xxxxx-a/quizdb`
   - Save this - you'll need it!

### 2.3 Create Web Service (FREE)

1. In Render Dashboard → Click **"New +"**
2. Select **"Web Service"**
3. Connect your GitHub account if not already connected
4. Select your repository: `quiz-app`
5. Configure the service:

   **Basic Settings:**
   - **Name**: `quiz-app-backend`
   - **Region**: Same as database (e.g., `Oregon (US West)`)
   - **Branch**: `main` (or your main branch)
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```bash
     gunicorn -w 4 -b 0.0.0.0:$PORT app:app
     ```
   - **Plan**: **Free** (512 MB RAM, 0.1 CPU)

6. Click **"Advanced"** → Add Environment Variables:

   ```
   DATABASE_URL=<paste-internal-database-url-from-step-2.2>
   SECRET_KEY=<generate-random-key>
   JWT_SECRET_KEY=<generate-different-random-key>
   JWT_ACCESS_TOKEN_EXPIRES=3600
   CORS_ORIGINS=https://your-frontend-url.vercel.app
   PORT=10000
   FLASK_ENV=production
   ```

   **Generate Secret Keys:**
   ```bash
   # Run this in terminal (run twice for two different keys)
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

7. Click **"Create Web Service"**
8. Wait 5-10 minutes for first deployment
9. **Save your backend URL**: `https://quiz-app-backend.onrender.com`

### 2.4 Run Database Migrations

1. Once backend is deployed, go to your service
2. Click **"Shell"** tab (or use "Logs" to find shell access)
3. Run these commands:

   ```bash
   flask db upgrade
   python seed.py
   python seed_quizzes.py
   ```

   Or use Render's Shell:
   - Go to your service → **"Shell"** button
   - Run commands one by one

---

## Step 3: Deploy Frontend (Vercel - FREE)

### 3.1 Create Vercel Account

1. Go to [vercel.com](https://vercel.com)
2. Click **"Sign Up"**
3. Sign up with GitHub
4. Authorize Vercel

### 3.2 Import Project

1. Vercel Dashboard → Click **"Add New..."** → **"Project"**
2. Import your GitHub repository: `quiz-app`
3. Configure Project:

   **Project Settings:**
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `dist` (auto-detected)
   - **Install Command**: `npm install` (auto-detected)

4. Click **"Environment Variables"**
5. Add:
   ```
   VITE_API_URL=https://quiz-app-backend.onrender.com/api
   ```
   (Use your actual backend URL from Step 2.3)

6. Click **"Deploy"**
7. Wait 2-3 minutes
8. **Save your frontend URL**: `https://quiz-app-xxxxx.vercel.app`

### 3.3 Update Backend CORS

1. Go back to Render → Your backend service
2. Go to **"Environment"** tab
3. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://quiz-app-xxxxx.vercel.app
   ```
   (Use your actual Vercel URL)
4. Click **"Save Changes"**
5. Render will auto-redeploy

---

## Step 4: Test Your Deployment

1. Visit your Vercel frontend URL
2. You should see the landing page with quizzes
3. Click **"Login as Admin"**
4. Login with:
   - Username: `admin`
   - Password: `admin123`
5. Test creating a quiz
6. Test taking a quiz

---

## Free Tier Limitations & Solutions

### Render Free Tier

**Limitations:**
- ⚠️ Service spins down after 15 minutes of inactivity
- ⚠️ First request after spin-down takes 30-60 seconds
- ⚠️ 750 hours/month free (enough for always-on small apps)
- ⚠️ 512 MB RAM limit

**Solutions:**
- Use a free uptime monitor (UptimeRobot) to ping your backend every 10 minutes
- Or accept the cold start delay
- Upgrade to paid ($7/month) for always-on

### Vercel Free Tier

**Limitations:**
- ✅ 100 GB bandwidth/month (plenty for small apps)
- ✅ Unlimited deployments
- ✅ Automatic HTTPS
- ✅ Custom domains supported
- ⚠️ Serverless functions have execution limits (not an issue for static sites)

**No issues for this app!** Vercel free tier is perfect for React/Vite apps.

### Render PostgreSQL Free Tier

**Limitations:**
- ⚠️ 90 days retention (database deleted after 90 days of inactivity)
- ⚠️ 1 GB storage limit
- ⚠️ Shared resources

**Solutions:**
- Keep your app active (deployments count as activity)
- 1 GB is plenty for thousands of quizzes
- Export data regularly if concerned

---

## Alternative Free Options

### Option 2: Railway.app (Limited Free Credits)

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Get $5 free credits/month
4. Deploy backend + database
5. Frontend on Vercel (still free)

**Note**: Railway free credits expire, but $5/month is usually enough for small apps.

### Option 3: Netlify (Frontend) + Render (Backend)

**Frontend on Netlify:**
1. Go to [netlify.com](https://netlify.com)
2. Sign up with GitHub
3. New site → Import from Git
4. Configure:
   - Base directory: `frontend`
   - Build: `npm run build`
   - Publish: `dist`
5. Add `VITE_API_URL` environment variable
6. Deploy

**Backend**: Same as Render steps above

---

## Environment Variables Summary

### Backend (Render)

```bash
DATABASE_URL=postgresql://user:pass@host:port/db
SECRET_KEY=<32-char-random-string>
JWT_SECRET_KEY=<32-char-random-string>
JWT_ACCESS_TOKEN_EXPIRES=3600
CORS_ORIGINS=https://your-frontend.vercel.app
PORT=10000
FLASK_ENV=production
```

### Frontend (Vercel)

```bash
VITE_API_URL=https://your-backend.onrender.com/api
```

---

## Keep Your App Free Forever

### 1. Prevent Render Spin-Down (Optional)

Use **UptimeRobot** (free):

1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Sign up (free)
3. Add Monitor:
   - Type: HTTP(s)
   - URL: `https://quiz-app-backend.onrender.com/api/health`
   - Interval: 5 minutes
4. This pings your backend every 5 minutes, keeping it awake

### 2. Monitor Usage

- **Render**: Dashboard shows hours used
- **Vercel**: Dashboard shows bandwidth
- Both have generous free tiers

### 3. Database Backups

Render auto-backs up, but you can export:

```bash
# In Render Shell
pg_dump $DATABASE_URL > backup.sql
```

---

## Quick Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] PostgreSQL database created on Render
- [ ] Backend web service created on Render
- [ ] Environment variables set in Render
- [ ] Database migrations run (`flask db upgrade`)
- [ ] Admin user created (`python seed.py`)
- [ ] Sample quizzes created (`python seed_quizzes.py`)
- [ ] Vercel account created
- [ ] Frontend deployed on Vercel
- [ ] `VITE_API_URL` set in Vercel
- [ ] Backend CORS updated with frontend URL
- [ ] Tested login
- [ ] Tested quiz creation
- [ ] Tested quiz taking

---

## Troubleshooting Free Tier Issues

### Backend Takes Long to Respond

**Problem**: First request after spin-down is slow (30-60 seconds)

**Solution**: 
- Use UptimeRobot to keep it awake (free)
- Or accept the delay
- Or upgrade to paid ($7/month)

### Database Connection Errors

**Problem**: Can't connect to database

**Solution**:
- Use **Internal Database URL** (not external)
- Check `DATABASE_URL` is correct
- Verify database is running in Render dashboard

### CORS Errors

**Problem**: Frontend can't call backend API

**Solution**:
- Check `CORS_ORIGINS` includes your Vercel URL
- No trailing slashes
- Use HTTPS URLs
- Redeploy backend after changing CORS

### Build Failures

**Problem**: Deployment fails

**Solution**:
- Check build logs in Render/Vercel
- Verify all dependencies in `requirements.txt`
- Check for syntax errors
- Ensure `Procfile` exists (for backend)

---

## Cost Breakdown (FREE)

| Service | Cost | What You Get |
|---------|------|--------------|
| **Render Backend** | $0 | 750 hours/month, 512 MB RAM |
| **Render PostgreSQL** | $0 | 1 GB storage, 90-day retention |
| **Vercel Frontend** | $0 | Unlimited deployments, 100 GB bandwidth |
| **GitHub** | $0 | Unlimited repos |
| **UptimeRobot** | $0 | 50 monitors, 5-min intervals |
| **Total** | **$0/month** | Fully functional production app |

---

## Next Steps

1. ✅ Deploy using steps above
2. ✅ Test everything works
3. ✅ Set up UptimeRobot (optional, keeps backend awake)
4. ✅ Add custom domain (optional, free on Vercel)
5. ✅ Monitor usage in dashboards
6. ✅ Enjoy your free production app! 🎉

---

## Important Notes

⚠️ **Render Free Tier**: Services spin down after inactivity. First request may be slow.

✅ **Vercel Free Tier**: Perfect for static sites, no limitations for this use case.

✅ **All Free**: This setup costs $0/month and is perfect for:
- Personal projects
- Portfolios
- Small businesses
- MVPs
- Learning projects

💡 **When to Upgrade**: 
- If you need always-on backend → Render paid ($7/month)
- If you exceed free limits → Check usage first, may still be free
- If you need more database storage → Render paid PostgreSQL ($7/month)

---

## Support Resources

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **UptimeRobot**: https://uptimerobot.com
- **Free Tier Limits**: Check each platform's pricing page

---

**You now have a fully functional, production-ready quiz app running on 100% free services!** 🚀

