# PRD: BBCS-Hackathon

## Overview
A React web application built during the BBCS (Building Bridges through Computing and Society) Hackathon. The `meal_share` subfolder contains the hackathon project — a meal-sharing platform that connects people who have excess food with those who need it. Built under hackathon time constraints with Create React App.

## Goals
- Connect food donors with recipients in the same area
- Allow donors to post available meals with description, quantity, pickup time
- Allow recipients to browse and claim available meals
- Simple, fast UI buildable in a hackathon timeframe

## Non-Goals
- Production-grade security or auth system
- Payment processing
- Delivery logistics
- Mobile native app

## User Stories
- As someone with excess food, I want to quickly post it so others can claim it.
- As someone in need, I want to browse nearby available meals and claim one.
- As an organizer, I want to facilitate community food sharing during the hackathon demo.

## Tech Stack
- **Language**: JavaScript / React
- **Build**: Create React App (CRA)
- **Libraries**: React (18+)
- **Backend**: (likely local/mock or minimal backend for hackathon)

## Architecture
```
BBCS-Hackathon/
├── meal_share/          # Main hackathon project (React CRA)
│   ├── src/             # React components
│   ├── public/
│   └── package.json
└── backup(plsdontdelete)/  # Dev backup during hackathon
```

## Deployment / Run
```bash
cd meal_share
npm install
npm start
```

## Constraints & Notes
- **Hackathon project**: built under time pressure (~24-48 hours); expect rough edges
- **CRA boilerplate**: README shows only CRA default template — project-specific docs not added
- **No backend**: may use localStorage or mock data for hackathon demo
- **BBCS context**: hackathon focused on social impact computing projects
