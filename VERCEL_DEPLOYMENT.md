# Hosting on Vercel

Complete guide for deploying the Enterprise Incentive Intelligence System on Vercel.

## 🚀 Deployment Options

### Option 1: Next.js Frontend + Vercel Python Functions (RECOMMENDED)

This is the easiest approach for Vercel hosting.

#### Prerequisites
- GitHub account with the repository
- Vercel account (free at vercel.com)

#### Steps

1. **Connect Repository to Vercel**
   ```bash
   # Push to GitHub first
   git push origin main
   ```

2. **Create Vercel Project**
   - Go to https://vercel.com/new
   - Import your GitHub repository
   - Framework Preset: Next.js
   - Root Directory: ./
   - Build Command: npm run build
   - Output Directory: .next

3. **Configure Environment Variables**
   Fastest path: run the CLI helper in the repo root after `vercel login` and `vercel link`:
   ```bash
   bash setup-vercel.sh
   ```

   If you only want to import the production environment variables with Vercel CLI, use:
   ```bash
   bash vercel-env-production.sh
   ```

   For preview or development environment sets, use:
   ```bash
   bash vercel-env-preview.sh
   bash vercel-env-development.sh
   ```

   This applies the full production set to Vercel, including API, database, auth, logging, caching, rate limiting, and feature flags.

   If you prefer the dashboard, set the same variables under Project Settings > Environment Variables.

4. **Deploy**
   - Click "Deploy"
   - Vercel automatically deploys on every git push

#### Features with This Approach
- ✅ Frontend hosted on Vercel (fast CDN)
- ✅ Python API functions on Vercel (serverless)
- ✅ Automatic deployments on git push
- ✅ Free tier available
- ✅ Custom domain support
- ✅ Built-in monitoring and analytics

---

### Option 2: Docker Container on Vercel

For more advanced control, use Docker.

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 3000
   CMD ["python", "main.py"]
   ```

2. **Deploy**
   ```bash
   vercel deploy --prod
   ```

---

### Option 3: Separate Deployments

Deploy frontend and backend separately:

- **Frontend**: Vercel (Next.js)
- **Backend**: Render, Railway, or Heroku (Python API)

Update `NEXT_PUBLIC_API_URL` to point to backend service.

---

## 📦 Production Checklist

- [ ] Environment variables configured
- [ ] DATABASE_URL points to production database
- [ ] NEXT_PUBLIC_API_URL set correctly
- [ ] Error logging configured
- [ ] CORS settings verified
- [ ] Rate limiting enabled
- [ ] Analytics enabled

---

## 🔧 Local Testing Before Deployment

```bash
# Install dependencies
npm install

# Run locally
npm run dev

# Build for production
npm run build

# Test production build
npm run start
```

---

## 📊 Monitoring on Vercel

1. **Analytics Dashboard**
   - Vercel > Project > Analytics
   - Monitor requests, errors, performance

2. **Logs**
   - Vercel > Project > Logs
   - View function logs and errors

3. **Deployments**
   - Vercel > Project > Deployments
   - Rollback to previous versions

---

## 🔗 Custom Domain

1. Go to Vercel Dashboard > Project > Settings > Domains
2. Add your custom domain
3. Update DNS records (provided by Vercel)
4. Enable SSL (automatic)

---

## 💰 Cost Estimate

Vercel Free Tier Includes:
- 100 GB bandwidth/month
- Unlimited deployments
- 12 serverless function hours/month
- Edge Network

For higher usage, see Vercel pricing at vercel.com/pricing

---

## 🐛 Troubleshooting

**Issue: Python packages not found**
```
Solution: Ensure requirements.txt is in root directory
```

**Issue: API returns 500 error**
```
Check Vercel logs: vercel logs --tail
```

**Issue: CORS errors in browser**
```
Verify CORS headers in api/index.py
Add your Vercel domain to allowed origins
```

**Issue: Database not persisting**
```
Use environment-based database path
Connect to external PostgreSQL or MongoDB
```

---

## 🚀 Deployment Commands

```bash
# Apply production environment variables and build locally
bash setup-vercel.sh

# Import only the production environment variables
bash vercel-env-production.sh

# Import preview or development environment variables
bash vercel-env-preview.sh
bash vercel-env-development.sh

# Deploy to Vercel (production)
vercel deploy --prod

# Deploy preview
vercel deploy

# View logs
vercel logs --tail

# View project settings
vercel env list

# Pull environment variables
vercel env pull
```

---

## 📚 Resources

- Vercel Docs: https://vercel.com/docs
- Next.js Docs: https://nextjs.org/docs
- Python Support: https://vercel.com/docs/serverless-functions/python

---

**Last Updated:** May 5, 2026
**Status:** Ready for Production
