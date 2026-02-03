# Playto Community Feed Prototype

## Setup
1. Backend: `cd backend`, `pip install -r requirements.txt`, `python manage.py migrate`, `python manage.py runserver`.
2. Frontend: `cd frontend`, `npm install`, `npm start`.
3. Database: PostgreSQL (update settings.py).

## Features
- Feed with posts and likes.
- Threaded comments.
- Leaderboard: Top 5 by 24h karma.

## API
- GET/POST /api/posts/
- GET/POST /api/comments/?post_id=1
- POST /api/like/
- GET /api/leaderboard/