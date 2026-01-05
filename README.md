# PostAutomation

A full-stack application for automating social media posts across multiple platforms. Built with Django REST Framework backend and Next.js frontend.

## Project Structure

```
PostAutomation/
├── backend/                    # Django backend (root level)
│   ├── capabilities/          # Platform capability evaluation
│   ├── posts/                 # Post management app
│   ├── social/                # Social media account models
│   ├── postautomation/        # Django project settings
│   ├── manage.py
│   ├── requirements.txt
│   └── db.sqlite3
│
├── frontend/                   # Next.js frontend
│   ├── app/                   # Next.js app directory
│   ├── components/            # React components
│   ├── contexts/              # React contexts
│   ├── lib/                   # Utilities and API client
│   ├── package.json
│   └── tsconfig.json
│
└── README.md
```

## Features

- **Multi-Platform Publishing**: Publish to Instagram, Facebook, TikTok, YouTube, LinkedIn, and X (Twitter)
- **Content Type Support**: TEXT, PHOTO, and VIDEO posts
- **Platform Availability System**: Smart platform selection based on content type and account capabilities
- **Real-time Validation**: Check platform availability before publishing
- **Modern UI**: Beautiful, responsive interface with dark mode support

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start Django server
python manage.py runserver
```

The backend will run at `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will run at `http://localhost:3000`

## Backend API

### Endpoints

- `GET /capabilities?content_type={TEXT|PHOTO|VIDEO}` - Get platform availability
- `POST /capabilities/validate` - Validate post draft
- `GET /posts` - List all posts
- `GET /posts/{id}` - Get post details
- `POST /posts` - Create new post
- `PATCH /posts/{id}` - Update post
- `DELETE /posts/{id}` - Delete post
- `POST /posts/{id}/publish` - Publish post to platforms

### Platform Capabilities

The backend evaluates platform availability based on:

- **Instagram**: Requires Professional account with valid permissions
- **Facebook**: Requires connected Page (not personal profile)
- **TikTok**: Requires prerequisites met and photo posting enabled (for photos)
- **YouTube**: Only supports VIDEO content type
- **LinkedIn**: Requires proper API access/scope
- **X (Twitter)**: TEXT always available; PHOTO/VIDEO require media upload enabled

## Frontend Pages

- `/` - Landing page
- `/login` - User authentication
- `/dashboard` - Post management dashboard
- `/posts/create` - Create new post
- `/posts/[id]` - Post details and publishing
- `/settings` - Social media connections

## Technology Stack

### Backend
- Django 4.2+
- Django REST Framework
- Celery (for async tasks)
- django-cors-headers

### Frontend
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- shadcn/ui
- Framer Motion
- Axios

## Development

### Running Tests

```bash
# Backend tests
python manage.py test

# Frontend tests (if configured)
cd frontend
npm test
```

### Code Structure

- **Backend**: Follows Django best practices with apps for different features
- **Frontend**: Next.js App Router with component-based architecture
- **API Integration**: Centralized API client in `frontend/lib/api.ts`

## Documentation

- [Frontend Setup Guide](frontend/FRONTEND_SETUP.md)
- [Integration Summary](frontend/INTEGRATION_SUMMARY.md)

## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

