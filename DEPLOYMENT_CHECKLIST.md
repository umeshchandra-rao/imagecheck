# ✅ Railway Deployment Checklist

## Pre-Deployment (Do Once)

### Local Setup
- [x] Codebase cleaned (1,222 lines dead code removed)
- [x] All critical bugs fixed (7 issues resolved)
- [x] Backend tested (0 compilation errors)
- [x] Frontend tested (0 compilation errors)
- [x] Database populated (3,624 vectors in Pinecone)
- [x] Docker configured (Dockerfile + docker-compose.yml)
- [x] Railway config created (railway.json)
- [x] Environment template created (.env.railway)
- [x] Deployment guides created (RAILWAY_DEPLOY.md)

### GitHub Setup
- [ ] Create GitHub repository (if not exist)
  ```bash
  # In your project folder:
  git init
  git add .
  git commit -m "Initial commit - ready for Railway"
  git branch -M main
  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
  git push -u origin main
  ```

- [ ] Verify files pushed:
  - Dockerfile ✓
  - railway.json ✓
  - requirements.txt ✓
  - backend/ folder ✓
  - frontend/ folder ✓
  - ml/ folder ✓
  - services/ folder ✓

### API Keys Ready
- [ ] Cloudinary credentials:
  - CLOUDINARY_CLOUD_NAME: `your_cloud_name`
  - CLOUDINARY_API_KEY: `_____________`
  - CLOUDINARY_API_SECRET: `_____________`

- [ ] Pinecone credentials:
  - PINECONE_API_KEY: `_____________`
  - PINECONE_INDEX_NAME: `quantum-image-retrieval` ✓

---

## Deployment (15 Minutes)

### Option A: Railway Dashboard (Easiest)

1. **Create Railway Account**
   - [ ] Go to https://railway.app
   - [ ] Click "Login with GitHub"
   - [ ] Authorize Railway

2. **Create New Project**
   - [ ] Click "New Project"
   - [ ] Select "Deploy from GitHub repo"
   - [ ] Choose your repository
   - [ ] Wait for Railway to detect Dockerfile

3. **Configure Environment Variables**
   - [ ] Click on your service
   - [ ] Go to "Variables" tab
   - [ ] Click "Add Variables"
   - [ ] Paste from .env.railway file:
     ```
     CLOUDINARY_CLOUD_NAME=your_cloud_name
     CLOUDINARY_API_KEY=your_actual_key
     CLOUDINARY_API_SECRET=your_actual_secret
     PINECONE_API_KEY=your_actual_key
     PINECONE_INDEX_NAME=quantum-image-retrieval
     ```

4. **Generate Public Domain**
   - [ ] Click "Settings" tab
   - [ ] Scroll to "Domains"
   - [ ] Click "Generate Domain"
   - [ ] Copy your URL: `https://_______.up.railway.app`

5. **Wait for First Build**
   - [ ] Watch "Deployments" tab
   - [ ] Build takes 8-12 minutes (PyTorch is large)
   - [ ] Look for "Success" status

6. **Update Frontend API URL**
   - [ ] Edit `frontend/.env`:
     ```properties
     VITE_API_URL=https://your-project.up.railway.app
     ```
   - [ ] Commit and push:
     ```bash
     git add frontend/.env
     git commit -m "Update API URL for Railway"
     git push origin main
     ```

7. **Wait for Rebuild**
   - [ ] Railway auto-detects push
   - [ ] Rebuild takes 2-3 minutes
   - [ ] Check "Success" status

### Option B: Railway CLI (Faster)

1. **Install CLI**
   ```bash
   npm install -g @railway/cli
   ```
   - [ ] CLI installed successfully

2. **Login**
   ```bash
   railway login
   ```
   - [ ] Browser opens, authorize Railway
   - [ ] Terminal shows "Logged in as YOUR_EMAIL"

3. **Initialize Project**
   ```bash
   railway init
   ```
   - [ ] Choose "Create new project"
   - [ ] Enter project name: `quantum-image-retrieval`

4. **Set Environment Variables**
   ```bash
   railway variables set CLOUDINARY_CLOUD_NAME=your_cloud_name
   railway variables set CLOUDINARY_API_KEY=your_key
   railway variables set CLOUDINARY_API_SECRET=your_secret
   railway variables set PINECONE_API_KEY=your_key
   railway variables set PINECONE_INDEX_NAME=quantum-image-retrieval
   ```
   - [ ] All 5 variables set

5. **Deploy**
   ```bash
   railway up
   ```
   - [ ] Build starts (8-12 minutes first time)
   - [ ] Watch progress in terminal
   - [ ] Look for "Deployment successful"

