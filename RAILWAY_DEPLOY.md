# 🚀 Railway.app Deployment Guide
## Quantum Image Retrieval System - Docker Deployment

---

## 📋 Prerequisites

Before deploying to Railway, ensure you have:

1. ✅ **GitHub Account** - Your code pushed to a GitHub repository
2. ✅ **Railway Account** - Sign up at [railway.app](https://railway.app) (free)
3. ✅ **API Keys Ready**:
   - Cloudinary API credentials (cloud_name, api_key, api_secret)
   - Pinecone API key + index name

---

## 🎯 Quick Start (5 Minutes)

### Option 1: Deploy via Railway Dashboard (Recommended)

#### Step 1: Create Railway Project
```bash
# 1. Go to https://railway.app
# 2. Click "New Project"
# 3. Select "Deploy from GitHub repo"
# 4. Authorize Railway to access your GitHub
# 5. Select your repository: finalcheck
```

#### Step 2: Configure Environment Variables
```bash
# In Railway Dashboard:
# Project → Variables → Add Variables

# Copy these from your local .env file:
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=<your_key>
CLOUDINARY_API_SECRET=<your_secret>
PINECONE_API_KEY=<your_key>
PINECONE_INDEX_NAME=quantum-image-retrieval

# Optional (already have defaults):
FEATURE_EXTRACTOR_TYPE=resnet
FEATURE_DIMENSION=2048
QUANTUM_MODE=simulation
```

#### Step 3: Deploy
```bash
# Railway auto-detects Dockerfile and builds
# Wait 5-10 minutes for first build (PyTorch is large)
# Click "Generate Domain" to get public URL
```

#### Step 4: Update Frontend API URL
```bash
# After deployment, Railway provides a domain like:
# https://your-project-production.up.railway.app

# Update frontend/.env:
VITE_API_URL=https://your-project-production.up.railway.app

# Commit and push to trigger rebuild:
git add frontend/.env
git commit -m "Update API URL for Railway"
git push origin main
```

---

### Option 2: Deploy via Railway CLI

#### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
```

#### Step 2: Login and Initialize
```bash
# Login to Railway
railway login

# Link to existing project or create new
railway init
```

#### Step 3: Set Environment Variables
```bash
# Add all required variables
railway variables set CLOUDINARY_CLOUD_NAME=your_cloud_name
railway variables set CLOUDINARY_API_KEY=<your_key>
railway variables set CLOUDINARY_API_SECRET=<your_secret>
railway variables set PINECONE_API_KEY=<your_key>
railway variables set PINECONE_INDEX_NAME=quantum-image-retrieval
```

#### Step 4: Deploy
```bash
# Deploy current directory
railway up

# Get your deployment URL
railway domain
```

#### Step 5: Update Frontend URL
```bash
# Edit frontend/.env with your Railway domain
# Then commit and push:
git add frontend/.env
git commit -m "Update API URL"
git push origin main
```

---

## 🔧 Production Configuration

### Backend Configuration (backend/config.py)
Your backend is already configured via environment variables. No changes needed.

### Frontend Configuration (frontend/.env)
```properties
# LOCAL DEVELOPMENT:
VITE_API_URL=http://localhost:8000

# PRODUCTION (after Railway deployment):
VITE_API_URL=https://your-project.up.railway.app
VITE_API_TIMEOUT=30000
```

### Database Status
✅ **Already Configured**: 3,624 images uploaded to Pinecone
- Healthcare: 624 images
- Satellite: 1,500 images
- Surveillance: 1,500 images

**No data migration needed** - Pinecone is cloud-hosted, Railway connects directly.

---

## 🐳 Docker Configuration

### Current Setup (Already Ready)
- **Dockerfile**: Multi-stage build (Node 18 → Python 3.13)
- **Size**: ~3GB (includes PyTorch 2.6.0)
- **Services**: Backend (port 8000) + Frontend (port 5000)
- **Health Check**: `/health` endpoint every 30s

### Railway-Specific Settings (railway.json)
```json
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "numReplicas": 1,
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100
  }
}
```

---

## 📊 Expected Build Process

```
Railway Build Log:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[1/4] Stage 1: Building frontend...
  ✅ npm install (30s)
  ✅ npm run build (45s)
  ✅ Frontend built → /dist

[2/4] Stage 2: Installing Python...
  ✅ Python 3.13-slim base image
  ✅ Installing system dependencies (20s)
  ✅ pip install requirements.txt (3-4 minutes)
     → PyTorch 2.6.0 (~2GB)
     → Qiskit, Transformers, Pinecone, etc.

[3/4] Copying application files...
  ✅ Copying backend code
  ✅ Copying frontend dist from Stage 1

