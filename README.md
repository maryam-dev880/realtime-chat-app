# Real-Time Chat Application

A real-time chat application built with **Django** and **Django Channels**, allowing multiple users to join chat rooms and exchange messages instantly using WebSockets.

## Features

- **Real-time messaging** — messages are delivered instantly to all users in a room using WebSockets (no page refresh needed)
- **Room-based chat** — users can create or join chat rooms by name
- **Message persistence** — chat history is saved to the database and loaded when a user rejoins a room
- **Edit messages** — users can edit their own sent messages, with an "(edited)" label shown to all participants
- **Delete messages** — users can delete their own messages; a "This message was deleted" placeholder is shown (similar to WhatsApp), preserving conversation context
- **Session-based usernames** — users enter a username and room name to join, no account/login required
- **Responsive, styled UI** — built with Bootstrap for a clean chat interface

## Tech Stack

- **Backend:** Django, Django Channels
- **ASGI Server:** Daphne
- **Real-time layer:** WebSockets, Channels' In-Memory Channel Layer
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5

## Project Structure

```
realtime-chat-app/
├── chat/
│   ├── consumers.py      # WebSocket consumer (handles send/edit/delete logic)
│   ├── models.py          # Room and Message models
│   ├── routing.py         # WebSocket URL routing
│   ├── views.py           # Views for joining rooms
│   └── ...
├── chatapp/
│   ├── asgi.py            # ASGI application with WebSocket routing
│   ├── settings.py
│   └── ...
├── templates/
│   ├── home.html          # Join room page
│   └── room.html          # Chat room page
├── requirements.txt
└── manage.py
```

## Setup Instructions

1. **Clone the repository**
   ```
   git clone <repository-url>
   cd realtime-chat-app
   ```

2. **Create and activate a virtual environment**
   ```
   python -m venv venv
   venv\Scripts\activate   # Windows
   ```

3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the development server**
   ```
   python manage.py runserver
   ```

6. **Open in browser**
   ```
   http://127.0.0.1:8000/
   ```

## How It Works

- Users enter a username and room name on the home page to join a chat room.
- A WebSocket connection is established with the server via Django Channels.
- Messages sent by a user are broadcast in real time to everyone connected to the same room, and saved to the database.
- Users can edit or delete their own messages; these actions are also broadcast in real time so all participants see the update instantly.

## Future Improvements

- User authentication (proper login/signup instead of session-based usernames)
- Typing indicators
- Online/offline user status
- Multiple chat rooms list with search
- Deployment with Redis as the channel layer for production scalability