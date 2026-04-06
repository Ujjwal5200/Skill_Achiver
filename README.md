# Skill Achiver - AI-Powered Skill Assessment Platform

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.0.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.10%2B-green" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.115.0-orange" alt="FastAPI">
  <img src="https://img.shields.io/badge/LLM-Groq-purple" alt="Groq">
  <a href="https://github.com/ujjwalkaushik/Skill_Achiver/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow" alt="License"></a>
</p>

> A production-ready AI-powered skill assessment platform that generates challenging technical exams using LLM technology.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Supported Skills](#supported-skills)
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Quiz Structure](#quiz-structure)
- [Environment Variables](#environment-variables)
- [Security Considerations](#security-considerations)
- [License](#license)

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
│   │ name, ID, │  ──→  │ 20 custom  │  ──→  │ 20 timed   │          │
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

### Prerequisites

- Python 3.10+
- Groq API Key ([get from console.groq.com](https://console.groq.com))

### Installation

```bash
# Clone the repository
git clone https://github.com/ujjwalkaushik/Skill_Achiver.git
cd Skill_Achiver

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_api_key_here
```

### Running

```bash
# Start the server
python main.py
```

Access the web interface at: **http://localhost:8001/app**

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

| Attribute | Value |
|-----------|-------|
| Total Questions | 20 |
| Time Limit | 60 minutes |
| Difficulty | Progressive (Basic → Advanced → Expert) |
| Pass Rate Target | 5-10% (designed to identify top talent) |

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes | Your Groq API key |

---

## Security Considerations

> ⚠️ **Important**: The following settings are suitable for development/testing only. Before deploying to production, address these items:

- **CORS**: Currently allows all origins - restrict to your domain(s)
- **Storage**: In-memory only - use Redis/PostgreSQL for persistence
- **Rate Limiting**: Not implemented - add per-endpoint rate limits
- **Authentication**: Not implemented - implement user auth system

---

## License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Built with <a href="https://fastapi.tiangolo.com">FastAPI</a> + <a href="https://groqcloud.com">Groq LLM</a>
</p>