# Quick Start Guide

## Fast Setup (5 minutes)

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Seed Database with Questions

```bash
cd backend
python seed_questions.py
```

This creates 12 Python coding questions across 3 difficulty levels.

### 3. Start the Server

From the project root:

```bash
python run_server.py
```

Or from backend directory:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access the Application

Open your browser and go to:
- **http://localhost:8000/** - Landing page
- **http://localhost:8000/admin** - Admin panel

## First Time Setup

### Step 1: Create an Event (Admin)

1. Go to `/admin`
2. Enter an event name (e.g., "Spring Coding Competition 2024")
3. Click "Create Event"

### Step 2: Upload College Logo (Admin)

1. In the admin panel, click "Choose File" under "Upload College Logo"
2. Select a PNG or JPG image
3. Click "Upload Logo"

### Step 3: Start the Contest (Admin)

1. Wait for players to join (they'll appear in the lobby)
2. Click "Start Contest" when ready
3. All players will be automatically redirected to the contest page

## Testing the Platform

### As a Player:

1. Go to the landing page (`/`)
2. Enter your name and select college year
3. Click "Join Competition"
4. Wait in the lobby
5. When admin starts the contest, you'll be redirected
6. Solve Python coding questions
7. Check your progress on the leaderboard

### As an Admin:

1. Create event and upload logo
2. Monitor players joining in the lobby
3. Start the contest
4. Monitor progress via leaderboard
5. Stop contest when finished
6. Export results as CSV
7. View Hall of Fame

## Troubleshooting

### Database not found
- The database is created automatically on first run
- Delete `competition.db` to reset everything

### Questions not showing
- Run `python backend/seed_questions.py` to seed questions

### Static files not loading
- Ensure you're running from the project root
- Check that `frontend/` and `static/` directories exist

### Port already in use
- Change port in `run_server.py` or use: `uvicorn app.main:app --port 8001`

## Next Steps

- Customize questions in `backend/seed_questions.py`
- Modify styling in `frontend/css/style.css`
- Add more security features as needed
- Deploy to production server

Happy coding! 🚀
