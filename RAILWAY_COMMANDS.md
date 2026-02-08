# 🚂 Railway Deployment - Quick Commands

## First-Time Setup (5 minutes)

### 1. Install Railway CLI
```bash
npm install -g @railway/cli
```

### 2. Login
```bash
railway login
```

### 3. Initialize Project
```bash
# In your project directory:
cd E:\finalcheck\finalcheck
railway init
```

### 4. Add Environment Variables
```bash
# Paste these one by one:
railway variables set CLOUDINARY_CLOUD_NAME=your_cloud_name
railway variables set CLOUDINARY_API_KEY=your_key_here
railway variables set CLOUDINARY_API_SECRET=your_secret_here
railway variables set PINECONE_API_KEY=your_key_here
railway variables set PINECONE_INDEX_NAME=quantum-image-retrieval
```

### 5. Deploy
```bash
railway up
```

### 6. Get Your URL
```bash
railway domain
```

### 7. Update Frontend
```bash
# Edit frontend/.env with your Railway URL:
# VITE_API_URL=https://your-project.up.railway.app

git add frontend/.env
git commit -m "Update production API URL"
git push origin main
```

---

## Daily Use (Push to Deploy)

```bash
# Make changes
git add .
git commit -m "Your changes"
git push origin main

# Railway auto-deploys in 2-3 minutes
```

---

## Useful Commands

```bash
# View logs
railway logs --tail

# Check status
railway status

# Open dashboard
railway open

# Run command in Railway environment
railway run python --version

# Link different project
railway link

# Unlink project
railway unlink
```

---

## Environment Variables Reference

**Required:**
- `CLOUDINARY_CLOUD_NAME` - Your Cloudinary account name
- `CLOUDINARY_API_KEY` - Cloudinary API key
- `CLOUDINARY_API_SECRET` - Cloudinary API secret
- `PINECONE_API_KEY` - Pinecone API key
- `PINECONE_INDEX_NAME` - quantum-image-retrieval

**Optional (have defaults):**
- `FEATURE_EXTRACTOR_TYPE` - resnet (default)
- `FEATURE_DIMENSION` - 2048 (default)
- `QUANTUM_MODE` - simulation (default)
- `QUANTUM_SHOTS` - 1024 (default)

---

## Troubleshooting

**Build fails?**
```bash
railway logs | grep -i error
```

**Need to restart?**
```bash
railway restart
```

**Check environment variables:**
```bash
railway variables
```

**Delete and recreate:**
```bash
railway down
railway up
```

---

## Cost Estimate
- Free Tier: $5 credit/month
- Your app: ~$5/month (covered by free tier)
- Always-on: 730 hours/month
- First build: 10 minutes
- Updates: 2-3 minutes

---

## Quick Links
- Dashboard: https://railway.app/dashboard
- Docs: https://docs.railway.app
- Status: https://status.railway.app
