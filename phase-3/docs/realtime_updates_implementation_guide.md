# Real-Time Task Updates Implementation Guide

## Overview
This guide explains how to implement real-time task updates in the frontend to complement the backend WebSocket implementation.

## Backend WebSocket Implementation
The backend has been updated to:
1. Emit real-time updates when tasks are created, updated, or deleted
2. Provide a WebSocket endpoint at `/ws/tasks/{user_id}`
3. Send structured messages with task data and timestamps

## Frontend Implementation

### 1. WebSocket Connection Management
Create a WebSocket service to manage the connection:

```javascript
// TaskWebSocketService.js
class TaskWebSocketService {
  constructor(userId) {
    this.userId = userId;
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectInterval = 3000; // 3 seconds
  }

  connect(onMessage, onError) {
    const wsUrl = `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/ws/tasks/${this.userId}`;
    
    this.ws = new WebSocket(wsUrl);
    
    this.ws.onopen = () => {
      console.log('Connected to task updates WebSocket');
      this.reconnectAttempts = 0; // Reset on successful connection
    };
    
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data);
    };
    
    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      if (onError) onError(error);
    };
    
    this.ws.onclose = () => {
      console.log('WebSocket connection closed');
      
      // Attempt to reconnect if we haven't exceeded max attempts
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        setTimeout(() => {
          this.reconnectAttempts++;
          this.connect(onMessage, onError);
        }, this.reconnectInterval);
      }
    };
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

export default TaskWebSocketService;
```

### 2. React Hook Implementation
Create a custom hook to manage WebSocket connections in React components:

```javascript
// useTaskUpdates.js
import { useState, useEffect, useCallback } from 'react';
import TaskWebSocketService from './TaskWebSocketService';

const useTaskUpdates = (userId, currentTasks, setCurrentTasks) => {
  const [isConnected, setIsConnected] = useState(false);
  const [connectionError, setConnectionError] = useState(null);

  const handleTaskUpdate = useCallback((data) => {
    switch (data.type) {
      case 'task_created':
        setCurrentTasks(prev => [...prev, data.task]);
        break;
      case 'task_updated':
        setCurrentTasks(prev => 
          prev.map(task => 
            task.id === data.task.id ? data.task : task
          )
        );
        break;
      case 'task_deleted':
        setCurrentTasks(prev => 
          prev.filter(task => task.id !== data.task_id)
        );
        break;
      default:
        console.warn('Unknown task update type:', data.type);
    }
  }, [setCurrentTasks]);

  const handleError = useCallback((error) => {
    setConnectionError('Failed to connect to real-time updates');
    console.error('WebSocket connection error:', error);
  }, []);

  useEffect(() => {
    if (!userId) return;

    const wsService = new TaskWebSocketService(userId);
    
    wsService.connect(
      (data) => {
        setIsConnected(true);
        setConnectionError(null);
        handleTaskUpdate(data);
      },
      (error) => {
        setIsConnected(false);
        handleError(error);
      }
    );

    return () => {
      wsService.disconnect();
    };
  }, [userId, handleTaskUpdate, handleError]);

  return { isConnected, connectionError };
};

export default useTaskUpdates;
```

### 3. Integration in Task List Component
Integrate the hook into your task list component:

```javascript
// TaskList.jsx
import React, { useState, useEffect } from 'react';
import useTaskUpdates from '../hooks/useTaskUpdates';
import { useAuth } from '../contexts/AuthContext'; // Assuming you have auth context

const TaskList = () => {
  const [tasks, setTasks] = useState([]);
  const { user } = useAuth(); // Get current user from auth context
  const { isConnected, connectionError } = useTaskUpdates(user?.id, tasks, setTasks);

  // Fetch initial tasks
  useEffect(() => {
    if (user?.id) {
      fetchTasks();
    }
  }, [user?.id]);

  const fetchTasks = async () => {
    try {
      const response = await fetch(`/api/${user.id}/tasks`);
      const data = await response.json();
      setTasks(data);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    }
  };

  return (
    <div className="task-list">
      <div className="realtime-status">
        {connectionError ? (
          <span className="error">⚠️ {connectionError}</span>
        ) : (
          <span className={`status ${isConnected ? 'connected' : 'disconnected'}`}>
            {isConnected ? '🟢 Connected' : '🟡 Connecting...'}
          </span>
        )}
      </div>
      
      <div className="tasks">
        {tasks.map(task => (
          <TaskItem key={task.id} task={task} />
        ))}
      </div>
    </div>
  );
};

export default TaskList;
```

### 4. Chat Component Integration
Also integrate real-time updates in the chat component to show when tasks are modified:

```javascript
// ChatInterface.jsx
import React, { useRef, useEffect } from 'react';
import useTaskUpdates from '../hooks/useTaskUpdates';
import { useAuth } from '../contexts/AuthContext';

const ChatInterface = () => {
  const messagesEndRef = useRef(null);
  const { user } = useAuth();
  const { isConnected } = useTaskUpdates(user?.id, tasks, setTasks); // Assuming tasks state exists

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]); // Assuming messages state exists

  // Render chat interface
  return (
    <div className="chat-container">
      <div className="chat-messages">
        {/* Render messages */}
        <div ref={messagesEndRef} />
      </div>
      <div className="realtime-indicator">
        {isConnected && <span>🔄 Real-time updates active</span>}
      </div>
      {/* Chat input */}
    </div>
  );
};
```

## Implementation Notes

### Error Handling
- The WebSocket service includes automatic reconnection logic
- Connection status is displayed to users
- Errors are gracefully handled without breaking the UI

### Performance
- Only one WebSocket connection per user
- Efficient task updates without full page reloads
- Proper cleanup of connections when components unmount

### Security
- WebSocket connections are user-specific
- Authentication is handled via the user ID in the URL
- No sensitive data is transmitted through WebSockets

## Testing
1. Connect to WebSocket and verify connection status
2. Perform task operations via chatbot
3. Verify UI updates in real-time without refresh
4. Test disconnection/reconnection scenarios
5. Verify proper cleanup when leaving the page

This implementation will provide seamless real-time updates to the UI when tasks are created, updated, or deleted through the chatbot, enhancing the user experience significantly.