[4/4] Final setup...
  ✅ Creating directories
  ✅ Exposing ports 8000, 5000
  ✅ Starting health check

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Build Time: 5-10 minutes
Final Image Size: ~3GB
```

---

## ✅ Post-Deployment Verification

### Test Your Deployment

#### 1. Health Check
```bash
curl https://your-project.up.railway.app/health
# Expected: {"status":"healthy","timestamp":"..."}
```

#### 2. API Health
```bash
curl https://your-project.up.railway.app/api/health
# Expected: {"status":"healthy","feature_extractor":"ResNet-50",...}
```

#### 3. Categories Endpoint
```bash
curl https://your-project.up.railway.app/api/categories
# Expected: {"success":true,"categories":["healthcare","satellite","surveillance"]}
```

#### 4. Frontend Access
```bash
# Open in browser:
https://your-project.up.railway.app:5000
# OR (if Railway proxies port 5000 to 80):
https://your-project.up.railway.app
```

#### 5. Upload Test (via Frontend)
- Open frontend URL
- Click "Upload Image"
- Select a test image
- Verify search results appear

---

## 💰 Cost & Limits

### Railway Free Tier (Hobby Plan)
- ✅ **$5 FREE credits per month**
- ✅ **500 hours execution time/month**
- ✅ **100GB outbound bandwidth/month**
- ✅ **Custom domains with HTTPS**
- ✅ **1GB memory limit per service**

### Expected Usage (Your Project)
| Resource | Usage | Monthly Cost |
|----------|-------|--------------|
| Build Time | 10 min/deploy × 10 deploys | $0.50 |
| Runtime | 730 hrs (always on) | $4.50 |
| Bandwidth | ~10GB (image CDN via Cloudinary) | $0.00 |
| **TOTAL** | | **~$5/month (FREE tier covers it)** |

### Optimization Tips
- Images served via Cloudinary CDN (not Railway bandwidth)
- Feature vectors cached in Pinecone (minimal memory usage)
- Frontend is static files (low CPU usage)
- Backend only runs inference on-demand

---

## 🔥 Troubleshooting

### Build Fails: "Out of Memory"
```bash
# Railway default: 1GB RAM during build
# PyTorch might need more. Solutions:

# Option 1: Upgrade to Pro plan ($20/month, 8GB RAM)
# Option 2: Use lighter dependencies (already optimized)
# Option 3: Pre-build Docker image, push to Docker Hub, deploy from there
```

### Health Check Fails
```bash
# Check logs in Railway Dashboard:
railway logs

# Common issues:
# 1. Missing environment variables → Add in Variables tab
# 2. Port mismatch → Railway auto-sets PORT env var
# 3. Startup timeout → Backend needs 30-60s for PyTorch init
```

### Frontend Can't Connect to Backend
```bash
# Issue: CORS error or 404

# Fix 1: Update frontend/.env with Railway domain
VITE_API_URL=https://your-project.up.railway.app

# Fix 2: Check backend CORS settings (backend/config.py)
# Should allow Railway domain

# Fix 3: Use same domain for frontend + backend
# Railway proxies both ports via single domain
```

### "Module Not Found" Error
```bash
# Check requirements.txt has all dependencies:
railway logs | grep "ModuleNotFoundError"

# If missing, add to requirements.txt and redeploy
```

---

## 🚀 Deployment Workflow (After Initial Setup)

### Daily Development Cycle
```bash
# 1. Make code changes locally
git add .
git commit -m "Add new feature"

# 2. Push to GitHub
git push origin main

# 3. Railway auto-deploys (2-3 minutes for updates)
# No manual intervention needed!

# 4. Check deployment status
railway status

# 5. View logs
railway logs --tail
```

### Rollback to Previous Version
```bash
# In Railway Dashboard:
# Deployments → Select previous successful deployment → Redeploy
```

---

## 📈 Monitoring & Logs

### Real-Time Logs
```bash
# Via CLI:
railway logs --tail

# Via Dashboard:
# Project → Deployments → View Logs
```

### Key Metrics to Watch
- **Response Time**: Should be <2s for search (quantum algorithm)
- **Memory Usage**: Should stay <800MB
- **Error Rate**: Should be <1%
- **Uptime**: Should be 99.9%+

### Logging in Your App
Already configured in `backend_server.py`:
```python
logger.info(f"✅ Feature extraction: {extraction_time:.2f}s")
logger.info(f"🔮 Quantum processing: {quantum_time:.2f}s")
```

View these in Railway logs to monitor performance.

---

## 🎓 For College Project Demo

### Quick Demo Script

**Setup (30 seconds):**
1. Open Railway deployment URL: `https://your-project.up.railway.app`
2. Show "System Status" - 3,624 images loaded

**Demo Flow (2 minutes):**
1. **Upload**: Select medical scan → Click upload
2. **Processing**: Show "Extracting features..." (ResNet-50)
3. **Quantum Search**: Show "Quantum enhancement..." (11 qubits)
4. **Results**: Display top 5 similar images
5. **Filter**: Show healthcare/satellite/surveillance categories
6. **Performance**: Point out "<2s response time"

**Technical Highlights:**
- ✅ ResNet-50 feature extraction (2048-D vectors)
- ✅ TRUE Quantum algorithm (Qiskit, 11 qubits)
- ✅ 3,624 real images across 3 domains
- ✅ Cloud production deployment (Railway)
- ✅ CDN-hosted images (Cloudinary)
- ✅ Vector database (Pinecone)

---

## 📚 Additional Resources

- **Railway Docs**: https://docs.railway.app
- **Railway CLI**: https://docs.railway.app/develop/cli
- **Docker Best Practices**: https://docs.docker.com/develop/dev-best-practices/
- **Your Project GitHub**: [Add your repo URL here]
- **Live Demo**: [Add Railway URL after deployment]

---

## ✨ What's Already Done

✅ **Dockerfile configured** (multi-stage, optimized)  
✅ **Backend ready** (0 errors, all APIs working)  
✅ **Frontend ready** (React + TypeScript built)  
✅ **Database populated** (3,624 vectors in Pinecone)  
✅ **Quantum algorithm active** (TRUE MODE)  
✅ **railway.json created** (auto-deploy config)  
✅ **.env.railway template** (environment variables guide)

---

## 🎯 Next Steps

1. **Push to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Ready for Railway deployment"
   git push origin main
   ```

2. **Create Railway Project**:
   - Go to railway.app
   - Connect GitHub repo
   - Add environment variables from `.env.railway`

3. **Wait for Build** (5-10 minutes first time)

4. **Get Public URL** (Railway generates automatically)

5. **Update Frontend** (set VITE_API_URL to Railway domain)

6. **Test & Demo** 🎉

---

**Questions? Check Railway logs or ping me!**
