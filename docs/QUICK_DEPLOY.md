# Quick Deploy - 5 Minutes

## Prerequisites
- GitHub account
- Render.com account (free): https://render.com
- Vercel account (free): https://vercel.com

---

## Step 1: Push to GitHub (2 minutes)

```bash
cd /Users/user/Documents/GitHub/pp/recipe-image/recipe-image-platform

# Initialize git (if not already)
git init
git add .
git commit -m "Recipe Image Platform - Ready for deployment"

# Create new GitHub repo at: https://github.com/new
# Name it: recipe-image-platform
# Then:

git remote add origin https://github.com/YOUR_USERNAME/recipe-image-platform.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy Backend to Render (3 minutes)

1. Go to: https://dashboard.render.com/select-repo
2. Click "Connect" next to your recipe-image-platform repo
3. Fill in:
   ```
   Name: recipe-api
   Environment: Python 3
   Root Directory: backend
   Build Command: pip install -r requirements.txt && python -m spacy download en_core_web_sm && python scripts/5_seed_database.py
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   Plan: Free
   ```
4. Add Environment Variables:
   - `DATABASE_URL` = `sqlite:///./recipe_platform.db`
   - `STATIC_DIR` = `static`
5. Click "Create Web Service"
6. **Copy your URL:** `https://recipe-api-XXXX.onrender.com`

---

## Step 3: Deploy Frontend to Vercel (3 minutes)

1. Go to: https://vercel.com/new
2. Import your GitHub repo
3. Configure:
   ```
   Framework: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   ```
4. Add Environment Variable:
   - `VITE_API_BASE_URL` = `https://recipe-api-XXXX.onrender.com/api/v1`
   (Use the URL from Step 2)
5. Click "Deploy"
6. **Your app URL:** `https://recipe-platform-XXXX.vercel.app`

---

## Step 4: Update CORS (1 minute)

1. Go back to Render: https://dashboard.render.com
2. Click on "recipe-api" → Environment
3. Update `CORS_ORIGINS`:
   ```
   https://recipe-platform-XXXX.vercel.app,http://localhost:5173
   ```
   (Use your Vercel URL from Step 3)
4. Click "Save" (auto-redeploys)

---

## Step 5: Test! 🎉

Visit your live app: `https://recipe-platform-XXXX.vercel.app`

You should see:
- ✅ Recipe list
- ✅ Images loading
- ✅ Can view recipe details
- ✅ Can create new recipes

**Share this URL with anyone!** 🚀

---

## Troubleshooting

### Backend taking long to respond?
- Render free tier spins down after 15 min of inactivity
- First request takes ~30s to wake up
- Subsequent requests are fast

### Images not loading?
- Check backend logs in Render dashboard
- Verify static files are included in deployment

### CORS errors?
- Double-check CORS_ORIGINS matches your Vercel URL exactly
- Include https:// in the URL

---

## Your Deployment URLs

Fill these in after deploying:

- **Backend API:** `___________________________________`
- **Frontend App:** `___________________________________`
- **API Docs:** `https://YOUR-BACKEND.onrender.com/docs`

---

## Next: Share Your App!

Once deployed, share your frontend URL with friends, colleagues, or add it to your portfolio!

Need help? See full guide: `DEPLOYMENT_GUIDE.md`
