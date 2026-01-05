# Frontend Setup and Integration Guide

## Overview

This frontend is built with Next.js, React, TypeScript, Tailwind CSS, and shadcn/ui. It connects to the Django REST API backend for managing posts and publishing to multiple social media platforms.

## Project Structure

```
PostAutomation/
├── app/                    # Next.js app directory
│   ├── dashboard/         # Dashboard page
│   ├── login/             # Login page
│   ├── posts/             # Post management pages
│   │   ├── create/        # Create post page
│   │   └── [id]/          # Post details page
│   ├── settings/          # Settings/connections page
│   ├── layout.tsx         # Root layout with AuthProvider
│   ├── page.tsx          # Landing page
│   └── globals.css        # Global styles
├── components/
│   ├── ui/                # shadcn/ui components
│   │   ├── background-paths.tsx
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   ├── label.tsx
│   │   └── textarea.tsx
│   ├── layout/            # Layout components
│   │   ├── navbar.tsx
│   │   └── app-layout.tsx
│   ├── platform-selector.tsx  # Platform selection component
│   └── protected-route.tsx    # Auth protection wrapper
├── contexts/
│   └── AuthContext.tsx    # Authentication context
├── lib/
│   ├── api.ts             # API client and types
│   └── utils.ts           # Utility functions
└── package.json
```

## Features

### Pages

1. **Landing Page** (`/`)
   - Beautiful animated background with BackgroundPaths component
   - Call-to-action buttons to login or view demo

2. **Login Page** (`/login`)
   - User authentication
   - Currently uses demo authentication (any username/password works)

3. **Dashboard** (`/dashboard`)
   - List of all posts
   - Quick actions to create new posts
   - Post cards with content type indicators

4. **Create Post** (`/posts/create`)
   - Content type selection (TEXT, PHOTO, VIDEO)
   - Media upload (image/video)
   - Caption and hashtags input
   - Platform selector with availability checking
   - Real-time platform availability based on content type

5. **Post Details** (`/posts/[id]`)
   - View post details
   - See publishing targets and their status
   - Publish post to selected platforms

6. **Settings** (`/settings`)
   - Manage social media connections
   - View connection status
   - Connect/disconnect accounts

### Components

- **PlatformSelector**: Displays available platforms with account selection
- **BackgroundPaths**: Animated background component used across pages
- **ProtectedRoute**: Wrapper for authenticated routes
- **Navbar**: Navigation bar with user info and logout

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment Variables

Create a `.env.local` file (or copy from `.env.example`):

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start Django Backend

In a separate terminal, start the Django development server:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

The Django API will be available at `http://localhost:8000`

### 4. Start Next.js Frontend

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Backend Integration

### API Endpoints Used

The frontend connects to these Django REST API endpoints:

- `GET /capabilities?content_type={TEXT|PHOTO|VIDEO}` - Get platform availability
- `POST /capabilities/validate` - Validate post draft
- `GET /posts` - List all posts
- `GET /posts/{id}` - Get post details
- `POST /posts` - Create new post
- `PATCH /posts/{id}` - Update post
- `DELETE /posts/{id}` - Delete post
- `POST /posts/{id}/publish` - Publish post to platforms

### Authentication

Currently, the frontend uses a simplified authentication system for demo purposes. In production, you should:

1. Implement proper Django session authentication
2. Add CSRF token handling
3. Implement token-based authentication (JWT) if preferred

To enable proper authentication:

1. Update `lib/api.ts` to include CSRF token handling
2. Update `contexts/AuthContext.tsx` to use real API endpoints
3. Add authentication endpoints to Django if needed

### CORS Configuration

The Django backend is configured with CORS headers to allow requests from `http://localhost:3000`. This is set in `postautomation/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

For production, update this to your frontend domain.

## Platform Availability System

The frontend integrates with the backend's platform availability system:

- When creating a post, the frontend calls `/capabilities?content_type={type}` to get available platforms
- Platforms that don't support the selected content type are shown as unavailable
- Accounts that don't meet requirements (e.g., Instagram Professional account) are disabled
- Action hints are displayed to guide users on how to enable unavailable platforms

## Styling

The project uses:
- **Tailwind CSS** for utility-first styling
- **shadcn/ui** components for consistent UI
- **Framer Motion** for animations
- **Dark mode** support via CSS variables

## Development

### Adding New Pages

1. Create a new file in `app/[page-name]/page.tsx`
2. Use `AppLayout` for consistent layout
3. Use `ProtectedRoute` for authenticated pages
4. Add navigation link in `components/layout/navbar.tsx`

### Adding New Components

1. UI components go in `components/ui/`
2. Feature components go in `components/`
3. Use shadcn/ui CLI to add new components: `npx shadcn-ui@latest add [component]`

### API Integration

All API calls are centralized in `lib/api.ts`. To add new endpoints:

1. Add the endpoint function to the appropriate API object
2. Add TypeScript types if needed
3. Use the function in your components

## Troubleshooting

### CORS Errors

If you see CORS errors:
1. Ensure Django CORS middleware is installed: `pip install django-cors-headers`
2. Check `CORS_ALLOWED_ORIGINS` in Django settings
3. Verify the frontend URL matches the allowed origins

### Authentication Issues

1. Check browser console for errors
2. Verify API base URL in `.env.local`
3. Ensure Django server is running
4. Check network tab for API request/response

### Platform Availability Not Loading

1. Verify `/capabilities` endpoint is working in Django
2. Check browser console for errors
3. Ensure user is authenticated
4. Verify content_type parameter is correct (TEXT, PHOTO, or VIDEO)

## Production Deployment

### Frontend

1. Build the Next.js app: `npm run build`
2. Deploy to Vercel, Netlify, or your preferred hosting
3. Update `NEXT_PUBLIC_API_URL` to production API URL

### Backend

1. Update `ALLOWED_HOSTS` in Django settings
2. Update `CORS_ALLOWED_ORIGINS` with production frontend URL
3. Set up proper authentication
4. Configure static/media file serving
5. Use a production WSGI server (Gunicorn, uWSGI)

## Next Steps

1. **Implement Real Authentication**: Replace demo auth with Django session/token auth
2. **Add Error Handling**: Improve error messages and handling
3. **Add Loading States**: Better loading indicators
4. **Add Form Validation**: Client-side validation for better UX
5. **Add Image Preview**: Preview uploaded images before submission
6. **Add Post Scheduling**: Schedule posts for future publishing
7. **Add Analytics**: Track post performance

