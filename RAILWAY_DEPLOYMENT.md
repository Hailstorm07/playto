# Railway Deployment Guide

This guide explains how to deploy the KYC Management application on Railway.

## Prerequisites

- Railway account (https://railway.app)
- GitHub repository with this code
- Git installed locally

## Deployment Steps

### 1. Prepare Your Repository

Ensure you have committed all changes:

```bash
git add .
git commit -m "Add Railway deployment configuration"
git push -u origin main
```

### 2. Create a Railway Project

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Authorize Railway to access your GitHub account
5. Select your repository
6. Click "Deploy"

### 3. Configure Environment Variables

Once deployed, Railway will automatically:
- Create a PostgreSQL database
- Set `DATABASE_URL` environment variable

You need to add additional variables in the Railway dashboard:

**Settings → Variables**

Add these environment variables:

```
DEBUG=False
SECRET_KEY=generate-a-random-secret-key
ALLOWED_HOSTS=your-app-name.railway.app,*.railway.app
CORS_ALLOWED_ORIGINS=https://your-app-name.railway.app
CSRF_TRUSTED_ORIGINS=https://your-app-name.railway.app
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
VITE_API_URL=https://your-app-name.railway.app
```

**To generate a SECRET_KEY:**
```python
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 4. Add PostgreSQL Database

1. In Railway project dashboard, click "Add Service"
2. Select "PostgreSQL"
3. Railway will automatically set `DATABASE_URL` environment variable

### 5. Build Configuration

Railway automatically detects:
- Backend uses Python (from requirements.txt)
- Frontend uses Node.js (from package.json)

The `build.sh` script handles:
- Installing Python dependencies
- Building the frontend
- Running Django migrations
- Collecting static files

### 6. Monitor Deployment

1. Go to Railway project dashboard
2. Click on the service to view logs
3. Wait for build to complete (usually 5-10 minutes)

### 7. Access Your Application

Once deployed, your app will be available at:
```
https://your-app-name.railway.app
```

The backend API will be at:
```
https://your-app-name.railway.app/api/v1/
```

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

**Frontend Not Loading:**
- Verify `VITE_API_URL` environment variable is set correctly
- Check browser console for CORS errors

### Manual Database Setup

If needed, you can run management commands:

```bash
railway run python backend/manage.py migrate
railway run python backend/manage.py createsuperuser
railway run python backend/manage.py seed
```

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | False | Set to True only for development |
| `SECRET_KEY` | Required | Django secret key (generate random) |
| `ALLOWED_HOSTS` | localhost | Comma-separated allowed domains |
| `DATABASE_URL` | Auto | PostgreSQL connection string (auto-set by Railway) |
| `CORS_ALLOWED_ORIGINS` | localhost:3000 | Allowed CORS origins |
| `VITE_API_URL` | . | Frontend API URL |
| `SECURE_SSL_REDIRECT` | False | Force HTTPS redirect |
| `SESSION_COOKIE_SECURE` | False | Only send cookies over HTTPS |
| `CSRF_COOKIE_SECURE` | False | CSRF token only over HTTPS |

## File Structure

- `Procfile` - Defines how Railway runs the app
- `railway.json` / `railway.toml` - Railway configuration
- `build.sh` - Build script (runs on deployment)
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

