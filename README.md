# Coding Competition Platform

A complete multi-user coding competition website built with Python FastAPI, featuring real-time leaderboards, secure code execution, and a persistent Hall of Fame.

## 🚀 Quick Start (TL;DR)

If you just want to get it running quickly:

```bash
# 1. Install dependencies
cd backend
pip install -r requirements.txt

# 2. Seed database with questions
python seed_questions.py

# 3. Start server (from project root) - This serves both backend AND frontend!
cd ..
python run_server.py

# 4. Open in browser
# Go to: http://localhost:8000
# You'll see a beautiful, modern website with gradients and animations!
```

**For detailed step-by-step instructions, see the [Installation & Setup](#installation--setup) section below.**

## 🎨 Modern Frontend Design

This website features a **stunning, modern frontend** with:

- ✨ **Animated gradient backgrounds** - No boring white pages!
- 🎭 **Glassmorphism effects** - Frosted glass design elements
- 🌈 **Beautiful color schemes** - Professional gradients throughout
- 🎬 **Smooth animations** - Every interaction is animated
- 🌓 **Dark/Light mode** - Toggle between themes seamlessly
- 📱 **Fully responsive** - Works perfectly on all devices
- 🎯 **Modern UI components** - Cards, buttons, and forms with style
- ⚡ **Performance optimized** - Fast loading and smooth scrolling

**Each page has a unique, visually appealing design that's far from boring!**

## Features

- 🎯 **12 Python Coding Questions** - Balanced difficulty across 3 levels
- 👥 **Multi-User Support** - Multiple players can compete simultaneously
- 🏆 **Live Leaderboard** - Real-time rankings with WebSocket updates
- 🎨 **Hall of Fame** - Persistent storage of winners and achievements
- 🔒 **Security Features** - Tab switching detection, rate limiting, sandboxed execution
- 🎭 **Dark/Light Mode** - Toggle between themes
- 📊 **Admin Panel** - Full control over events, logo upload, and data export
- ⚡ **Real-Time Updates** - WebSocket-based live updates

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Real-Time**: WebSockets
- **Code Execution**: Secure Python sandbox

## Project Structure

```
coding_website/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── database.py          # Database configuration
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── code_executor.py    # Secure code execution
│   │   ├── security.py          # Security features
│   │   ├── websocket.py         # WebSocket manager
│   │   └── routes/
│   │       ├── auth.py          # Authentication endpoints
│   │       ├── questions.py     # Question endpoints
│   │       ├── submissions.py   # Code submission endpoints
│   │       ├── leaderboard.py   # Leaderboard endpoints
│   │       ├── admin.py         # Admin endpoints
│   │       └── hall_of_fame.py  # Hall of Fame endpoints
│   ├── seed_questions.py        # Database seeding script
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── index.html               # Landing page
│   ├── lobby.html              # Waiting lobby
│   ├── contest.html            # Contest interface
│   ├── leaderboard.html        # Leaderboard page
│   ├── hall-of-fame.html       # Hall of Fame page
│   ├── admin.html              # Admin panel
│   ├── css/
│   │   └── style.css           # Main stylesheet
│   └── js/
│       ├── main.js             # Utility functions
│       ├── lobby.js            # Lobby functionality
│       ├── contest.js          # Contest functionality
│       ├── leaderboard.js      # Leaderboard functionality
│       ├── hall-of-fame.js     # Hall of Fame functionality
│       └── admin.js            # Admin functionality
├── static/
│   └── logo/                   # College logo storage
└── README.md                   # This file
```

## Installation & Setup

### Prerequisites

Before starting, ensure you have:
- **Python 3.8 or higher** installed on your system
- **pip** (Python package manager) - usually comes with Python
- **Internet connection** (for downloading packages)

#### Check Python Installation

Open your terminal/command prompt and verify Python is installed:

```bash
python --version
```

or

```bash
python3 --version
```

You should see something like `Python 3.8.x` or higher. If not, download Python from [python.org](https://www.python.org/downloads/).

### Step-by-Step Installation

#### Step 1: Navigate to Project Directory

Open your terminal/command prompt and navigate to the project folder:

```bash
cd path/to/coding_website
```

For example:
- Windows: `cd C:\Users\YourName\Desktop\coding_website`
- Mac/Linux: `cd ~/Desktop/coding_website`

#### Step 2: Install Python Dependencies

Navigate to the backend folder and install all required packages:

```bash
cd backend
pip install -r requirements.txt
```

**Note for Windows users:** If `pip` doesn't work, try `python -m pip install -r requirements.txt`

**Note for Mac/Linux users:** You might need to use `pip3` instead of `pip`, or `python3 -m pip install -r requirements.txt`

This will install:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- SQLAlchemy (database ORM)
- WebSockets (real-time communication)
- And other required packages

**Expected output:** You should see packages being downloaded and installed. Wait until you see "Successfully installed..." messages.

#### Step 3: Seed Database with Questions

While still in the `backend` directory, run the seeding script to populate the database with 12 Python coding questions:

```bash
python seed_questions.py
```

or

```bash
python3 seed_questions.py
```

**Expected output:** You should see:
```
Successfully seeded 12 questions!
```

This creates:
- 4 Beginner questions (Level 1)
- 4 Intermediate questions (Level 2)
- 4 Advanced questions (Level 3)

#### Step 4: Start the Backend Server

The backend server also serves the frontend automatically. You have two options:

**Option A: Using the startup script (Recommended - Easiest)**

From the project root directory (not inside backend folder):

```bash
python run_server.py
```

or

```bash
python3 run_server.py
```

**Option B: Using uvicorn directly**

From the `backend` directory:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
==================================================
Coding Competition Platform
==================================================

Starting server on http://localhost:8000

Access the application at:
  - Landing Page: http://localhost:8000/
  - Admin Panel: http://localhost:8000/admin
  - Hall of Fame: http://localhost:8000/hall-of-fame

Press Ctrl+C to stop the server
==================================================
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
Database initialized
INFO:     Application startup complete.
```

**Important:** 
- Keep this terminal window open while using the website
- The server must be running for both backend API and frontend to work
- The frontend is automatically served by the backend - no separate frontend server needed!

#### Step 5: Open the Frontend Website in Your Browser

**The frontend is automatically available when the backend server is running!**

Once you see the server running message, follow these steps:

1. **Open Your Web Browser**
   - Use any modern browser: Chrome, Firefox, Edge, Safari, Opera
   - Make sure JavaScript is enabled (enabled by default)

2. **Navigate to the Website**
   - Type in the address bar: `http://localhost:8000`
   - Press Enter
   - You should see the beautiful landing page with gradient background

3. **Alternative Access Methods**
   - Click this link: [http://localhost:8000](http://localhost:8000)
   - Or use: `http://127.0.0.1:8000`

4. **Verify Everything is Working**
   - You should see:
     - Modern gradient background with animated particles
     - Styled registration form
     - Smooth animations
     - Professional UI design
   - If you see an error, check that:
     - The server is running in your terminal
     - No error messages appear in the terminal
     - You're using the correct URL

**Note:** The frontend and backend run together - when you start the backend server, the frontend is automatically available at the same URL. There's no need to run a separate frontend server!

**Other Important Pages:**
- **Admin Panel**: `http://localhost:8000/admin`
- **Hall of Fame**: `http://localhost:8000/hall-of-fame`
- **Leaderboard**: `http://localhost:8000/leaderboard` (after contest starts)

### First-Time Setup (Admin)

Before players can join, you need to set up an event:

1. **Open Admin Panel**
   - Go to `http://localhost:8000/admin` in your browser

2. **Create an Event**
   - Enter an event name (e.g., "Spring Coding Competition 2024")
   - Click the "Create Event" button
   - You should see "Event created successfully!" message

3. **Upload College Logo (Optional but Recommended)**
   - Click "Choose File" under "Upload College Logo"
   - Select a PNG or JPG image file from your computer
   - Click "Upload Logo" button
   - The logo will appear in the preview and on all pages

4. **Verify Setup**
   - Check that the event name appears under "Current Event"
   - The logo should be visible in the navbar

### Testing the Website

#### As an Admin:

1. **Start the Contest**
   - Go to `/admin`
   - Click "Start Contest" button
   - All players in the lobby will be automatically redirected

2. **Monitor Progress**
   - Check the leaderboard to see player scores
   - Monitor real-time updates

3. **Stop the Contest**
   - Click "Stop Contest" when finished
   - Results will be finalized and added to Hall of Fame

#### As a Player:

1. **Register**
   - Go to `http://localhost:8000/`
   - Enter your name
   - Select your college year (1st, 2nd, 3rd, or 4th)
   - Click "Join Competition"

2. **Wait in Lobby**
   - You'll be redirected to the waiting lobby
   - Wait for the admin to start the contest

3. **Compete**
   - Once started, you'll see the first question
   - Write Python code in the editor
   - Click "Run Code" to test your solution
   - Click "Submit" when ready
   - Progress through all 12 questions

4. **View Results**
   - Check the live leaderboard
   - See your rank and score

### Stopping the Server

To stop the server:
- Press `Ctrl + C` in the terminal where the server is running
- The server will shut down gracefully

### Verifying Everything Works

1. **Check Server Status**
   - The terminal should show "Uvicorn running on http://0.0.0.0:8000"
   - No error messages should appear

2. **Test Website Access**
   - Open `http://localhost:8000` in your browser
   - You should see the landing page with registration form
   - If you see an error, check the terminal for error messages

3. **Test Admin Panel**
   - Go to `http://localhost:8000/admin`
   - You should see the admin control panel
   - Try creating an event

4. **Test Database**
   - After seeding, a file named `competition.db` should be created in the `backend` directory
   - This confirms the database is working

### Common Issues & Solutions

**Issue: "python: command not found"**
- **Solution:** Use `python3` instead of `python`, or install Python

**Issue: "pip: command not found"**
- **Solution:** Use `python -m pip` or `python3 -m pip` instead

**Issue: "Port 8000 already in use"**
- **Solution:** 
  - Close other applications using port 8000, OR
  - Change the port in `run_server.py` to 8001 or another port
  - Then access the website at `http://localhost:8001`

**Issue: "Module not found" errors**
- **Solution:** Make sure you installed requirements: `pip install -r requirements.txt`

**Issue: Website shows "Connection refused"**
- **Solution:** Make sure the server is running in a terminal window

**Issue: Database errors**
- **Solution:** Delete `backend/competition.db` and restart the server (it will recreate automatically)

### Accessing from Other Devices on Same Network

If you want to access the website from other devices (phones, tablets, other computers):

1. Find your computer's IP address:
   - Windows: Open Command Prompt, type `ipconfig`, look for "IPv4 Address"
   - Mac/Linux: Open Terminal, type `ifconfig` or `ip addr`, look for your network IP

2. Access from other device:
   - Use `http://YOUR_IP_ADDRESS:8000` instead of `localhost:8000`
   - Example: `http://192.168.1.100:8000`

**Note:** Make sure your firewall allows connections on port 8000

### What to Expect When You First Open the Website

When you navigate to `http://localhost:8000` for the first time, you'll see a **beautiful, modern website** with:

1. **Landing Page** (`/`)
   - **Animated gradient background** with floating particles
   - **Floating college logo** (if uploaded) with smooth animation
   - **Glassmorphism registration form** with:
     - Modern styled input fields
     - Gradient buttons with hover effects
     - Smooth animations
   - Player Name input with focus effects
   - College Year dropdown with modern styling
   - "Join Competition" button with gradient and ripple effect
   - Navigation bar with gradient text and hover animations

2. **Admin Panel** (`/admin`)
   - **Modern card-based layout** with glassmorphism
   - Gradient borders and shadows
   - Event management section with styled inputs
   - Logo upload with preview
   - **Colorful control buttons** (Start/Stop/Reset) with gradients
   - Export buttons with modern styling
   - Current event status with visual indicators

3. **After Registration** (`/lobby`)
   - **Animated waiting lobby** with gradient background
   - **Player cards** with hover effects and animations
   - Smooth card entrance animations
   - Real-time player list updates
   - Pulsing waiting message
   - Modern typography and spacing

4. **During Contest** (`/contest`)
   - **Split-screen layout** with modern design
   - Question panel with:
     - Gradient level badges
     - Animated timer with color changes
     - Styled code editor (dark theme)
     - Gradient buttons (Run/Submit)
     - Test results with color-coded cards
   - Sidebar with:
     - Animated progress bars with shimmer effect
     - Mini leaderboard with modern cards
     - Score display with gradient text

5. **Leaderboard** (`/leaderboard`)
   - **Modern table design** with:
     - Gradient header
     - Hover effects on rows
     - Special badges for top 3 (gold, silver, bronze gradients)
     - Smooth animations
     - Glassmorphism effect
   - Real-time updates with smooth transitions

6. **Hall of Fame** (`/hall-of-fame`)
   - **Beautiful card grid layout**
   - Special gradient borders for top 3
   - Hover animations with scale and glow effects
   - Event grouping with modern headers
   - Smooth card entrance animations
   - Gradient text for ranks and names

**All pages feature:**
- Modern gradient backgrounds (not plain white!)
- Smooth animations and transitions
- Glassmorphism effects (frosted glass look)
- Professional color schemes
- Responsive design
- Dark/Light mode support
- Custom scrollbars
- Hover effects everywhere

## How to Open Both Backend and Frontend

### Understanding the Architecture

**Important:** This project uses a unified architecture where:
- The **backend server** (FastAPI) serves both:
  - API endpoints (for data and functionality)
  - Frontend files (HTML, CSS, JavaScript)
- **No separate frontend server needed!**
- When you start the backend, the frontend is automatically available

### Starting Both Backend and Frontend Together

Since the backend serves the frontend, you only need to start one server:

1. **Start the Backend Server** (which includes frontend)
   ```bash
   python run_server.py
   ```

2. **Open Your Browser**
   - The frontend is immediately available at `http://localhost:8000`
   - No additional steps needed!

### Opening the Frontend in Your Browser

Once the server is running, follow these steps:

1. **Open Your Web Browser**
   - Use any modern browser: Chrome, Firefox, Edge, Safari, etc.
   - Make sure JavaScript is enabled (it's enabled by default)

2. **Navigate to the Website**
   - Type in the address bar: `http://localhost:8000`
   - Press Enter
   - You should see the **beautiful modern landing page** with:
     - Animated gradient background
     - Floating logo animation
     - Styled registration form with glassmorphism effect
     - Smooth animations and transitions

3. **Alternative Access Methods**
   - Click this link: [http://localhost:8000](http://localhost:8000)
   - Or use: `http://127.0.0.1:8000`

4. **Verify the Website is Working**
   - You should see:
     - Modern, colorful design (not boring white pages!)
     - Animated background with gradient particles
     - Professional UI with smooth transitions
     - Registration form with modern styling
   - If you see an error:
     - Check that the server is running in your terminal
     - Look for error messages in the terminal
     - Verify you're using the correct URL

### Frontend Design Features

The frontend includes:
- **Modern gradient backgrounds** with animated particles
- **Glassmorphism effects** (frosted glass look)
- **Smooth animations** on all interactions
- **Dark/Light mode** with beautiful transitions
- **Responsive design** that works on all devices
- **Professional color schemes** with gradients
- **Hover effects** and interactive elements
- **Custom scrollbars** and styled components

Each page has a unique, modern design - no boring white pages!

### Available Pages and URLs

Here are all the pages you can access:

| Page | URL | Description |
|------|-----|-------------|
| **Landing Page** | `http://localhost:8000/` | Player registration page |
| **Admin Panel** | `http://localhost:8000/admin` | Admin control panel |
| **Waiting Lobby** | `http://localhost:8000/lobby` | Players wait here before contest starts |
| **Contest Page** | `http://localhost:8000/contest` | Main coding interface |
| **Leaderboard** | `http://localhost:8000/leaderboard` | Live rankings |
| **Hall of Fame** | `http://localhost:8000/hall-of-fame` | Past winners archive |

**Note:** Some pages require authentication or will redirect you if accessed directly.

## Complete Website Operation Guide

### 📋 Complete Admin Workflow

#### Step 1: Initial Setup

1. **Open Admin Panel**
   - Navigate to: `http://localhost:8000/admin`
   - You should see the admin control panel

2. **Create an Event**
   - In the "Event Management" section:
     - Type an event name in the "Event Name" field (e.g., "Spring Coding Competition 2024")
     - Click the **"Create Event"** button
     - You should see a success message
     - The event name will appear under "Current Event"

3. **Upload College Logo** (Optional but Recommended)
   - In the "Upload College Logo" section:
     - Click **"Choose File"** or **"Browse"** button
     - Select a logo image file from your computer (PNG or JPG format)
     - The file name will appear next to the button
     - Click **"Upload Logo"** button
     - You should see a preview of the logo
     - The logo will now appear on all pages (navbar and hero sections)

#### Step 2: Pre-Contest Preparation

1. **Verify Event Status**
   - Check the "Current Event" section
   - It should show your event name with "(Inactive)" status
   - The "Start Contest" button should be enabled

2. **Wait for Players to Join**
   - Players will register at the landing page (`http://localhost:8000/`)
   - They will be redirected to the waiting lobby
   - You can monitor how many players have joined (if you have access to lobby)

#### Step 3: Starting the Contest

1. **Start the Contest**
   - When ready to begin:
     - Click the **"Start Contest"** button in the "Contest Controls" section
     - A confirmation dialog will appear
     - Click **"OK"** to confirm
     - You should see a success message: "Contest started!"
   - **What happens:**
     - All players in the lobby are automatically redirected to the contest page
     - The event status changes to "(Active)"
     - The "Start Contest" button becomes disabled
     - The "Stop Contest" button becomes enabled

2. **Monitor the Contest**
   - Open the leaderboard page: `http://localhost:8000/leaderboard`
   - You'll see real-time updates as players solve questions
   - Rankings update automatically via WebSocket

#### Step 4: During the Contest

1. **Monitor Progress**
   - Keep the leaderboard page open to see:
     - Current rankings
     - Scores updating in real-time
     - Number of questions solved by each player
     - Total time taken

2. **View Individual Progress** (if needed)
   - You can check the contest page to see what questions players are working on
   - Note: You'll need to register as a player to fully experience the contest interface

#### Step 5: Ending the Contest

1. **Stop the Contest**
   - When the contest time is up or you want to end it:
     - Go back to the admin panel: `http://localhost:8000/admin`
     - Click the **"Stop Contest"** button
     - A confirmation dialog will appear asking to finalize results
     - Click **"OK"** to confirm
   - **What happens:**
     - Contest ends immediately
     - All players are notified
     - Top 10 winners are automatically added to Hall of Fame
     - Leaderboard is finalized
     - Event status changes to "(Inactive)"

2. **View Final Results**
   - Go to the leaderboard: `http://localhost:8000/leaderboard`
   - Final rankings are displayed
   - Go to Hall of Fame: `http://localhost:8000/hall-of-fame`
   - Winners are now permanently recorded

#### Step 6: Exporting Data

1. **Export Leaderboard**
   - In the admin panel, under "Export Data" section:
     - Click **"Export Leaderboard (CSV)"** button
     - A CSV file will be downloaded to your computer
     - File name format: `leaderboard_[EventName]_[Timestamp].csv`
     - Open in Excel, Google Sheets, or any spreadsheet application

2. **Export Hall of Fame**
   - Click **"Export Hall of Fame (CSV)"** button
     - A CSV file will be downloaded
     - File name format: `hall_of_fame_[Timestamp].csv`
     - Contains all historical winners

#### Step 7: Reset Contest (Optional)

If you want to run another contest with the same event:

1. **Reset the Contest**
   - Click the **"Reset Contest"** button
   - A warning dialog will appear (this action cannot be undone)
   - Click **"OK"** to confirm
   - **What happens:**
     - All player progress is cleared
     - All submissions are deleted
     - Leaderboard is cleared
     - Players' scores reset to 0
     - Players can register again and start fresh

**Warning:** This permanently deletes all contest data. Only use this if you want to start completely fresh.

---

### 🎮 Complete Player Workflow

#### Step 1: Registration

1. **Open the Landing Page**
   - Navigate to: `http://localhost:8000/`
   - You'll see the registration form

2. **Fill in Registration Details**
   - **Player Name:** Enter your full name or nickname
     - Example: "John Doe" or "JohnD"
   - **College Year:** Select your year from the dropdown:
     - 1st Year
     - 2nd Year
     - 3rd Year
     - 4th Year

3. **Join the Competition**
   - Click the **"Join Competition"** button
   - You'll be automatically redirected to the waiting lobby
   - Your session is saved in your browser

#### Step 2: Waiting in Lobby

1. **Lobby Page Features**
   - You'll see:
     - College logo (if uploaded by admin)
     - Event name
     - "Waiting Lobby" heading
     - Message: "Contest Not Started - Please wait for the admin to start the competition"
     - List of players who have joined
     - Player count

2. **What to Do**
   - Wait patiently for the admin to start the contest
   - You can see other players joining in real-time
   - The page will automatically redirect you when the contest starts
   - **Don't close the browser tab** - keep it open

3. **Navigation**
   - You can click "Hall of Fame" to view past winners while waiting
   - Use the theme toggle (🌓) to switch between dark and light mode

#### Step 3: Contest Begins

1. **Automatic Redirect**
   - When admin starts the contest, you'll be automatically taken to the contest page
   - You'll see the first question immediately

2. **Understanding the Contest Interface**

   **Left Side - Question Panel:**
   - **Level Badge:** Shows current level (1, 2, or 3) with color coding
     - Green = Level 1 (Beginner)
     - Yellow = Level 2 (Intermediate)
     - Red = Level 3 (Advanced)
   - **Question Title:** Name of the current question
   - **Timer:** Countdown timer (for Level 2 and 3 questions)
     - Turns yellow when < 30 seconds
     - Turns red and pulses when < 10 seconds
   - **Question Description:** Detailed problem statement
   - **Code Editor:** Dark-themed text area where you write Python code
   - **Run Code Button:** Test your solution without submitting
   - **Submit Button:** Submit your final answer
   - **Output Panel:** Shows execution results and errors
   - **Test Results:** Shows which test cases passed/failed

   **Right Side - Sidebar:**
   - **Your Progress:**
     - Level 1 progress bar (0/4, 1/4, etc.)
     - Level 2 progress bar
     - Level 3 progress bar
     - Your current score
   - **Top 5 Leaderboard:** Mini leaderboard showing top 5 players

#### Step 4: Solving Questions

1. **Read the Question Carefully**
   - Read the full problem description
   - Understand what input format is expected
   - Understand what output format is expected
   - Check the starter code (if provided)

2. **Write Your Solution**
   - Type your Python code in the code editor
   - **Important Notes:**
     - Copy-paste is disabled (security feature)
     - Code must read from `input()` for test cases
     - Code must print the result using `print()`
     - Follow Python syntax rules

3. **Test Your Code (Run Button)**
   - Click **"Run Code"** to test your solution
   - **What happens:**
     - Your code is executed with test cases
     - Output panel shows:
       - Success message if syntax is correct
       - Error messages if there are syntax errors
     - Test results show:
       - Which test cases passed (green)
       - Which test cases failed (red)
       - Expected vs actual output for failed tests
   - **Use this to debug** before submitting

4. **Submit Your Solution**
   - When you're confident your solution is correct:
     - Click the **"Submit"** button
   - **What happens:**
     - Your code is evaluated against all test cases
     - If correct:
       - You see "Correct! Question solved!" message
       - Your score increases
       - Next question automatically loads
       - Progress bars update
     - If incorrect:
       - You see "Incorrect solution. Please try again."
       - Error details are shown
       - You can modify and resubmit

5. **Progress Through Levels**
   - **Level 1 (Questions 1-4):**
     - No time limit
     - Basic Python concepts
     - 10 points each
   - **Level 2 (Questions 5-8):**
     - 30-second time limit per question
     - Functions, dictionaries, recursion
     - 15 points each
     - Timer appears and counts down
   - **Level 3 (Questions 9-12):**
     - 60-second time limit per question
     - Advanced algorithms
     - 20 points each
     - Auto-submits when time runs out

6. **Time Management Tips**
   - For timed questions, watch the timer
   - If time is running out, submit what you have
   - Questions auto-submit when timer reaches 0
   - You can't skip questions - must solve in order

#### Step 5: During the Contest

1. **Monitor Your Progress**
   - Check the progress sidebar:
     - See how many questions you've solved per level
     - Track your current score
   - Check the mini leaderboard:
     - See top 5 players
     - Compare your position

2. **View Full Leaderboard**
   - Click **"Leaderboard"** in the navbar
   - See all players' rankings
   - Updates in real-time
   - Shows:
     - Rank (with special badges for top 3)
     - Player name
     - College year
     - Score
     - Questions solved
     - Total time

3. **Navigation During Contest**
   - You can switch between Contest and Leaderboard pages
   - Your progress is saved automatically
   - You can return to the contest page to continue

#### Step 6: Contest Ends

1. **Automatic Notification**
   - When admin stops the contest, you'll see a notification
   - You may be redirected to the leaderboard

2. **View Final Results**
   - Go to the leaderboard page
   - See your final rank and score
   - See all other players' final positions

3. **Check Hall of Fame**
   - Go to: `http://localhost:8000/hall-of-fame`
   - If you're in the top 10, you'll see your name there
   - Top 3 winners have special highlighting
   - Your achievement is permanently recorded

---

### 🎨 Website Features and Controls

#### Theme Toggle (Dark/Light Mode)

**How to Use:**
- Click the **🌓** button in the top-right corner of any page
- Toggle between light and dark themes
- Your preference is saved in browser storage
- Applies to all pages

**When to Use:**
- Dark mode: Better for low-light environments, reduces eye strain
- Light mode: Traditional, easier to read in bright environments

#### Navigation Menu

Available on all pages:
- **Home/Logo:** Returns to landing page
- **Leaderboard:** View current rankings (only during/after contest)
- **Hall of Fame:** View past winners (always available)
- **Admin Panel:** Only accessible via direct URL (`/admin`)

#### Security Features (During Contest)

1. **Tab Switch Detection**
   - System monitors if you switch browser tabs
   - After 3 switches, you get a warning
   - After 5 switches, you may be disqualified
   - **Tip:** Stay focused on the contest page

2. **Copy-Paste Disabled**
   - Right-click is disabled in code editor
   - Copy (Ctrl+C) is blocked
   - Paste (Ctrl+V) is blocked
   - **Tip:** Type code manually - it's part of the challenge

3. **Rate Limiting**
   - Maximum 10 code submissions per minute
   - Prevents spam and abuse
   - **Tip:** Test thoroughly with "Run Code" before submitting

#### Real-Time Updates

- **Leaderboard:** Updates automatically every few seconds
- **Lobby:** Shows new players joining in real-time
- **Contest:** Progress updates in real-time
- **No need to refresh the page** - everything updates automatically

---

### 📱 Mobile/Tablet Access

The website is responsive and works on mobile devices:

1. **On the Same Network:**
   - Find your computer's IP address (see "Accessing from Other Devices" section)
   - On your phone/tablet, open browser
   - Go to: `http://YOUR_IP_ADDRESS:8000`
   - Example: `http://192.168.1.100:8000`

2. **Features on Mobile:**
   - All features work, but interface may be optimized for desktop
   - Code editor is usable but smaller
   - Leaderboard scrolls horizontally if needed
   - Touch-friendly buttons

---

### 🔄 Complete Contest Flow Example

Here's a complete example of running a contest from start to finish:

**Admin Side:**
1. ✅ Server running → Open `http://localhost:8000/admin`
2. ✅ Create event: "Spring 2024 Competition"
3. ✅ Upload college logo
4. ✅ Wait for players to register (monitor lobby)
5. ✅ Start contest when ready
6. ✅ Monitor leaderboard during contest
7. ✅ Stop contest after time limit
8. ✅ Export results as CSV
9. ✅ View Hall of Fame

**Player Side:**
1. ✅ Open `http://localhost:8000/`
2. ✅ Register: Name="Alice", Year="2nd"
3. ✅ Wait in lobby
4. ✅ Contest starts → Auto-redirected to contest page
5. ✅ Solve Question 1 (Level 1, no time limit)
6. ✅ Solve Question 2-4 (Level 1)
7. ✅ Unlock Level 2 → Solve Questions 5-8 (30s each)
8. ✅ Unlock Level 3 → Solve Questions 9-12 (60s each)
9. ✅ Check leaderboard periodically
10. ✅ Contest ends → View final rank
11. ✅ Check Hall of Fame if in top 10

---

### 💡 Tips for Best Experience

**For Admins:**
- Test the platform before the actual event
- Have a backup plan if server crashes
- Monitor the leaderboard during contest
- Export data immediately after contest ends
- Keep server terminal visible to monitor for errors

**For Players:**
- Use "Run Code" extensively before submitting
- Read questions carefully - understand input/output format
- Manage time wisely on timed questions
- Don't switch tabs during contest
- Check leaderboard to gauge your performance
- Stay calm and focused

**General:**
- Keep browser updated
- Use a stable internet connection
- Don't refresh pages unnecessarily (auto-updates work)
- Clear browser cache if you see old data
- Use Chrome or Firefox for best compatibility

## Question Structure

### Level 1 (Beginner) - Questions 1-4
- Basic Python: loops, conditionals, strings, lists
- No time limit
- 10 points each

### Level 2 (Intermediate) - Questions 5-8
- Functions, dictionaries, recursion
- 30-second time limit
- 15 points each

### Level 3 (Advanced) - Questions 9-12
- Algorithmic problems
- 60-second time limit
- 20 points each
- Auto-submit on timeout

## Security Features

- **Code Sandboxing**: Secure Python code execution
- **Rate Limiting**: Maximum 10 submissions per minute
- **Tab Switch Detection**: Warns users about switching tabs
- **Copy-Paste Disabled**: Prevents code copying during contest
- **Session Management**: Secure session-based authentication

## Database Schema

- **Users**: Player information and progress
- **Questions**: All coding questions with test cases
- **Submissions**: Code submissions and results
- **Events**: Contest events and settings
- **Leaderboard**: Real-time rankings
- **HallOfFame**: Persistent winner records

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `GET /api/auth/me/{session_id}` - Get user info

### Questions
- `GET /api/questions/` - Get available questions
- `GET /api/questions/{question_id}` - Get specific question

### Submissions
- `POST /api/submissions/run` - Run code (test)
- `POST /api/submissions/submit` - Submit code (evaluate)

### Leaderboard
- `GET /api/leaderboard/` - Get current leaderboard

### Admin
- `POST /api/admin/event` - Create event
- `POST /api/admin/upload-logo/{event_id}` - Upload logo
- `POST /api/admin/event/{event_id}/start` - Start contest
- `POST /api/admin/event/{event_id}/stop` - Stop contest
- `POST /api/admin/event/{event_id}/reset` - Reset contest
- `GET /api/admin/export/leaderboard/{event_id}` - Export leaderboard
- `GET /api/admin/export/hall-of-fame` - Export Hall of Fame

### Hall of Fame
- `GET /api/hall-of-fame/` - Get all Hall of Fame entries
- `GET /api/hall-of-fame/event/{event_name}` - Get entries by event

## WebSocket Endpoints

- `/ws/lobby` - Lobby updates
- `/ws/leaderboard` - Leaderboard updates
- `/ws/contest` - Contest updates

## Customization

### Adding New Questions

Edit `backend/seed_questions.py` and add questions to the `questions` list, then run:

```bash
python seed_questions.py
```

### Changing Time Limits

Modify `time_limit` values in question data or update the code executor timeout.

### Styling

Edit `frontend/css/style.css` to customize the appearance.

## Troubleshooting

### Database Issues
- Delete `competition.db` and restart the server to reset
- Run `seed_questions.py` again to re-seed questions

### Static Files Not Loading
- Ensure `static/` and `frontend/` directories exist
- Check file paths in `main.py`

### WebSocket Connection Failed
- Ensure server is running
- Check firewall settings
- Verify WebSocket endpoint URLs

## Production Deployment

For production deployment:

1. Use PostgreSQL instead of SQLite
2. Set up proper authentication (JWT tokens)
3. Use environment variables for configuration
4. Enable HTTPS
5. Set up proper logging
6. Use a production WSGI server (Gunicorn + Uvicorn workers)
7. Configure reverse proxy (Nginx)

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please check the code comments or create an issue in the repository.

---

**Built with ❤️ for competitive programming events**
