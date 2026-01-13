# Reddit Political Analysis Dashboard

A frontend showcase application that analyzes and visualizes political discourse on Reddit across multiple subreddits. Built with **Next.js 15** and **shadcn/ui** components.

> **Assignment Project**: This project was created as part of a technical assignment for **Simpl**, demonstrating skills in data visualization, modern frontend development, and API integration.

🔗 **Live Demo**: [https://simppl-assignment.vercel.app/](https://simppl-assignment.vercel.app/)

## Features

### Analytics Dashboard
- **Subreddit Comparison**: Visualize posts, comments, and upvotes across political subreddits
- **Interactive Charts**: Bar charts, pie charts, and line graphs using Recharts
- **Trend Analysis**: Track keyword trends over time
- **Misleading Content Detection**: Identify potentially misleading posts based on metrics
- **Customizable Views**: Filter and sort data by various metrics

### AI Chat Interface
- Natural language queries about Reddit political discourse
- Powered by Google Generative AI (Gemini)
- Real-time responses with chat history
- Clean, modern chat UI with message timestamps

### Subreddit Explorer
- Browse posts from 10+ political subreddits:
  - r/Anarchism
  - r/Conservative
  - r/Liberal
  - r/PoliticalDiscussion
  - r/Republican
  - r/Democrats
  - r/Neoliberal
  - r/Politics
  - r/Socialism
  - r/WorldPolitics
- Sort by: Hot, Top, New, Rising
- Real-time Reddit data integration
- Post details: scores, comments, timestamps
- Direct links to original Reddit posts

### Story Page
Interactive narrative exploring Reddit's political landscape from July 2024 to February 2025, featuring:
- Key figures and themes analysis
- Information sources and trust patterns
- Community dynamics
- Linguistic patterns
- Visual data storytelling with charts and images

## Tech Stack

### Frontend
- **Framework**: Next.js 15 (App Router)
- **UI Library**: React 19
- **Styling**: Tailwind CSS
- **Component Library**: shadcn/ui (Radix UI primitives)
- **Charts**: Recharts
- **Theme**: next-themes (dark/light mode)
- **Forms**: React Hook Form + Zod validation
- **Icons**: Lucide React
- **Date Utilities**: date-fns

### Backend
- Built with **FastAPI** (deployed separately, not included in this repository)
- Data processing with Pandas, scikit-learn, NLTK
- AI integration with Google Generative AI (Gemini)
- Reddit data fetched via PRAW

> **Note**: The backend is privately deployed and not included in this repository. This showcase focuses on the frontend implementation.

### Development Tools
- **TypeScript**: Type safety
- **Package Manager**: pnpm
- **Linting**: ESLint
- **Deployment**: Vercel (Frontend)

## Prerequisites

- **Node.js**: 18.x or higher
- **pnpm**: Latest version (or npm/yarn)

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd nextjs-shadcn-fastapi
```

### 2. Install Dependencies
```bash
pnpm install
# or
npm install
```

### 3. Environment Setup
> **Note**: This project connects to a privately deployed backend. The live demo at [simppl-assignment.vercel.app](https://simppl-assignment.vercel.app/) is fully functional.

To run locally, you would need to set up your own backend or contact the repository owner.

## 💻 Development

### Run Development Server
```bash
pnpm dev
# or
npm run dev
```

The app will be available at `http://localhost:3000` and will connect to the production backend at `https://simppl-backend.onrender.com`.

## 🏗️ Build & Deployment
.

> **Note**: The backend is privately deployed and not publicly accessible for local development
### Build for Production
```bash
pnpm build
# or
npm run build
```

### Start Production Server Locally
```bash
pnpm start
# or
npm start
```

### DeploymentPrivately deployed (not publicly accessible
- **Frontend**: Deployed on Vercel at [https://simppl-assignment.vercel.app/](https://simppl-assignment.vercel.app/)
- **Backend**: Deployed on Render at [https://simppl-backend.onrender.com](https://simppl-backend.onrender.com)

## 📁 Project Structure

```
nextjs-shadcn-fastapi/
├── app/                      # Next.js App Router
│   ├── globals.css          # Global styles
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Analytics dashboard (home)
│   ├── chat/
│   │   └── page.tsx         # AI chat interface
│   ├── story/
│   │   └── page.tsx         # Data story & narrative
│   └── subreddits/
│       └── page.tsx         # Subreddit explorer
├── components/
│   ├── navbar.tsx           # Navigation component
│   ├── theme-provider.tsx   # Dark/light theme
│   └── ui/                  # shadcn/ui components (40+)
├── hooks/                    # Custom React hooks
├── lib/
│   └── utils.ts             # Utility functions
├── public/                  # Static assets & images
├── package.json             # Node dependencies & scripts
├── tailwind.config.ts       # Tailwind configuration
├── tsconfig.json            # TypeScript configuration
└── next.config.mjs          # Next.js configuration
```

> **Note**: Backend code is maintained separately and not included in this repository.

## 🎨 Features Deep Dive

### Analytics Dashboard
The main dashboard (`/`) provides:
- **Subreddit Statistics**: Posts, comments, and upvotes comparison
- **Monthly Trends**: Track keyword mentions over time
- **Misleading Content**: Identify posts with suspicious engagement patterns
- **Interactive Filters**: Customize time ranges and data views

### AI Chat
Navigate to `/chat` to:
- Ask questions about Reddit political discourse
- Get AI-generated insights from the dataset
- Explore patterns and trends through conversation

### Subreddit Browser
Visit `/subreddits` to:
- Select from 10 political subreddits
- Choose sorting method (Hot, Top, New, Rising)
- Browse posts with rich metadata
- Access original Reddit posts directly

### Story Narrative
The `/story` page presents:
- Visual data storytelling
- Analysis of key political figures (Trump, Musk)
- Source credibility patterns
- Community behavior insights
- Interactive visualizations

## 🔑 Key Technologies

### shadcn/ui Components Used
- Cards, Buttons, Inputs, Selects
- Accordions, Alerts, Badges
- Dialogs, Dropdowns, Popovers
- Tabs, Tables, Tooltips
- Charts, Carousels, Progress bars
- Forms with validation
- And 40+ more components

### Recharts Visualizations
- Bar Charts
- Pie Charts
- Line Graphs
- Responsive containers
- Custom tooltips and legends

## 🌐 API Architecture

The frontend connects to a FastAPI backend that provides:
- AI-powered chat responses using Google Generative AI
- Real-time Reddit data via PRAW
- Processed analytics and visualization data

> **Note**: Backend API is privately deployed and not publicly documented.

## 🎯 About This Project

This was created as a **technical assignment for Simpl** to demonstrate:

1. **Full-Stack Integration**: Frontend consuming external REST API
2. **Data Visualization**: Complex charts and interactive dashboards
3. **Modern UI/UX**: shadcn/ui component library implementation
4. **Real-time Data**: Reddit API integration for live posts
5. **AI Integration**: Chat interface with Google Generative AI
6. **Responsive Design**: Mobile-first approach with Tailwind CSS
7. **TypeScript**: Type-safe React application

### Use Cases
- Political discourse pattern analysis across ideological spectrums
- Trend tracking of political topics over time
- Sentiment analysis of political discussions
- Potentially misleading content identification
- Community behavior study across different political groups

## 🔒 Data Privacy

- No user data is stored permanently
- Chat histories are session-based
- Reddit data is fetched in real-time or from processed datasets
- API keys should be kept secure in `.env.local`

## 📝 License

This project was created as an assignment submission and is for demonstration purposes only.

## 🐛 Troubleshooting

### Common Issues

**Port 3000 already in use**
```bash
# Kill the process using port 3000
# On Windows PowerShell:
Stop-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess -Force

# Or change port in package.json
```

**Module not found errors**
```bash
# Reinstall dependencies
rm -rf node_modules
pnpm install
```

**Build errors**
```bash
# Clear Next.js cache
rm -rf .next
pnpm build
```

**API connection issues**
- The live demo should work seamlessly
- For local development, backend access is required (not publicly available)
- Check browser console for network errors

**Theme not working**
- Ensure `theme-provider.tsx` is properly imported in `layout.tsx`
- Check browser localStorage for theme preference

## 🎓 Learning Outcomes

This project demonstrates proficiency in:
- ✅ Next.js 15 App Router
- ✅ React 19 with TypeScript
- ✅ Modern CSS with Tailwind
- ✅ Component library integration (shadcn/ui)
- ✅ Data visualization with Recharts
- ✅ API integration and error handling
- ✅ Responsive design patterns
- ✅ Dark/light theme implementation
- ✅ Production deployment on Vercel

## 📧 Contact

For questions or feedback about this project, please open an issue in the repository.

## 🙏 Acknowledgments

- [shadcn/ui](https://ui.shadcn.com/) for the exceptional component library
- [Vercel](https://vercel.com/) for frontend hosting
- [Render](https://render.com/) for backend hosting
- Reddit API for data access
- Google Generative AI for chat capabilities
- The open-source community for all the amazing tools

---
**Simpl** for the assignment opportunity
- [shadcn/ui](https://ui.shadcn.com/) for the exceptional component library
- [Vercel](https://vercel.com/) for hosting
- Reddit for data access
- Google Generative AI for chat capabilities
- The open-source community

---

**Built with ❤️ using Next.js 15, TypeScript, and shadcn/ui**  
*Assignment project for Simpl - Showcasing modern web development and data visualization