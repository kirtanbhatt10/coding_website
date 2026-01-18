from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
from datetime import datetime

class ConnectionManager:
    """Manages WebSocket connections for real-time updates"""
    
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {
            "lobby": [],
            "leaderboard": [],
            "contest": []
        }
        self.user_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, room: str, session_id: str = None, already_accepted: bool = False):
        """Connect a WebSocket to a room"""
        if not already_accepted:
            await websocket.accept()
        self.active_connections[room].append(websocket)
        if session_id:
            self.user_connections[session_id] = websocket
    
    def disconnect(self, websocket: WebSocket, room: str, session_id: str = None):
        """Disconnect a WebSocket from a room"""
        if websocket in self.active_connections[room]:
            self.active_connections[room].remove(websocket)
        if session_id and session_id in self.user_connections:
            del self.user_connections[session_id]
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to a specific connection"""
        await websocket.send_text(json.dumps(message))
    
    async def broadcast_to_room(self, message: dict, room: str):
        """Broadcast message to all connections in a room"""
        disconnected = []
        for connection in self.active_connections[room]:
            try:
                await connection.send_text(json.dumps(message))
            except:
                disconnected.append(connection)
        
        # Remove disconnected connections
        for conn in disconnected:
            self.disconnect(conn, room)
    
    async def send_to_user(self, message: dict, session_id: str):
        """Send message to a specific user"""
        if session_id in self.user_connections:
            try:
                await self.user_connections[session_id].send_text(json.dumps(message))
            except:
                pass

manager = ConnectionManager()
