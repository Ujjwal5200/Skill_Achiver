# Skill Achiver - AI-Powered Skill Assessment Platform

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.0.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.10%2B-green" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.115.0-orange" alt="FastAPI">
  <img src="https://img.shields.io/badge/LLM-Groq-purple" alt="Groq">
</p>

A production-ready AI-powered skill assessment platform that generates challenging technical exams using LLM technology.

---

## Overview

Skill Achiver is an intelligent assessment platform designed to evaluate technical skills through AI-generated questions. It helps organizations:

- **Automate exam creation** - AI generates relevant questions based on skills and experience level
- **Standardize assessments** - Consistent, high-quality questions for all candidates
- **Save recruiter time** - No manual question bank maintenance needed
- **Identify top talent** - Challenging questions designed to distinguish skilled candidates

---

## Key Features

| Feature | Description |
|---------|-------------|
| **AI-Powered Generation** | Creates custom questions using LLM technology |
| **50+ Skills Supported** | AWS, Azure, Python, JavaScript, React, Docker, and more |
| **Real-time Streaming** | Questions appear as they're generated |
| **Timed Sections** | Structured quiz with time management |
| **Instant Results** | Immediate scoring and detailed feedback |
| **Attempt Tracking** | Prevents repeated attempts per skill |

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    HOW IT WORKS                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   1. REGISTER          2. GENERATE         3. TAKE QUIZ          │
│   ┌───────────┐       ┌───────────┐       ┌───────────┐          │
│   │ Enter     │       │ AI creates │       │ Answer    │          │
│   │ name, ID, │  ──→  │ 20 custom  │  ──→  │ 20 timed  │          │
│   │ skill     │       │ questions  │       │ questions │          │
│   └───────────┘       └───────────┘       └───────────┘          │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│   Validate and        Build prompt        Track score           │
│   check attempts     → Groq LLM →          and progress          │
│                                                                  │
│   4. RESULTS                                                     │
│   ┌───────────┐                                                 │
│   │ View      │                                                 │
│   │ score %,  │  ──→  Detailed breakdown                         │
│   │ answers   │       and performance report                      │
│   └───────────┘                                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Supported Skills

- **Cloud Platforms**: AWS, Azure, GCP
- **Programming**: Python, JavaScript, TypeScript, Java, Go, Rust, PHP, Ruby
- **Frontend**: React, Vue, Angular, Node.js, Django, Flask
- **Backend**: Spring, Django, FastAPI, Express, Rails
- **DevOps**: Docker, Kubernetes, CI/CD, Linux
- **Data**: SQL, NoSQL, Data Science, Machine Learning
- **Security**: Cybersecurity, Penetration Testing

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment variable
# Create .env file and add:
GROQ_API_KEY=your_api_key_here

# Run the server
python main.py

# Open in browser
# http://localhost:8001/app
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/app` | Web interface |
| GET | `/api/health` | Health check |
| POST | `/generate-assignment` | Generate quiz questions |
| POST | `/api/check-attempts` | Check remaining attempts |
| POST | `/api/register-attempt` | Register new attempt |
| POST | `/api/submit-result` | Submit quiz results |
| GET | `/api/results/{id}` | Get student results |

---

## Quiz Structure

- **Total Questions**: 20
- **Time Limit**: 60 minutes
- **Difficulty**: Progressive (Basic → Advanced → Expert)
- **Pass Rate Target**: 5-10% (designed to identify top talent)

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes | Get from [groq.cloud](https://console.groq.com) |

---

## Security Notes

- **CORS**: Currently allows all origins - restrict for production deployment
- **Storage**: In-memory only - use Redis/PostgreSQL for production
- **Rate Limiting**: Not implemented - add for production
- **Authentication**: Not implemented - add for production

---

## License

MIT License

---

<p align="center">Built with FastAPI + Groq LLM</p>