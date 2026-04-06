# Skill Achiver - AI-Powered Skill Assessment Platform

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=ujjwalkaushik&repo=Skill_Achiver&label=Views&color=00f0ff&style=flat-square" alt="Views">
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
- [Live Demo](#-live-demo)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Interactive Architecture](#-interactive-architecture)
- [Supported Skills](#supported-skills)
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Quiz Structure](#quiz-structure)
- [Environment Variables](#environment-variables)
- [Security Considerations](#security-considerations)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Skill Achiver is an intelligent assessment platform designed to evaluate technical skills through AI-generated questions. It helps organizations:

- **Automate exam creation** - AI generates relevant questions based on skills and experience level
- **Standardize assessments** - Consistent, high-quality questions for all candidates
- **Save recruiter time** - No manual question bank maintenance needed
- **Identify top talent** - Challenging questions designed to distinguish skilled candidates

---

## 🔴 Live Demo

<p align="center">
<a href="http://localhost:8001/app">
  <img src="https://img.shields.io/badge/Try_Demo-Live_Now-10b981?style=for-the-badge&logo=rocket&logoColor=white">
</a>
</p>

<p align="center">
  <em>Click above to launch the interactive assessment platform</em>
</p>

---

## Key Features

| Feature | Description | Status |
|---------|-------------|--------|
| **AI-Powered Generation** | Creates custom questions using LLM technology | ✅ Active |
| **50+ Skills Supported** | AWS, Azure, Python, JavaScript, React, Docker, and more | ✅ Active |
| **Real-time Streaming** | Questions appear as they're generated | ✅ Active |
| **Timed Sections** | Structured quiz with time management | ✅ Active |
| **Instant Results** | Immediate scoring and detailed feedback | ✅ Active |
| **Attempt Tracking** | Prevents repeated attempts per skill | ✅ Active |

---

## How It Works

```mermaid
graph LR
    A[User Registration] --> B[Skill Selection]
    B --> C[AI Question Generation]
    C --> D[Timed Quiz Assessment]
    D --> E[Instant Results]
    
    style A fill:#00f0ff,color:#0a0e27
    style B fill:#a855f7,color:#fff
    style C fill:#00f0ff,color:#0a0e27
    style D fill:#a855f7,color:#fff
    style E fill:#10b981,color:#fff
```

### Step-by-Step Flow

| Step | Process | Description |
|------|---------|-------------|
| **1️⃣** | Register | Enter name, ID, skill, and experience level |
| **2️⃣** | Generate | AI creates 20 custom questions via Groq LLM |
| **3️⃣** | Take Quiz | Answer questions with timed sections |
| **4️⃣** | Results | View score, breakdown, and performance report |

---

## 🔧 Interactive Architecture

```mermaid
flowchart TB
    subgraph Client["🌐 Frontend (app.html)"]
        UI[User Interface]
        GS[Game State]
    end
    
    subgraph API["⚡ FastAPI Backend"]
        GE[Assignment Engine]
        GR[Groq API]
        DB[(In-Memory DB)]
    end
    
    UI -->|HTTP Requests| GE
    GE -->|API Calls| GR
    GE -->|Store Data| DB
    
    style Client fill:#131842,color:#00f0ff
    style API fill:#1a1f3c,color:#a855f7
    style GR fill:#2d1f4e,color:#fff
    style DB fill:#0f172a,color:#10b981
```

### Data Flow

```mermaid
sequenceDiagram
    participant User
    participant API as FastAPI
    participant LLM as Groq LLM
    participant DB as In-Memory Store
    
    User->>API: POST /register-attempt
    API->>DB: Check attempts
    DB-->>API: Attempts remaining
    API-->>User: Registration confirmed
    
    User->>API: POST /generate-assignment
    API->>LLM: Send prompt with skill/level
    LLM-->>API: Stream questions (SSE)
    API-->>User: Real-time question delivery
    
    User->>API: Submit answers
    API->>DB: Calculate score
    DB-->>API: Result data
    API-->>User: Final score & breakdown
```

---

## Supported Skills

<details>
<summary><b>Click to expand skill categories</b></summary>

### ☁️ Cloud Platforms
| AWS | Azure | GCP |
|-----|-------|-----|
| AWS EC2 | Azure VM | GCP Compute |
| AWS S3 | Azure Storage | BigQuery |
| AWS Lambda | Azure Functions | Cloud Functions |
| AWS DynamoDB | Azure Cosmos DB | Firestore |

### 💻 Programming Languages
<div style="display:flex;gap:10px;flex-wrap:wrap;">
<img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black">
<img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white">
<img src="https://img.shields.io/badge/Java-ED8B00?style=flat&logo=java&logoColor=white">
<img src="https://img.shields.io/badge/Go-00ADD8?style=flat&logo=go&logoColor=white">
<img src="https://img.shields.io/badge/Rust-DEA584?style=flat&logo=rust&logoColor=white">
<img src="https://img.shields.io/badge/C%2B%2B-00599C?style=flat&logo=c%2B%2B&logoColor=white">
</div>

### 🎨 Frontend Frameworks
<div style="display:flex;gap:10px;flex-wrap:wrap;">
<img src="https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black">
<img src="https://img.shields.io/badge/Vue.js-4FC08D?style=flat&logo=vuedotjs&logoColor=white">
<img src="https://img.shields.io/badge/Angular-DD0031?style=flat&logo=angular&logoColor=white">
<img src="https://img.shields.io/badge/Next.js-000000?style=flat&logo=nextdotjs&logoColor=white">
</div>

### ⚙️ Backend Frameworks
| Django | FastAPI | Express | Spring | Rails |
|--------|---------|---------|--------|-------|
| Python | Python | Node.js | Java | Ruby |

### 🐳 DevOps Tools
<div style="display:flex;gap:10px;flex-wrap:wrap;">
<img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white">
<img src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat&logo=kubernetes&logoColor=white">
<img src="https://img.shields.io/badge/Terraform-7B42BC?style=flat&logo=terraform&logoColor=white">
<img src="https://img.shields.io/badge/Jenkins-D24939?style=flat&logo=jenkins&logoColor=white">
<img src="https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white">
</div>

### 📊 Data & ML
| SQL | NoSQL | Data Science | Machine Learning | Deep Learning |
|-----|-------|--------------|------------------|---------------|
| PostgreSQL | MongoDB | Pandas | TensorFlow | PyTorch |
| MySQL | Redis | NumPy | Keras | Hugging Face |

### 🔐 Security
<div style="display:flex;gap:10px;flex-wrap:wrap;">
<img src="https://img.shields.io/badge/Cybersecurity-FF6B6B?style=flat">
<img src="https://img.shields.io/badge/Penetration_Testing-4ECDC4?style=flat">
<img src="https://img.shields.io/badge/Cloud_Security-45B7D1?style=flat">
</div>

</details>

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

### Interactive API Docs

<p align="center">
<a href="http://localhost:8001/docs">
  <img src="https://img.shields.io/badge/OpenAPI_Swagger-6DB33F?style=for-the-badge&logo=swagger">
</a>
</p>

| Method | Endpoint | Description | Try it |
|--------|----------|-------------|--------|
| GET | `/app` | Web interface | [Launch](http://localhost:8001/app) |
| GET | `/api/health` | Health check | [Check](http://localhost:8001/api/health) |
| POST | `/generate-assignment` | Generate quiz questions | 📋 See below |
| POST | `/api/check-attempts` | Check remaining attempts | 📋 See below |
| POST | `/api/register-attempt` | Register new attempt | 📋 See below |
| POST | `/api/submit-result` | Submit quiz results | 📋 See below |
| GET | `/api/results/{id}` | Get student results | 📋 See below |

### Example Request

```bash
curl -X POST "http://localhost:8001/generate-assignment" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "1234",
    "student_name": "John Doe",
    "skills": ["Python"],
    "exp_level": "3 years",
    "subject": "Python"
  }'
```

---

## Quiz Structure

| Attribute | Value | Visual |
|-----------|-------|--------|
| Total Questions | 20 | █████████████████████ |
| Time Limit | 60 minutes | ⏱️ 60:00 |
| Difficulty | Progressive | Basic → Advanced → Expert |
| Pass Rate Target | 5-10% | 🎯 Elite |

---

## Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `GROQ_API_KEY` | Yes | Your Groq API key | None |

---

## Security Considerations

> ⚠️ **Important**: The following settings are suitable for development/testing only. Before deploying to production, address these items:

- **CORS**: Currently allows all origins - restrict to your domain(s)
- **Storage**: In-memory only - use Redis/PostgreSQL for persistence
- **Rate Limiting**: Not implemented - add per-endpoint rate limits
- **Authentication**: Not implemented - implement user auth system

---

## Contributing

<p align="center">
<a href="https://github.com/ujjwalkaushik/Skill_Achiver/issues">
  <img src="https://img.shields.io/badge/Issues-Welcome-10b981?style=for-the-badge">
</a>
<a href="https://github.com/ujjwalkaushik/Skill_Achiver/pulls">
  <img src="https://img.shields.io/badge/PRs-Welcome-a855f7?style=for-the-badge">
</a>
</p>

Contributions are welcome! Please feel free to submit a Pull Request.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Built with <a href="https://fastapi.tiangolo.com">FastAPI</a> + <a href="https://groqcloud.com">Groq LLM</a>
</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=0,2,11&height=100&section=footer">
</p>
