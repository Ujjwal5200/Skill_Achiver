"""
============================================================
  main.py  —  FASTAPI BACKEND  (Exam Assessment System)
============================================================
  PURPOSE:
    Complete exam system with AI question generation + attempt tracking
    Uses assignment_engine.py as the core engine
  RUN:
    uvicorn main:app --reload --host 0.0.0.0 --port 8001
============================================================
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List

from assignment_engine import (
    AssignmentRequest,
    AssignmentGenerator,
    attempt_storage,
    result_storage,
    results_lock,
    MAX_ATTEMPTS,
    app as engine_app,
)

app = FastAPI(
    title="Exam Assessment System",
    description="Secure exam platform with AI questions and retry limits",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/app")
async def serve_app():
    with open("app.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.post("/api/check-attempts")
async def check_attempts(body: dict = Body(...)):
    """Check how many attempts a user has remaining."""
    student_id = body.get("student_id")
    skill = body.get("skill")
    if not student_id or not skill:
        raise HTTPException(status_code=400, detail="student_id and skill required")
    
    key = f"{student_id}:{skill}"
    attempts = attempt_storage[key]
    attempts_used = len(attempts)
    attempts_remaining = MAX_ATTEMPTS - attempts_used
    
    return {
        "allowed": attempts_remaining > 0,
        "attempts_used": attempts_used,
        "attempts_remaining": attempts_remaining,
        "max_attempts": MAX_ATTEMPTS
    }


@app.post("/api/register-attempt")
async def register_attempt(body: dict = Body(...)):
    """Register a new test attempt. Must be called before starting a test."""
    student_id = body.get("student_id")
    skill = body.get("skill")
    if not student_id or not skill:
        raise HTTPException(status_code=400, detail="student_id and skill required")
    
    key = f"{student_id}:{skill}"
    attempts = attempt_storage[key]
    attempts_used = len(attempts)
    attempts_remaining = MAX_ATTEMPTS - attempts_used
    
    if attempts_remaining <= 0:
        raise HTTPException(status_code=403, detail="Maximum attempts exhausted")
    
    attempt_number = attempts_used + 1
    attempt_storage[key].append({
        "attempt_number": attempt_number,
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "status": "in_progress"
    })
    
    return {
        "success": True,
        "attempt_number": attempt_number,
        "attempts_remaining": attempts_remaining - 1
    }


@app.post("/generate-assignment")
async def generate_assignment(request: AssignmentRequest):
    """Generate assignment questions from the AI engine."""
    return StreamingResponse(
        AssignmentGenerator.generate_stream(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@app.post("/api/submit-result")
async def submit_result(body: dict = Body(...)):
    """Submit test results and mark attempt as complete."""
    student_id = body.get("student_id")
    skill = body.get("skill")
    if not student_id or not skill:
        raise HTTPException(status_code=400, detail="student_id and skill required")
    
    key = f"{student_id}:{skill}"
    
    for attempt in attempt_storage[key]:
        if attempt.get("status") == "in_progress":
            attempt["status"] = "completed"
            attempt["completed_at"] = __import__('datetime').datetime.now().isoformat()
            break
    
    with results_lock:
        result_storage[key].append({
            "student_id": student_id,
            "skill": skill,
            "score": body.get("score", 0),
            "total": body.get("total", 0),
            "percentage": round((body.get("score", 0) / max(body.get("total", 1), 1) * 100), 2),
            "answers": body.get("answers", {}),
            "time_taken": body.get("time_taken", 0),
            "submitted_at": __import__('datetime').datetime.now().isoformat()
        })
    
    return {
        "success": True,
        "message": "Result saved"
    }


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "2.0.0",
        "max_attempts": MAX_ATTEMPTS
    }


@app.get("/api/results/{student_id}")
async def get_student_results(student_id: str):
    """Get all results for a student."""
    results = []
    for key, result_list in result_storage.items():
        if key.startswith(f"{student_id}:"):
            results.extend(result_list)
    return {"results": results}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
