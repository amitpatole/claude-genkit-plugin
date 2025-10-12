# Real-Time Collaboration for Genkit Applications

Build real-time, collaborative AI applications with WebSockets and Server-Sent Events (SSE).

## 🌟 Overview

Enable real-time features in your Genkit applications:
- 💬 Live chat with AI streaming
- 🤝 Collaborative document editing
- 📊 Real-time dashboards
- 🔔 Push notifications
- 👥 Multi-user sessions

## 🚀 Technologies

### WebSockets (Bidirectional)
- Full-duplex communication
- Low latency
- Binary data support
- Connection pooling

### Server-Sent Events (Unidirectional)
- HTTP-based streaming
- Auto-reconnection
- Event-driven
- Simpler implementation

## 📁 Structure

```
realtime-collaboration/
├── README.md
├── websocket/
│   ├── server.ts
│   ├── client.ts
│   └── presence.ts
├── sse/
│   ├── server.ts
│   └── streaming.ts
└── examples/
    ├── chat-room.ts
    ├── collaborative-rag.ts
    └── live-dashboard.ts
```

## 🎯 Use Cases

### 1. Real-Time Chat
```typescript
import { createChatRoom } from './examples/chat-room';

const room = createChatRoom('support-chat');
room.onMessage(async (msg) => {
  const response = await ai.generate(msg);
  room.broadcast(response);
});
```

### 2. Streaming AI Responses
```typescript
import { streamAIResponse } from './sse/streaming';

for await (const chunk of streamAIResponse(query)) {
  sendToClient(chunk);
}
```

### 3. Collaborative RAG
```typescript
import { collaborativeRAG } from './examples/collaborative-rag';

// Multiple users query same knowledge base
await collaborativeRAG.query(userId, question);
```

## 📊 Features

- ✅ WebSocket server with rooms
- ✅ SSE streaming for AI responses
- ✅ Presence tracking
- ✅ Message broadcasting
- ✅ Connection pooling
- ✅ Auto-reconnection
- ✅ Error handling
- ✅ Rate limiting

## 🔧 Quick Start

### WebSocket Server
```typescript
import { WebSocketServer } from './websocket/server';

const wss = new WebSocketServer({
  port: 8080,
  path: '/ws'
});

wss.on('connection', (client) => {
  client.on('message', async (data) => {
    const response = await processMessage(data);
    client.send(response);
  });
});
```

### SSE Streaming
```typescript
import { SSEServer } from './sse/server';

app.get('/stream', async (req, res) => {
  const sse = new SSEServer(res);

  for await (const chunk of aiStream(query)) {
    sse.send(chunk);
  }

  sse.close();
});
```

## 🔐 Security

- Authentication tokens
- Rate limiting
- Message validation
- CORS configuration
- SSL/TLS encryption

## 📚 Resources

- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [Socket.io](https://socket.io/)

---

**Build real-time AI experiences!** 🚀
