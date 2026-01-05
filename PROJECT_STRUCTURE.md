# Project Structure

This document describes the standard Django + Next.js project structure.

## Directory Layout

```
PostAutomation/
│
├── README.md                 # Main project documentation
├── .gitignore               # Git ignore rules
├── requirements.txt        # Python dependencies
├── manage.py               # Django management script
│
├── capabilities/           # Django app: Platform capability evaluation
│   ├── __init__.py
│   ├── apps.py
│   ├── service.py          # Core availability evaluation logic
│   ├── tests.py
│   └── views.py            # API endpoints
│
├── posts/                  # Django app: Post management
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py           # Post and PostTarget models
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # PostViewSet and publish endpoint
│   ├── tasks.py            # Celery tasks for publishing
│   ├── tests.py
│   └── migrations/          # Database migrations
│
├── social/                 # Django app: Social media accounts
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py           # Platform and SocialAccount models
│   └── migrations/         # Database migrations
│
├── postautomation/         # Django project settings
│   ├── __init__.py
│   ├── settings.py         # Django settings (CORS configured)
│   ├── urls.py             # Root URL configuration
│   ├── wsgi.py             # WSGI config
│   ├── asgi.py             # ASGI config
│   └── celery.py           # Celery configuration
│
├── media/                  # User-uploaded media files
│   └── images/
│
├── db.sqlite3              # SQLite database (not in git)
│
└── frontend/               # Next.js frontend application
    ├── package.json        # Node.js dependencies
    ├── package-lock.json   # Locked dependencies
    ├── tsconfig.json       # TypeScript configuration
    ├── next.config.js      # Next.js configuration
    ├── tailwind.config.js # Tailwind CSS configuration
    ├── postcss.config.js   # PostCSS configuration
    ├── components.json     # shadcn/ui configuration
    │
    ├── app/                # Next.js App Router
    │   ├── layout.tsx      # Root layout with AuthProvider
    │   ├── page.tsx       # Landing page
    │   ├── globals.css     # Global styles
    │   ├── login/          # Login page
    │   ├── dashboard/      # Dashboard page
    │   ├── posts/          # Post management pages
    │   │   ├── create/    # Create post page
    │   │   └── [id]/       # Post details page
    │   └── settings/       # Settings page
    │
    ├── components/         # React components
    │   ├── ui/             # shadcn/ui components
    │   │   ├── background-paths.tsx
    │   │   ├── button.tsx
    │   │   ├── card.tsx
    │   │   ├── input.tsx
    │   │   ├── label.tsx
    │   │   └── textarea.tsx
    │   ├── layout/         # Layout components
    │   │   ├── navbar.tsx
    │   │   └── app-layout.tsx
    │   ├── platform-selector.tsx
    │   └── protected-route.tsx
    │
    ├── contexts/           # React contexts
    │   └── AuthContext.tsx
    │
    ├── lib/                # Utilities and API client
    │   ├── api.ts          # Axios client and API functions
    │   └── utils.ts        # Utility functions (cn helper)
    │
    └── Documentation/
        ├── FRONTEND_SETUP.md
        ├── INTEGRATION_SUMMARY.md
        └── SETUP_INSTRUCTIONS.md
```

## Django Apps

### capabilities/
Handles platform availability evaluation based on:
- Content type (TEXT, PHOTO, VIDEO)
- Connected social accounts
- Account types and permissions
- Platform-specific requirements

**Key Files:**
- `service.py`: Core evaluation logic with platform-specific rules
- `views.py`: API endpoints for capabilities and validation

### posts/
Manages post creation, storage, and publishing.

**Key Files:**
- `models.py`: Post and PostTarget models
- `views.py`: REST API endpoints (CRUD + publish)
- `tasks.py`: Celery tasks for async publishing

### social/
Manages social media account connections.

**Key Files:**
- `models.py`: Platform enum and SocialAccount model

## Frontend Structure

### Next.js App Router
All pages use the App Router pattern:
- `app/layout.tsx`: Root layout with providers
- `app/page.tsx`: Landing page
- `app/*/page.tsx`: Route pages

### Component Organization
- `components/ui/`: Reusable UI components (shadcn/ui)
- `components/layout/`: Layout components (navbar, app layout)
- `components/`: Feature-specific components

### API Integration
- `lib/api.ts`: Centralized API client with TypeScript types
- All API calls use axios with interceptors
- Type-safe request/response handling

## Configuration Files

### Backend
- `requirements.txt`: Python dependencies
- `postautomation/settings.py`: Django settings with CORS

### Frontend
- `package.json`: Node.js dependencies
- `tsconfig.json`: TypeScript configuration
- `tailwind.config.js`: Tailwind CSS with shadcn theme
- `next.config.js`: Next.js configuration

## Git Structure

The repository follows standard practices:
- `.gitignore`: Excludes node_modules, __pycache__, .env files, etc.
- `README.md`: Main project documentation
- Separate commits for logical changes

## Development Workflow

1. **Backend Development**: Work in root Django apps
2. **Frontend Development**: Work in `frontend/` directory
3. **API Integration**: Update `frontend/lib/api.ts` for new endpoints
4. **Commits**: Commit and push after each logical change

## Standard Django Patterns

This project follows Django best practices:
- Apps organized by feature (capabilities, posts, social)
- Models in `models.py`
- Views in `views.py` (using DRF ViewSets)
- Serializers in `serializers.py`
- Tests in `tests.py`
- Migrations in `migrations/`

## Standard Next.js Patterns

This project follows Next.js 14 App Router patterns:
- Pages in `app/` directory
- Components in `components/` directory
- Shared utilities in `lib/` directory
- Contexts in `contexts/` directory
- TypeScript for type safety
- Tailwind CSS for styling

