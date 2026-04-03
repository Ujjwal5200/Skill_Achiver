"""
Assignment Generation Engine - Enhanced with Retry Tracking
============================================================
- Adds attempt tracking and result storage
- Integrates with the frontend quiz application
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from groq import AsyncGroq, RateLimitError
from dotenv import load_dotenv
from typing import List, AsyncGenerator, Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import json
import os
import time
import logging
import uuid
from datetime import datetime
from collections import defaultdict
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(
    title="Assignment Generation Engine - Enhanced",
    description="Skill Assessment with Retry Tracking",
    version="4.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

groq_client = AsyncGroq(api_key=GROQ_API_KEY)

# In-memory storage for attempts and results (use database in production)
attempt_storage = defaultdict(list)
result_storage = defaultdict(list)
results_lock = threading.Lock()


class AssignmentRequest(BaseModel):
    student_id: str = Field(..., min_length=1)
    student_name: str = Field(..., min_length=1)
    skills: List[str] = Field(..., min_length=1)
    exp_level: str = Field(..., min_length=3)


class SubmitResultRequest(BaseModel):
    student_id: str
    student_name: str
    skill: str
    answers: dict
    score: int
    total: int
    time_taken: float


class CheckAttemptRequest(BaseModel):
    student_id: str
    skill: str


class AssignmentGenerator:
    
    @staticmethod
    def _build_prompt(skills: List[str], exp_level: str) -> str:
        prompt = f"""You are a PRINCIPAL ENGINEER at FAANG (ex-Google/Amazon) designing the final promotion exam for L7 → L8 level.

This exam is LEGENDARY and BRUTAL — it has a strict 5–10% pass rate. It is specifically designed to separate truly exceptional engineers from confident but shallow seniors. Most candidates who think they are ready will fail.

STUDENT PROFILE:
- Skills: {json.dumps(skills)}
- Experience: {exp_level.replace('_', ' ').title()}

MISSION: Generate **exactly 20 brutally hard MCQs** that test deep production mastery. 
Only engineers with exceptional insight, battle-tested intuition, and the ability to synthesize multiple complex concepts under pressure should pass.

DIFFICULTY RULES (STRICTLY NON-NEGOTIABLE):
1. NO basic syntax, API recall, or "what does this code return?" questions.
2. Every question must force synthesis of **at least 2–4 interconnected concepts** (e.g., distributed locking + consistency models + failure modes + performance under load).
3. The "obvious" or "textbook" answer must be **wrong or dangerously incomplete**. The correct answer should be counter-intuitive yet precisely correct in real production environments.
4. Distractors must be highly plausible — exactly what a strong Senior Engineer (L6/L7) would confidently choose, but with subtle, critical flaws.
5. Explanations must reveal deep, non-obvious production insights (e.g., "This pattern works in low traffic but causes cascading failures at scale" or "This trade-off saves CPU but silently corrupts data during network partitions").

QUESTION TYPES (Balanced & Progressive):
- Q1–10: Advanced Edge-Case & Nuanced Single/Multi-Concept Questions  
  Deep dives into subtle behaviors, race conditions, consistency traps, observability blind spots, etc., tailored to the student's skills. Focus on foundational mastery with high-stakes twists.
- Q11–16: Multi-Concept Traps  
  Combine 3–4 domains (e.g., caching + retry semantics + idempotency + observability + partial failures). Introduce conflicting goals, scale-induced edge cases, and trade-offs that expose shallow understanding.
- Q17–20: The Gauntlet — Hard Production War-Story Case Studies (converted to MCQ)  
  Present a realistic, detailed 6–8 line production incident (outage, silent data issue, performance cliff, etc.) with specific metrics (p99 latency, error rate, throughput, traffic pattern, constraints).  
  Ask for root cause, best mitigation, or optimal trade-off.  
  Make the scenario feel authentic, high-stakes, and drawn from real FAANG war stories. Force evaluation of multiple failure modes and systemic impacts.

ENGAGEMENT & WORTHINESS:
- Questions should be immersive and progressively challenging so students stay fully engaged.
- The overall exam must feel prestigious and valuable — when a student finishes (especially if they pass), they should feel:  
  "I have truly earned this. This proves real mastery and credibility in my skill. Only a few engineers can clear this."

