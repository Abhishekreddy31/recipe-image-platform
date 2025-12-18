# Deployment Guide - Recipe Image Platform

## Quick Deploy (Free Hosting)

This guide will help you deploy the Recipe Image Platform to free hosting services so you can share it with anyone.

**Total Time:** ~15 minutes
**Cost:** $0 (100% Free)

---

## Option 1: Deploy to Render.com (Recommended - Easiest)

### Prerequisites
1. GitHub account
2. Render.com account (sign up free at https://render.com)

### Step 1: Push Code to GitHub

```bash
# Initialize git if not already done
cd /Users/user/Documents/GitHub/pp/recipe-image/recipe-image-platform
git init
git add .
git commit -m "Initial commit - Recipe Image Platform"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/recipe-image-platform.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy Backend to Render

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** `recipe-platform-api`
   - **Environment:** `Python 3`
   - **Build Command:**
     ```bash
     pip install -r backend/requirements.txt && python -m spacy download en_core_web_sm && python backend/scripts/5_seed_database.py
     ```
   - **Start Command:**
     ```bash
     cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan:** Free
5. Add Environment Variables:
   - `DATABASE_URL` = `sqlite:///./recipe_platform.db`
   - `CORS_ORIGINS` = `https://YOUR-FRONTEND-URL.vercel.app` (we'll update this after frontend deploy)
6. Click "Create Web Service"
7. Wait ~5 minutes for deployment
8. **Copy your backend URL:** `https://recipe-platform-api.onrender.com`

### Step 3: Deploy Frontend to Vercel

1. Go to https://vercel.com
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
5. Add Environment Variable:
   - `VITE_API_BASE_URL` = `https://recipe-platform-api.onrender.com/api/v1`
6. Click "Deploy"
7. Wait ~2 minutes
8. **Your app is live!** Get the URL: `https://your-app.vercel.app`

### Step 4: Update CORS

Go back to Render dashboard → recipe-platform-api → Environment:
- Update `CORS_ORIGINS` to include your Vercel URL:
  ```
  https://your-app.vercel.app,http://localhost:5173
  ```
- Click "Save Changes" (this will redeploy)

### Step 5: Test Your Deployment!

Visit `https://your-app.vercel.app` and you should see:
- ✅ Recipe list loads
- ✅ Can view recipe details
- ✅ Cooking technique images display
- ✅ Can create new recipes

---

## Option 2: Deploy Both to Render (All-in-One)

### Deploy Backend (Same as above)

### Deploy Frontend to Render

1. In Render dashboard, click "New +" → "Static Site"
2. Connect your GitHub repo
3. Configure:
   - **Name:** `recipe-platform-frontend`
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`
4. Add Environment Variable:
   - `VITE_API_BASE_URL` = `https://recipe-platform-api.onrender.com/api/v1`
5. Click "Create Static Site"
6. Get URL: `https://recipe-platform-frontend.onrender.com`

---

## Option 3: Quick Deploy with Railway (Alternative)

### Deploy Backend to Railway

1. Sign up at https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects Python
5. Add environment variables:
   ```
   DATABASE_URL=sqlite:///./recipe_platform.db
   PORT=8000
   ```
6. Click "Deploy"
7. Get your backend URL

### Deploy Frontend to Vercel (same as Option 1)

---

## Important Notes

### Database

**Using SQLite (Current Setup):**
- ✅ Simple, works for MVP
- ✅ No additional setup needed
- ⚠️  Data persists but may reset on free tier restarts
- ⚠️  Limited to single server

**Upgrading to PostgreSQL (Optional):**

If you need persistent data:

1. Create free PostgreSQL database on Render:
   - New → PostgreSQL
   - Copy connection string
2. Update `DATABASE_URL` environment variable
3. Change database models to use proper UUID type (not String)
4. Run migrations

### Static Files (Images)

**Current Setup:**
- Images stored in `backend/static/images/techniques/`
- Served by FastAPI

**For Production:**
- Consider using S3-compatible storage (Cloudflare R2 free tier)
- Or keep images in git repo (current setup works fine for 50 images ~3MB)

### Free Tier Limitations

**Render.com Free:**
- Spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- 750 hours/month free

**Vercel Free:**
- Unlimited bandwidth
- No spin-down
- Perfect for frontend

---

## Troubleshooting

### Backend won't start
**Error:** "Module not found"
- Check build command includes all dependencies
- Verify spaCy model is downloaded

### CORS errors
- Ensure `CORS_ORIGINS` includes your frontend URL
- Check for typos in URLs (https vs http)

### Images not loading
- Verify static files are included in deployment
- Check image paths start with `/static/`
- Ensure backend mounts static directory

### Database empty
- Ensure seed script runs in build command
- Check logs for database initialization errors

---

## Environment Variables Summary

### Backend (Required)
```bash
DATABASE_URL=sqlite:///./recipe_platform.db
CORS_ORIGINS=https://your-frontend.vercel.app,http://localhost:5173
PORT=8000  # Usually auto-set by platform
```

### Frontend (Required)
```bash
VITE_API_BASE_URL=https://your-backend.onrender.com/api/v1
```

### Optional
```bash
PEXELS_API_KEY=your-key-here  # Only needed for re-downloading images
```

---

## Post-Deployment Checklist

- [ ] Backend health check: `https://your-backend.onrender.com/` returns JSON
- [ ] API docs accessible: `https://your-backend.onrender.com/docs`
- [ ] Frontend loads: `https://your-frontend.vercel.app`
- [ ] Recipes display correctly
- [ ] Images load properly
- [ ] Can create new recipes
- [ ] NLP extracts cooking actions
- [ ] Mobile responsive

---

## Sharing Your App

Once deployed, you can share:
```
https://recipe-platform.vercel.app
```

Anyone can:
- Browse recipes
- View cooking technique images
- Create new recipes (if you want to restrict this, add authentication)

---

## Monitoring

### Check Logs

**Render:**
- Dashboard → Your Service → Logs

**Vercel:**
- Dashboard → Your Project → Deployments → View Function Logs

---

## Updating the Deployment

### Auto-Deploy (Recommended)

Both Render and Vercel auto-deploy on git push:

```bash
# Make changes
git add .
git commit -m "Updated images"
git push

# Automatic redeployment triggered!
```

### Manual Deploy

**Render:** Dashboard → Service → Manual Deploy → Deploy latest commit
**Vercel:** Dashboard → Project → Deployments → Redeploy

---

## Cost Optimization

**Current Setup (Free):**
- Backend: Render free tier
- Frontend: Vercel free tier
- Database: SQLite (no cost)
- Images: Served from backend (no CDN cost)
- **Total: $0/month**

**If you need to scale:**
- Backend: Render starter ($7/month) - no spin-down
- Database: Render PostgreSQL ($7/month) - persistent data
- CDN: Cloudflare R2 (free tier includes 10GB)

---

## Security Checklist for Production

- [ ] Add rate limiting to API endpoints
- [ ] Implement authentication for recipe creation (optional)
- [ ] Add input validation and sanitization
- [ ] Enable HTTPS (automatic on Render/Vercel)
- [ ] Set secure CORS origins (no wildcards in production)
- [ ] Monitor for suspicious activity
- [ ] Regular backups of database

---

## Next Steps After Deployment

1. **Custom Domain (Optional):**
   - Buy domain from Namecheap, etc.
   - Add to Vercel/Render in dashboard
   - Update DNS records

2. **Analytics (Optional):**
   - Add Google Analytics
   - Or use Vercel Analytics (built-in)

3. **Feedback:**
   - Add feedback form
   - Monitor user behavior
   - Iterate based on usage

---

## Need Help?

If deployment fails:
1. Check build logs in platform dashboard
2. Verify all environment variables are set
3. Test locally first: `npm run build` and `uvicorn app.main:app`

---

**Ready to deploy? Start with Option 1 (Render + Vercel) - it's the easiest!** 🚀
