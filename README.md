# Coding Competition Platform

**A self-hosted website for running live Python coding contests, with a real-time leaderboard and a Hall of Fame.**

An organiser starts an event from the admin panel, players join a lobby, and everyone solves the
same set of questions against the clock. Submissions are run against test cases on the server and
the leaderboard updates for all players as results come in.

## Features

- **12 Python questions** across three difficulty levels, seeded with one command.
- **Live leaderboard and lobby** over WebSockets, with no page refreshes.
- **Automatic judging:** each submission runs against test cases with a time limit.
- **Admin panel:** start, end and reset events, upload a logo and export results.
- **Hall of Fame** that keeps winners between events.
- **Contest guard rails:** tab-switch detection, copy-paste disabled and a limit of 10 submissions per minute.
- **Dark and light themes**, and a layout that works on phones.

## Install and run

**Requirements:** Python 3.8 or later.

```bash
git clone https://github.com/kirtanbhatt10/coding_website.git
cd coding_website/backend
pip install -r requirements.txt
python seed_questions.py           # creates the database and the 12 questions
cd ..
python run_server.py               # serves the API and the website on port 8000
```

| Page | URL |
| --- | --- |
| Landing page | <http://localhost:8000/> |
| Admin panel | <http://localhost:8000/admin> |
| Hall of Fame | <http://localhost:8000/hall-of-fame> |

Players on the same network can join at `http://<your-ip>:8000`.

The full walkthrough for organisers and players, the API reference and troubleshooting are in
[docs/GUIDE.md](docs/GUIDE.md). There is also a short [QUICKSTART.md](QUICKSTART.md).

## Before you run a real event

- **Set your own admin password** when you create the event. The built-in default is public in this repository.
- **Run it only on a network you trust.** Submitted code is executed in a subprocess with a timeout. That is not a hardened sandbox, so a player could run arbitrary Python on the host.

## Tech stack

| Layer | Used |
| --- | --- |
| Backend | Python, FastAPI, Uvicorn |
| Database | SQLite with SQLAlchemy |
| Real-time | WebSockets |
| Frontend | HTML, CSS, JavaScript (no framework) |

## Project structure

```text
backend/app/        FastAPI app: routes, models, code executor, WebSocket manager
backend/            Seed and migration scripts, requirements
frontend/           HTML pages
static/             CSS and JavaScript
run_server.py       Starts everything
```
