# AI-Ready Todo App - Frontend

This is the frontend of the AI-Ready Full-Stack Todo App, built with Next.js 16+, TypeScript, and Tailwind CSS.

## Tech Stack

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth (JWT-enabled)
- **UI Components**: Custom components following the design system

## Features

- User authentication (login/signup)
- Task management (CRUD operations)
- Priority levels (High/Medium/Low)
- Tagging system
- Due dates and reminders
- Recurring tasks
- Search, filter, and sort functionality
- Responsive design (mobile-first)

## Prerequisites

- Node.js 18+ (recommended)
- npm or yarn package manager

## Installation & Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd agentic-todo-system/phase-2/frontend
```

### 2. Install dependencies

```bash
npm install
# or
yarn install
```

### 3. Environment Configuration

Create a `.env.local` file in the frontend root directory with the following content:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-here
NEXTAUTH_URL=http://localhost:3000
```

**Note**: The `BETTER_AUTH_SECRET` should match the one used in the backend for JWT validation.

### 4. Run the development server

```bash
npm run dev
# or
yarn dev
```

The frontend will be available at [http://localhost:3000](http://localhost:3000)

### 5. Build for production

```bash
npm run build
npm start
# or
yarn build
yarn start
```

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── auth/             # Authentication pages (login, register)
│   ├── dashboard/        # Dashboard page
│   ├── layout.tsx        # Root layout
│   └── page.tsx          # Homepage
├── components/           # Reusable UI components
│   └── auth/            # Authentication-related components
├── lib/                 # Utilities and API clients
│   ├── api/             # API client and functions
│   ├── contexts/        # React Context providers
│   └── types/           # TypeScript type definitions
├── styles/              # Global styles
└── public/              # Static assets
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter

## API Integration

The frontend communicates with the backend API using the following endpoints:

- Authentication: `/api/v1/login`, `/api/v1/register`
- Tasks: `/api/{user_id}/tasks` (following constitution API contract)

JWT tokens are automatically included in requests after successful authentication.

## Authentication Flow

1. User visits the homepage
2. If not authenticated, redirected to `/auth/login`
3. User can sign up at `/auth/register` or log in
4. After successful authentication, redirected to `/dashboard`
5. JWT token is stored in localStorage and included in API requests

## Design System

The UI follows the design system specified in the constitution:

- **Colors**: Primary: #4F46E5, Secondary: #22C55E, Danger: #EF4444, etc.
- **Typography**: Inter (headings & body), JetBrains Mono (monospace)
- **Border Radius**: Cards: 16px, Buttons: 12px, Inputs: 10px

## Email Verification Process

After registration, users will see the message "Email not verified. Check your inbox." This indicates that:

1. The user account has been created successfully
2. A verification email has been sent to the provided email address
3. The user needs to verify their email before full account activation

**Important**: The email verification system requires proper backend configuration with valid Gmail SMTP settings. If users don't receive verification emails, check that the backend has the correct `SENDER_EMAIL` and `GMAIL_APP_PASSWORD` configured.

## Troubleshooting

- If you get CORS errors, ensure the backend is running and the `NEXT_PUBLIC_API_BASE_URL` is correctly set
- For authentication issues, verify that the `BETTER_AUTH_SECRET` matches between frontend and backend
- If components don't render properly, check browser console for TypeScript errors
- If users see "Email not verified. Check your inbox." but don't receive emails, verify the backend email configuration
- Check spam/junk folders if verification emails are not received

## Learn More

To learn more about the technologies used:

- [Next.js Documentation](https://nextjs.org/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)