6. **Get Public URL**
   ```bash
   railway domain
   ```
   - [ ] Copy URL: `https://_______.up.railway.app`

7. **Update Frontend & Redeploy**
   ```bash
   # Edit frontend/.env with Railway URL
   git add frontend/.env
   git commit -m "Update API URL"
   git push origin main
   ```
   - [ ] Changes pushed
   - [ ] Railway auto-deploys (2-3 minutes)

---

## Verification (5 Minutes)

### Test Endpoints

1. **Health Check**
   ```bash
   curl https://your-project.up.railway.app/health
   ```
   - [ ] Returns: `{"status":"healthy",...}`

2. **API Health**
   ```bash
   curl https://your-project.up.railway.app/api/health
   ```
   - [ ] Returns: `{"status":"healthy","feature_extractor":"ResNet-50",...}`

3. **Categories**
   ```bash
   curl https://your-project.up.railway.app/api/categories
   ```
   - [ ] Returns: `{"success":true,"categories":["healthcare","satellite","surveillance"]}`

4. **Frontend Access**
   - [ ] Open: `https://your-project.up.railway.app:5000` (or port 80 if proxied)
   - [ ] UI loads correctly
   - [ ] System status shows "3,624 images loaded"

5. **Upload Test**
   - [ ] Click "Upload Image"
   - [ ] Select test image
   - [ ] Click "Search Similar"
   - [ ] Results appear in <2 seconds
   - [ ] Quantum processing indicator shows

6. **Search Test**
   - [ ] Filter by "healthcare"
   - [ ] Results update
   - [ ] Filter by "satellite"
   - [ ] Results update

---

## Post-Deployment

### Monitor

- [ ] Check Railway Dashboard → Logs
  ```
  ✅ ResNet-50 feature extractor initialized
  ✅ Pinecone connected (3624 vectors)
  ✅ Quantum algorithm initialized (TRUE MODE)
  ```

- [ ] Check memory usage (should be <1GB)
- [ ] Check response times (should be <2s)

### Document

- [ ] Add Railway URL to README.md
- [ ] Add deployment date
- [ ] Add any custom configurations
- [ ] Update project documentation with live demo link

### Share

- [ ] Test from different network (not localhost)
- [ ] Test on mobile device
- [ ] Share with team/professor
- [ ] Prepare demo script (see RAILWAY_DEPLOY.md)

---

## Troubleshooting

### Build Fails
- [ ] Check Railway logs: Click "View Logs"
- [ ] Common issues:
  - Missing environment variable → Add in Variables tab
  - Out of memory → Upgrade to Pro plan or optimize
  - Dockerfile syntax → Check Dockerfile line mentioned in error

### Health Check Fails
- [ ] Verify backend started: `railway logs | grep "Uvicorn running"`
- [ ] Check port: Railway auto-sets PORT env var (usually 8000)
- [ ] Wait 60 seconds: PyTorch initialization takes time

### Frontend Can't Connect
- [ ] Verify VITE_API_URL in frontend/.env matches Railway domain
- [ ] Check CORS: Backend should allow Railway domain
- [ ] Try both port 5000 and default port (Railway may proxy)

### Quantum Algorithm Fails
- [ ] Check logs: `railway logs | grep "Quantum"`
- [ ] Verify: Should see "TRUE MODE" not "Disabled"
- [ ] If disabled: Qiskit might not install - check requirements.txt

---

## Success Criteria ✅

Your deployment is successful when:

- ✅ Railway domain accessible (HTTPS)
- ✅ Health check returns `{"status":"healthy"}`
- ✅ Frontend loads and shows UI
- ✅ Upload works and returns results
- ✅ Search returns similar images
- ✅ Quantum processing indicator shows
- ✅ Response time <2 seconds
- ✅ No errors in Railway logs
- ✅ Can access from any network
- ✅ Free tier covers costs ($5/month)

---

## Next Steps

1. **Test thoroughly** - Try all features
2. **Monitor costs** - Check Railway usage dashboard
3. **Optimize if needed** - Review slow endpoints
4. **Add custom domain** (optional) - Settings → Domains → Add
5. **Set up monitoring** (optional) - Add Sentry or similar
6. **Prepare demo** - Use script in RAILWAY_DEPLOY.md

---

## Quick Reference

**Railway Dashboard**: https://railway.app/dashboard
**Your Project URL**: `https://_______.up.railway.app`
**Deployment Date**: __________
**Build Time**: 8-12 minutes (first), 2-3 minutes (updates)
**Monthly Cost**: ~$5 (covered by free tier)

---

**Status**: ⏳ Ready to Deploy | 🚀 Deploy Now!
