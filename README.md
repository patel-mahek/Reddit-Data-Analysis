# Reddit Political Analysis Dashboard

A modern web application for analyzing and visualizing political discourse across Reddit communities. 

**Live Demo**: [https://simppl-assignment.vercel.app/](https://simppl-assignment.vercel.app/)

## Features

- **Analytics Dashboard**: Interactive charts visualizing subreddit statistics, trends, and engagement patterns
- **AI Chat Interface**: Natural language queries powered by Google Generative AI
- **Subreddit Explorer**: Browse and filter posts from 10+ political subreddits in real-time
- **Story Page**: Data-driven narrative exploring Reddit's political landscape (July 2024 - February 2025)

## Tech Stack

**Frontend**
- Next.js 15 with App Router
- React 19 + TypeScript
- Tailwind CSS
- shadcn/ui (Radix UI components)
- Recharts for data visualization

**Backend**
- FastAPI with Python
- Google Generative AI (Gemini)
- PRAW for Reddit API integration
- Pandas, scikit-learn, NLTK

## Installation

```bash
# Clone repository
git clone <repository-url>
cd nextjs-shadcn-fastapi

# Install dependencies
npm install
# or
pnpm install

# Run development server
npm run dev
# or
pnpm dev
```

Visit `http://localhost:3000`

## Build

```bash
npm run build
npm start
```

## Project Structure

```
app/
├── page.tsx              # Analytics dashboard
├── chat/page.tsx         # AI chat interface
├── story/page.tsx        # Data narrative
└── subreddits/page.tsx   # Subreddit browser

components/
├── navbar.tsx
├── theme-provider.tsx
└── ui/                   # shadcn/ui components

lib/
└── utils.ts

public/                   # Static assets
```

## Deployment

Deployed on Vercel at [https://simppl-assignment.vercel.app/](https://simppl-assignment.vercel.app/)

---


