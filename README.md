# Playto Pay KYC Pipeline

A small, working version of a KYC onboarding service for Indian agencies and freelancers to collect international payments.

## Stack
- **Backend**: Django, Django REST Framework, SQLite locally / PostgreSQL on Railway
- **Frontend**: React (Vite), Tailwind CSS, Axios, Lucide React
- **Authentication**: Token-based authentication

## Setup Instructions

### Backend
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Seed the database with test users:
   ```bash
   python seed.py
   ```
6. Start the backend server:
   ```bash
   python manage.py runserver
   ```

### Frontend
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the frontend development server:
   ```bash
   npm run dev
   ```

## Deployment

- Deploy the backend service to Railway from the repository root. Railway uses `railway.json`, the root `Dockerfile`, and `start.sh`.
- Deploy the frontend service to Vercel with `frontend` as the project root. Vercel uses `frontend/vercel.json`.
- Set `VITE_API_URL` in Vercel to your Railway backend URL, for example `https://your-backend-name.up.railway.app`.
- Set `CORS_ALLOWED_ORIGINS` in Railway to your Vercel frontend URL.

See `RAILWAY_DEPLOYMENT.md` for the full step-by-step flow.

## Test Data
The seed script creates the following users (Password for all is `password123`):
- **Reviewer**: `reviewer1`
- **Merchant (Draft)**: `merchant_draft`
- **Merchant (Under Review, At Risk)**: `merchant_review`
- **Merchant (Submitted)**: `merchant_submitted`

## Running Tests
To run the backend tests:
```bash
cd backend
python manage.py test kyc
```
