# Railway Backend + Vercel Frontend Deployment Guide

This guide deploys only the Django backend on Railway and the Vite React frontend on Vercel.

## Prerequisites

- Railway account (https://railway.app)
- Vercel account (https://vercel.com)
- GitHub repository with this code
- Git installed locally

## 1. Deploy Backend On Railway

### Prepare Your Repository

Ensure you have committed all changes:

```bash
git add .
git commit -m "Split Railway backend and Vercel frontend deployment"
git push -u origin main
```

### Create a Railway Project

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Authorize Railway to access your GitHub account
5. Select your repository
6. Click "Deploy"

Railway uses `railway.json` and the root `Dockerfile`. The Docker image installs only the Django backend.

### Add PostgreSQL Database

1. In Railway project dashboard, click "Add Service"
2. Select "PostgreSQL"
3. Railway will automatically set `DATABASE_URL` for the backend service

### Configure Railway Environment Variables

In the backend service, open **Settings -> Variables** and add:

Replace the domains with your actual Railway and Vercel domains.

```
DEBUG=False
SECRET_KEY=generate-a-random-secret-key
ALLOWED_HOSTS=your-backend-name.up.railway.app,.railway.app
CORS_ALLOWED_ORIGINS=https://your-frontend-name.vercel.app
CSRF_TRUSTED_ORIGINS=https://your-backend-name.up.railway.app,https://your-frontend-name.vercel.app
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

**To generate a SECRET_KEY:**
```python
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### Backend URL

After deployment, the API is available at:

```
https://your-backend-name.up.railway.app/api/v1/
```

## 2. Deploy Frontend On Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New..." -> "Project"
3. Import the same GitHub repository
4. Set **Root Directory** to `frontend`
5. Vercel will use `frontend/vercel.json`
6. Add this environment variable:

```
VITE_API_URL=https://your-backend-name.up.railway.app
```

7. Deploy

The frontend will call the backend at `${VITE_API_URL}/api/v1/`.

## 3. Update CORS After Vercel Deploys

Once Vercel gives you the final frontend URL, go back to Railway and make sure:

```
CORS_ALLOWED_ORIGINS=https://your-frontend-name.vercel.app
CSRF_TRUSTED_ORIGINS=https://your-backend-name.up.railway.app,https://your-frontend-name.vercel.app
```

Redeploy the Railway backend after changing variables.

## Monitor Deployment

1. Go to Railway project dashboard
2. Click on the service to view logs
3. Wait for build to complete (usually 5-10 minutes)

## Troubleshooting

### Check Logs
- Go to Railway dashboard → Your project → View logs
- Look for any error messages during build or deployment

### Common Issues

**Build Fails:**
- Check that all dependencies in `requirements.txt` and `package.json` are correct
- Ensure the `build.sh` script has proper permissions

**Database Connection Error:**
- Verify `DATABASE_URL` is set automatically by Railway
- Check if PostgreSQL service is running

**Static Files Not Loading:**
- Ensure `python manage.py collectstatic` runs successfully
- Check that frontend build completes without errors

**Frontend Cannot Reach API:**
- Verify Vercel has `VITE_API_URL=https://your-backend-name.up.railway.app`
- Verify Railway has `CORS_ALLOWED_ORIGINS=https://your-frontend-name.vercel.app`
- Redeploy Vercel after changing `VITE_API_URL`

### Manual Database Setup

If needed, you can run management commands:

```bash
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | False | Set to True only for development |
| `SECRET_KEY` | Required | Django secret key (generate random) |
| `ALLOWED_HOSTS` | localhost | Comma-separated allowed domains |
| `DATABASE_URL` | Auto | PostgreSQL connection string (auto-set by Railway) |
| `CORS_ALLOWED_ORIGINS` | localhost dev URLs | Vercel frontend origins allowed to call the API |
| `SECURE_SSL_REDIRECT` | False | Force HTTPS redirect |
| `SESSION_COOKIE_SECURE` | False | Only send cookies over HTTPS |
| `CSRF_COOKIE_SECURE` | False | CSRF token only over HTTPS |
| `VITE_API_URL` | localhost backend | Vercel frontend API base URL |

## File Structure

- `Dockerfile` - Builds only the Django backend for Railway
- `railway.json` - Railway backend configuration
- `start.sh` - Runs migrations and starts Gunicorn on Railway's `$PORT`
- `frontend/vercel.json` - Vercel build and SPA routing configuration
- `.env.example` - Environment variables template

## Local Development

To test locally before deploying:

```bash
# Backend
cd backend
python -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

Access at `http://localhost:3000`

## Database Backups

Railway PostgreSQL databases include automatic backups. To download:

1. Go to Railway project → PostgreSQL service
2. Click "Data" tab
3. Use Railway CLI or database tools to export

## Scaling and Performance

- Railway auto-scales based on traffic
- For high-traffic scenarios, increase dyno tier in settings
- Consider Redis for caching if needed

## Support

- Railway Docs: https://docs.railway.app
- Django Deployment: https://docs.djangoproject.com/en/6.0/howto/deployment/
- Report issues: Create a GitHub issue in your repository

