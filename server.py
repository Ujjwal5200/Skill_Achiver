import os
import json
import csv
import logging
import threading
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAX_ATTEMPTS = 2
DATA_FILE = "assessment_data.csv"
DATA_EXPIRY_HOURS = 48

def init_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["student_id", "student_name", "skill", "experience", "attempts_used", "score", "total", "percentage", "status", "time_taken", "last_attempt", "submitted_at"])

init_data_file()

def cleanup_old_data():
    try:
        cutoff_time = datetime.now() - timedelta(hours=DATA_EXPIRY_HOURS)
        rows = []
        fieldnames = ["student_id", "student_name", "skill", "experience", "attempts_used", "score", "total", "percentage", "status", "time_taken", "last_attempt", "submitted_at"]
        with open(DATA_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    last_attempt = datetime.fromisoformat(row.get('last_attempt', '2000-01-01'))
                    submitted_at = datetime.fromisoformat(row.get('submitted_at', '2000-01-01'))
                    if last_attempt > cutoff_time or submitted_at > cutoff_time:
                        rows.append(row)
                except:
                    continue
        
        with open(DATA_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        logger.info("Cleaned up data older than 48 hours")
    except Exception as e:
        logger.error(f"Cleanup error: {e}")

cleanup_old_data()

def get_user_data(student_id, skill):
    try:
        with open(DATA_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['student_id'] == student_id and row['skill'] == skill:
                    return {
                        'attempts_used': int(row.get('attempts_used', 0)),
                        'score': int(row.get('score', 0)),
                        'total': int(row.get('total', 0)),
                        'percentage': float(row.get('percentage', 0))
                    }
    except:
        pass
    return {'attempts_used': 0, 'score': 0, 'total': 0, 'percentage': 0}

def save_user_attempt(student_id, student_name, skill, experience=""):
    existing = get_user_data(student_id, skill)
    attempts = existing.get('attempts_used', 0)
    rows = []
    found = False
    try:
        with open(DATA_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['student_id'] == student_id and row['skill'] == skill:
                    row['attempts_used'] = str(attempts + 1)
                    row['student_name'] = student_name
                    row['experience'] = str(experience)
                    row['last_attempt'] = datetime.now().isoformat()
                    found = True
                rows.append(row)
    except:
        pass
    if not found:
        rows.append({'student_id': student_id, 'student_name': student_name, 'skill': skill, 'attempts_used': '1', 'score': '0', 'total': '0', 'percentage': '0', 'experience': str(experience), 'time_taken': '0', 'last_attempt': datetime.now().isoformat(), 'submitted_at': ''})
    
    with open(DATA_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["student_id", "student_name", "skill", "experience", "attempts_used", "score", "total", "percentage", "status", "time_taken", "last_attempt", "submitted_at"])
        writer.writeheader()
        writer.writerows(rows)

def save_user_result(student_id, student_name, skill, score, total, time_taken):
    percentage = round((score / total * 100), 2) if total > 0 else 0
    status = "PASS" if percentage >= 80 else "FAIL"
    rows = []
    found = False
    try:
        with open(DATA_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['student_id'] == student_id and row['skill'] == skill:
                    row['score'] = str(score)
                    row['total'] = str(total)
                    row['percentage'] = str(percentage)
                    row['status'] = status
                    row['time_taken'] = str(time_taken)
                    row['submitted_at'] = datetime.now().isoformat()
                    found = True
                rows.append(row)
    except:
        pass
    if not found:
        rows.append({'student_id': student_id, 'student_name': student_name, 'skill': skill, 'attempts_used': '1', 'score': str(score), 'total': str(total), 'percentage': str(percentage), 'time_taken': str(time_taken), 'last_attempt': datetime.now().isoformat(), 'submitted_at': datetime.now().isoformat()})
    
    with open(DATA_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["student_id", "student_name", "skill", "experience", "attempts_used", "score", "total", "percentage", "status", "time_taken", "last_attempt", "submitted_at"])
        writer.writeheader()
        writer.writerows(rows)

def get_user_results(student_id):
    results = []
    try:
        with open(DATA_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['student_id'] == student_id and row.get('submitted_at'):
                    results.append(row)
    except:
        pass
    return results

HTML_PATH = os.path.join(BASE_DIR, "app.html")

@app.get("/")
@app.get("/app.html")
async def serve_html():
    try:
        with open(HTML_PATH, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        html_content = html_content.replace(
            "const API_BASE = 'http://127.0.0.1:8001';",
            "const API_BASE = '';"
        )
        
        return Response(html_content, media_type="text/html")
    except Exception as e:
        logger.error(f"Error serving HTML: {e}")
        return Response(f"Error: {e}", status_code=500)

@app.post("/api/check-attempts")
async def check_attempts(request: dict):
    student_id = request.get("student_id")
    skill = request.get("skill")
    data = get_user_data(student_id, skill)
    attempts_used = data.get('attempts_used', 0)
    attempts_remaining = MAX_ATTEMPTS - attempts_used
    return {"allowed": attempts_remaining > 0, "attempts_used": attempts_used, "attempts_remaining": attempts_remaining, "max_attempts": MAX_ATTEMPTS}

@app.post("/api/register-attempt")
async def register_attempt(request: dict):
    student_id = request.get("student_id")
    student_name = request.get("student_name", "")
    skill = request.get("skill")
    experience = request.get("experience", "")
    data = get_user_data(student_id, skill)
    attempts_used = data.get('attempts_used', 0)
    attempts_remaining = MAX_ATTEMPTS - attempts_used
    if attempts_remaining <= 0:
        raise HTTPException(status_code=403, detail="Attempts exhausted")
    attempt_number = attempts_used + 1
    save_user_attempt(student_id, student_name, skill, experience)
    return {"success": True, "attempt_number": attempt_number, "attempts_remaining": MAX_ATTEMPTS - attempt_number}

@app.post("/api/submit-result")
async def submit_result(request: dict):
    student_id = request.get("student_id")
    student_name = request.get("student_name")
    skill = request.get("skill")
    score = request.get("score", 0)
    total = request.get("total", 20)
    time_taken = request.get("time_taken", 0)
    
    save_user_result(student_id, student_name, skill, score, total, time_taken)
    
    percentage = round((score / total * 100), 2) if total > 0 else 0
    status = "PASS" if percentage >= 80 else "FAIL"
    return {"success": True, "score": score, "total": total, "percentage": percentage, "status": status}

@app.get("/api/results/{student_id}")
async def get_results(student_id: str):
    results = get_user_results(student_id)
    return results

@app.get("/api/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/generate-assignment")
async def generate_assignment(request: dict):
    from assignment_engine import AssignmentGenerator, AssignmentRequest
    from fastapi.responses import StreamingResponse
    
    skill = request.get("skills", [request.get("skill", "")])[0]
    exp = request.get("exp_level", "3 years")
    
    req = AssignmentRequest(
        student_id=request.get("student_id", " anon"),
        student_name=request.get("student_name", "User"),
        skills=[skill],
        exp_level=exp
    )
    
    async def stream():
        try:
            async for chunk in AssignmentGenerator.generate_stream(req):
                yield chunk.encode() if isinstance(chunk, str) else chunk
        except Exception as e:
            logger.error(f"Generation error: {e}")
            yield b'{"type":"error","error":"Failed to generate questions"}'
        finally:
            yield b'{"type":"complete","assignment":{"mcqs":[]}}'
    
    return StreamingResponse(stream(), media_type="application/x-ndjson")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)