OUTPUT ONLY VALID JSON (nothing else — no markdown, no explanations outside JSON).

JSON Schema:
{{
  "title": "string (e.g. 'L8 Principal Engineer Promotion Exam - {skills} - {exp_level}')",
  "objective": "string (e.g. 'Prove elite-level production systems mastery and battle-tested judgment')",
  "difficulty": "brutal",
  "pass_rate_target": "5-10%",
  "total_questions": 20,
  "mcqs": [
    {{
      "id": int,
      "type": "single" | "multi" | "special",
      "question": "string (for case studies, embed the full realistic scenario inside the question)",
      "options": ["A. ...", "B. ...", "C. ...", "D. ..."] | ["A. ...", "B. ...", "C. ...", "D. ...", "E. ..."],
      "correct": "A. ..." | ["B. ...", "D. ..."] | "A. ..." , "B. ..." , "C. ..." | "None" | "All",
      "explanation": "string (2-3 sentences max: explain why the obvious answer fails in production and why the correct one succeeds)"
    }}
  ]
}}

CRITICAL INSTRUCTION: 
If any question feels even slightly easy, standard, or textbook — reject and make it significantly harder. Add constraints, edge conditions, or conflicting goals. Ensure Q1–10 test foundational concepts with brutal twists, Q11–16 demand multi-concept integration under pressure, and Q17–20 feel like real war stories that would make even a Senior Engineer pause and think deeply. Make questions increasingly hard from Q11 to Q20, 
such that even attempts to cheat via image recognition or search engines fail due to custom, context-specific synthesis requirements. All questions must have different correct answers across options (no repeated patterns). The questions should require deep understanding and synthesis of concepts, not just recall.
Ensure diversity in domains (e.g., mix of systems, data, security, performance) and tailor to student skills for maximum relevance and rigor."""
        return prompt

    @staticmethod
    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(RateLimitError)
    )
    async def generate_stream(request: AssignmentRequest) -> AsyncGenerator[str, None]:
        start_time = time.time()
        prompt = AssignmentGenerator._build_prompt(request.skills, request.exp_level)

        try:
            stream = await groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a technical examiner. Generate ONLY valid JSON. No markdown. No explanations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=6100,
                temperature=0.7,
                top_p=0.95,
                stream=True,
                timeout=60.0
            )

            full_response = ""
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    token = chunk.choices[0].delta.content
                    full_response += token
                    yield json.dumps({"type": "token", "content": token}) + "\n"

            generation_time_ms = int((time.time() - start_time) * 1000)

            try:
                assignment = json.loads(full_response)
                
                input_tokens_est = round(len(prompt) / 3.8 + 140)
                output_tokens_est = round(len(full_response) / 3.8)
                cost_usd = (input_tokens_est * 0.05 + output_tokens_est * 0.08) / 1_000_000
                cost_inr = round(cost_usd * 84.5, 2)

                yield json.dumps({
                    "type": "complete",
                    "assignment": assignment,
                    "cost_inr": cost_inr,
                    "generation_time_ms": generation_time_ms,
                    "estimated_tokens": {"input": input_tokens_est, "output": output_tokens_est},
                    "model": "llama-3.1-8b-instant"
                }) + "\n"

            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error for {request.student_id}: {str(e)}")
                yield json.dumps({
                    "type": "error",
                    "error": f"Invalid JSON: {str(e)}",
                    "raw_output_preview": full_response[:300],
                    "cost_inr": 0.0
                }) + "\n"

        except RateLimitError as e:
            logger.warning(f"Rate limit hit for {request.student_id}, retried")
            yield json.dumps({
                "type": "error",
                "error": "Rate limit exceeded. Retrying...",
                "cost_inr": 0.0
            }) + "\n"
        except Exception as e:
            logger.error(f"Generation failed for {request.student_id}: {str(e)}")
            yield json.dumps({
                "type": "error",
                "error": str(e),
                "cost_inr": 0.0
            }) + "\n"


# ============== ATTEMPT TRACKING ENDPOINTS ==============

MAX_ATTEMPTS = 2


@app.post("/generate-assignment")
async def generate_assignment(request: AssignmentRequest, request_obj: Request):
    """Generate assignment questions from the AI engine."""
    request_id = str(uuid.uuid4())
    logger.info(f"Starting assignment for {request.student_id} (ID: {request_id})")
    
    return StreamingResponse(
        AssignmentGenerator.generate_stream(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "X-Request-ID": request_id
        }
    )


@app.post("/api/check-attempts")
async def check_attempts(request: CheckAttemptRequest):
    """
    Check how many attempts a user has remaining.
    Returns: { allowed: bool, attempts_used: int, attempts_remaining: int }
    """
    key = f"{request.student_id}:{request.skill}"
    attempts = attempt_storage[key]
    attempts_used = len(attempts)
    attempts_remaining = MAX_ATTEMPTS - attempts_used
    
    return JSONResponse({
        "allowed": attempts_remaining > 0,
        "attempts_used": attempts_used,
        "attempts_remaining": attempts_remaining,
        "max_attempts": MAX_ATTEMPTS
    })


@app.post("/api/register-attempt")
async def register_attempt(request: CheckAttemptRequest):
    """
    Register a new test attempt. Must be called before starting a test.
    Returns: { success: bool, attempt_number: int }
    """
    key = f"{request.student_id}:{request.skill}"
    attempts = attempt_storage[key]
    attempts_used = len(attempts)
    attempts_remaining = MAX_ATTEMPTS - attempts_used
    
    if attempts_remaining <= 0:
        raise HTTPException(
            status_code=403,
            detail="You have exhausted your attempts. You cannot take this test again."
        )
    
    # Register new attempt
    attempt_number = attempts_used + 1
    attempt_storage[key].append({
        "attempt_number": attempt_number,
        "timestamp": datetime.now().isoformat(),
        "status": "in_progress"
    })
    
    logger.info(f"Registered attempt {attempt_number} for {key}")
    
    return JSONResponse({
        "success": True,
        "attempt_number": attempt_number,
        "attempts_remaining": MAX_ATTEMPTS - attempt_number
    })


@app.post("/api/submit-result")
async def submit_result(request: SubmitResultRequest):
    """
    Submit test results and mark attempt as complete.
    """
    key = f"{request.student_id}:{request.skill}"
    
    # Find and update the in-progress attempt
    attempts = attempt_storage[key]
    for attempt in attempts:
        if attempt.get("status") == "in_progress":
            attempt["status"] = "completed"
            attempt["score"] = request.score
            attempt["total"] = request.total
            attempt["completed_at"] = datetime.now().isoformat()
            break
    
    # Store result
    with results_lock:
        result_entry = {
            "student_id": request.student_id,
            "student_name": request.student_name,
            "skill": request.skill,
            "score": request.score,
            "total": request.total,
            "percentage": round((request.score / request.total * 100), 2) if request.total > 0 else 0,
            "answers": request.answers,
            "time_taken": request.time_taken,
            "submitted_at": datetime.now().isoformat()
        }
        result_storage[key].append(result_entry)
    
    logger.info(f"Result submitted for {key}: {request.score}/{request.total}")
    
    return JSONResponse({
        "success": True,
        "score": request.score,
        "total": request.total,
        "percentage": result_entry["percentage"]
    })


@app.get("/api/results/{student_id}")
async def get_student_results(student_id: str):
    """Get all results for a student."""
    results = []
    for key, result_list in result_storage.items():
        if key.startswith(f"{student_id}:"):
            results.extend(result_list)
    
    return JSONResponse({"results": results})


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "model": "llama-3.1-8b-instant",
        "version": "4.1.0",
        "features": ["attempt_tracking", "result_storage", "retry_limit"]
    }


@app.get("/")
async def root():
    return {
        "service": "Assignment Generation Engine - Enhanced",
        "version": "4.1.0",
        "description": "Skill Assessment with Retry Tracking",
        "max_attempts": MAX_ATTEMPTS,
        "endpoints": {
            "POST /generate-assignment": "Generate quiz questions",
            "POST /api/check-attempts": "Check remaining attempts",
            "POST /api/register-attempt": "Register new attempt",
            "POST /api/submit-result": "Submit test result",
            "GET /api/results/{student_id}": "Get student results"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
