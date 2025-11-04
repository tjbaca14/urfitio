# UrFit.io Client

Next.js frontend for the UrFit.io chat application.

## Getting Started

### Prerequisites

- Node.js 20.9.0 or higher (you're currently on 18.20.8 - consider upgrading)
- npm

### Installation

1. Install dependencies:

```bash
npm install
```

2. Set up environment variables:

```bash
cp .env.example .env.local
```

Edit `.env.local` to point to your backend API:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### Development

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Building for Production

```bash
npm run build
npm start
```

## Architecture

### State Management

- **React Query** (`@tanstack/react-query`): Server state management
  - Chat history
  - Divisions and schools data
  - Automatic caching and refetching

- **Zustand** (`zustand`): Client-side UI state
  - Current input text
  - Streaming status
  - Selected division/school
  - Local storage persistence

### API Layer

The API client is located in `lib/api/`:
- `client.ts`: API methods for chat and coach endpoints
- `types.ts`: TypeScript types matching backend models

### Components

- `components/Chat.tsx`: Main chat interface with:
  - Message history display
  - Context selection (division/school)
  - Streaming response support
  - Auto-scrolling

### Hooks

Custom hooks in `hooks/`:
- `useChat.ts`: React Query hooks for data fetching
- `useStreamingChat.ts`: Streaming chat responses

## Features

- Real-time chat with AI
- Context-aware responses based on selected coach
- Message persistence
- Optimistic UI updates
- Streaming responses support
- Responsive design with Tailwind CSS

## Environment Variables

- `NEXT_PUBLIC_API_URL`: Backend API URL (required)

## Tech Stack

- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Query + Zustand
- **HTTP Client**: Axios

## Project Structure

```
client/
├── app/
│   ├── layout.tsx         # Root layout with providers
│   ├── page.tsx           # Home page (Chat component)
│   └── providers.tsx      # React Query provider setup
├── components/
│   └── Chat.tsx           # Main chat UI component
├── hooks/
│   ├── useChat.ts         # Data fetching hooks
│   └── useStreamingChat.ts # Streaming chat hook
├── lib/
│   └── api/
│       ├── client.ts      # API client methods
│       ├── types.ts       # TypeScript types
│       └── index.ts       # Exports
└── stores/
    └── useChatStore.ts    # Zustand store for UI state
```

## Connecting to Backend

Make sure your FastAPI backend is running on `http://localhost:8000` before starting the client.

From the root directory, start the backend:

```bash
# In one terminal
uvicorn app.main:app --reload
```

Then start the client:

```bash
# In another terminal
cd client
npm run dev
```