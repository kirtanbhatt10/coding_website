from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from .database import init_db
from .routes import auth, questions, submissions, leaderboard, admin, hall_of_fame
from .websocket import manager

app = FastAPI(title="Coding Competition Platform")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(questions.router)
app.include_router(submissions.router)
app.include_router(leaderboard.router)
app.include_router(admin.router)
app.include_router(hall_of_fame.router)

# Mount static files
import pathlib
BASE_DIR = pathlib.Path(__file__).parent.parent.parent
STATIC_DIR = BASE_DIR / "static"
FRONTEND_DIR = BASE_DIR / "frontend"

os.makedirs(str(STATIC_DIR / "logo"), exist_ok=True)

# Mount static directories
# Main static directory (covers /static/css, /static/js, /static/logo)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# WebSocket endpoints
@app.websocket("/ws/lobby")
async def websocket_lobby(websocket: WebSocket):
    await manager.connect(websocket, "lobby")
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back or handle lobby messages
            await manager.send_personal_message({"type": "pong"}, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, "lobby")

@app.websocket("/ws/leaderboard")
async def websocket_leaderboard(websocket: WebSocket):
    await websocket.accept()
    session_id = websocket.query_params.get("session_id")
    await manager.connect(websocket, "leaderboard", session_id, already_accepted=True)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle leaderboard updates
    except WebSocketDisconnect:
        manager.disconnect(websocket, "leaderboard", session_id)

@app.websocket("/ws/contest")
async def websocket_contest(websocket: WebSocket):
    await websocket.accept()
    session_id = websocket.query_params.get("session_id")
    await manager.connect(websocket, "contest", session_id, already_accepted=True)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle contest updates
    except WebSocketDisconnect:
        manager.disconnect(websocket, "contest", session_id)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("Database initialized")

# Get base directory (already defined above)

@app.get("/")
async def root():
    return FileResponse(str(FRONTEND_DIR / "index.html"))

@app.get("/lobby")
async def lobby():
    return FileResponse(str(FRONTEND_DIR / "lobby.html"))

@app.get("/contest")
async def contest():
    return FileResponse(str(FRONTEND_DIR / "contest.html"))

@app.get("/leaderboard")
async def leaderboard_page():
    return FileResponse(str(FRONTEND_DIR / "leaderboard.html"))

@app.get("/hall-of-fame")
async def hall_of_fame_page():
    return FileResponse(str(FRONTEND_DIR / "hall-of-fame.html"))

@app.get("/admin")
async def admin_page():
    # Admin page requires authentication via frontend
    return FileResponse(str(FRONTEND_DIR / "admin.html"))

@app.get("/admin-login")
async def admin_login_page():
    return FileResponse(str(FRONTEND_DIR / "admin-login.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
