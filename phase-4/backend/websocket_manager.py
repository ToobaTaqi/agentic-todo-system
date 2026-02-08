"""WebSocket manager for real-time task updates."""
import asyncio
from typing import Dict, List, Set
from fastapi import WebSocket, WebSocketDisconnect
from uuid import UUID
import json


class ConnectionManager:
    def __init__(self):
        # Store connections by user_id
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        self.active_connections[user_id].add(websocket)

    def disconnect(self, websocket: WebSocket, user_id: str):
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            if not self.active_connections[user_id]:  # Remove empty sets
                del self.active_connections[user_id]

    async def broadcast_to_user(self, message: dict, user_id: str):
        """Send a message to all connected websockets for a specific user."""
        if user_id in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except WebSocketDisconnect:
                    disconnected.add(connection)
            
            # Clean up disconnected connections
            for connection in disconnected:
                self.active_connections[user_id].discard(connection)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def broadcast_to_all_users(self, message: dict):
        """Send a message to all connected websockets for all users."""
        disconnected_users = []
        for user_id, connections in self.active_connections.items():
            disconnected = set()
            for connection in connections:
                try:
                    await connection.send_text(json.dumps(message))
                except WebSocketDisconnect:
                    disconnected.add(connection)
            
            # Clean up disconnected connections for this user
            for connection in disconnected:
                connections.discard(connection)
            if not connections:
                disconnected_users.append(user_id)
        
        # Remove users with no connections
        for user_id in disconnected_users:
            if user_id in self.active_connections:
                del self.active_connections[user_id]


# Global instance
manager = ConnectionManager()