# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is the **OPCVM Investment Simulator** - a full-stack application for modeling long-term outcomes of recurring investments into Moroccan funds. The project consists of:

1. **Python Backend** (`py-opcvm-simulator/`) - Core simulation engine with deterministic and Monte Carlo modeling
2. **Next.js Frontend** (`next-opcvm-visualizer/`) - Modern React web interface with Tailwind CSS and shadcn/ui

## Architecture

### Backend (Python)
- **Core Engine**: `opcvm_simulator.py` - Contains simulation algorithms, fund data, and risk metrics
- **Web API**: `server.py` - FastAPI server exposing simulation endpoints
- **Fund Data**: Hardcoded Moroccan OPCVM fund data with returns, categories, and tax rates
- **Simulation Types**:
  - Deterministic CAGR projection with fees and taxes
  - Monte Carlo simulation using Geometric Brownian Motion (GBM)

### Frontend (Next.js)
- **Framework**: Next.js 15+ with App Router
- **Styling**: Tailwind CSS v4 with shadcn/ui components
- **Charting**: Recharts for investment trajectory visualization
- **State**: React hooks for form management and API integration
- **Key Components**: Located in `src/components/ui/` following shadcn/ui patterns

### Data Flow
1. User inputs investment parameters via React interface
2. Frontend calls `/api/simulate` endpoint
3. Python backend processes simulation with fund data and returns results
4. Frontend visualizes trajectory and metrics using charts

## Common Commands

### Python Backend
```bash
# Development server (from py-opcvm-simulator/)
uvicorn server:app --reload --port 8000

# Run tests
python simulator.test.py

# Interactive simulation
python opcvm_simulator.py
```

### Next.js Frontend
```bash
# Development server (from next-opcvm-visualizer/)
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev

# Production build
npm run build
npm run start

# Linting
npm run lint
```

### Full Stack Development
```bash
# Terminal 1: Start Python API
cd py-opcvm-simulator && uvicorn server:app --reload --port 8000

# Terminal 2: Start Next.js frontend
cd next-opcvm-visualizer && npm run dev
```

## Key Files and Directories

### Backend Structure
- `opcvm_simulator.py` - Main simulation engine with fund data and algorithms
- `server.py` - FastAPI web server with `/simulate` endpoint
- `simulator.test.py` - Example usage and testing
- `opcvm_simulator.old.py` - Contains `summarize()` utility function

### Frontend Structure
- `src/app/page.tsx` - Main simulation interface with form controls
- `src/app/layout.tsx` - App layout and font configuration
- `src/components/ui/` - shadcn/ui component library
- `src/lib/utils.ts` - Utility functions (Tailwind class merging)

### Configuration Files
- `tsconfig.json` - TypeScript configuration with path aliases
- `package.json` - Dependencies including Recharts, Radix UI, Lucide icons
- `eslint.config.mjs` - ESLint configuration for Next.js
- `next.config.ts` - Next.js configuration

## Development Notes

### Fund Data
The simulator includes real Moroccan OPCVM fund data from Wafa Gestion (Aug 2025) with:
- Historical cumulative returns over specific horizons
- Fund categories (Actions, Diversifié, Obligations, Taux, Monétaire, Trésorerie)  
- Default tax rates and volatility estimates per category

### API Integration
The Next.js frontend expects to call `/api/simulate` but this endpoint needs to be proxied to the Python backend running on port 8000. Consider adding Next.js API routes or proxy configuration.

### Component Library
Uses shadcn/ui components built on Radix UI primitives with Tailwind CSS. Components follow the pattern:
- Variants defined with `class-variance-authority`
- Accessible by default via Radix UI
- Customized styling with Tailwind

### Simulation Features
- **Deterministic**: CAGR-based projections with monthly compounding, fees, and end-of-horizon taxation
- **Monte Carlo**: GBM-based stochastic modeling with risk metrics (Sharpe, Sortino, Max Drawdown, VaR)
- **Tax Modeling**: Morocco-specific capital gains tax by fund category
- **Fee Structure**: Annual management fees applied monthly

## Testing

### Backend Testing
Run `python simulator.test.py` to verify core simulation functionality with sample data.

### Frontend Testing
No specific test setup currently configured. Consider adding Jest/React Testing Library for component testing.

## Deployment Considerations

- Backend requires Python with FastAPI, NumPy dependencies
- Frontend builds to static files, can be deployed on Vercel/Netlify
- API and frontend need proper CORS configuration for production
- Environment variables may be needed for API endpoint configuration
