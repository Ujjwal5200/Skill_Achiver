"""
Assignment Generation Engine - AI Question Generator
=================================================
Pure AI module for generating questions.
Can be used in any project.
"""

import json
import os
import asyncio
import logging
import time
from groq import AsyncGroq, RateLimitError
from dotenv import load_dotenv
from typing import List, AsyncGenerator
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

groq_client = AsyncGroq(api_key=GROQ_API_KEY)


class AssignmentRequest:
    def __init__(self, student_id: str, student_name: str, skills: List[str], exp_level: str, subject: str | None = None):
        self.student_id = student_id
        self.student_name = student_name
        self.skills = skills
        self.exp_level = exp_level
        self.subject = subject or (skills[0] if skills else "")


class AssignmentGenerator:
    """Generator for quiz questions using Groq AI"""
    
    @staticmethod
    def _build_prompt(skills: List[str], exp_level: str) -> str:
        prompt = f"""You are a PRINCIPAL ENGINEER at FAANG (ex-Google/Amazon) designing the final promotion exam for L7 → L8 level.
This exam is LEGENDARY and BRUTAL — it has a strict 5–10% pass rate. It is specifically designed to separate truly exceptional engineers from confident but shallow seniors. Most candidates who think they are ready will fail.

STUDENT PROFILE:
Skills: {json.dumps(skills)}
Experience: {exp_level.replace('_', ' ').title()}

MISSION: Generate **exactly 20 brutally hard MCQs** that test deep production mastery.
Only engineers with exceptional insight, battle-tested intuition, and the ability to synthesize multiple complex concepts under extreme time pressure should pass.

ANTI-CHEATING & TIME RULES (HIGHEST PRIORITY):
- Questions 1-10 must be solvable by a true expert in **15 seconds** via deep intuition.
- Questions 11-15 in **20 seconds**.
- Questions 16-20 in **25 seconds**.
- Every question must be **unique, custom-crafted, and context-specific**. No generic textbook scenarios, no common interview questions, no repeated patterns or structures across the 20 questions.
- Design so that **Google Lens + reverse image search + ChatGPT fails** within the time limit. Include unique quantitative constraints and subtle twists that don't exist in any public source.
- Cheaters using OCR will get plausible but dangerously wrong answers due to counter-intuitive production realities.

SPECIFIC LENGTH CONSTRAINT FOR FAST READING:
- **Q1–10 (15-second questions)**: Keep the question text **short and concise** — maximum 1-2 sentences (ideally under 60-70 words total). The student must be able to read and comprehend the question quickly, but the conceptual depth and synthesis required must still be extremely high. Use tight, precise wording with embedded scale twists or conflicting goals.
- **Q11–15**: Moderately longer (3-5 sentences if needed for context).
- **Q16–20**: Full 7–10 line realistic war-story scenarios with specific metrics.

DIFFICULTY RULES (STRICTLY NON-NEGOTIABLE):
- NO basic syntax, API recall, or simple code output questions.
- Every question must force synthesis of **at least 3–5 interconnected concepts** tailored to the student's skills (e.g., distributed locking + consistency + partial failures + observability + security + performance at scale).
- The "obvious" textbook answer must be **wrong or dangerously incomplete** in real production. Correct answer should feel counter-intuitive yet precisely right.
- Distractors must be highly plausible (what a strong L6/L7 would pick confidently) but contain subtle critical flaws.
- Explanations: 2-3 sentences max, highlighting why obvious choices fail at scale and the systemic risks/trade-offs.

QUESTION TYPES (Balanced & Progressive):
Q1–10: Short Advanced Edge-Case Questions (15s)
  Short, crisp questions with high-stakes nuanced twists. Deep dives into subtle behaviors, race conditions, or consistency traps with unexpected constraints. Make them readable instantly but require elite judgment.

Q11–15: Complex Multi-Concept Traps (20s)(long enough to require reading but not too long to exceed time limit)
  Combine 4+ domains with conflicting priorities and long-term impacts.

Q16–20: The Gauntlet — Production War Stories (25s)(long enough to set a rich context but focused on critical decision points , at least 7-10 lines of text)
  Detailed, authentic-feeling incidents with unique metrics. Ask for root cause, best mitigation, or optimal trade-off.

ADDITIONAL CRITICAL INSTRUCTIONS:
- Ensure **maximum diversity** in domains and no repetition of concepts, failure modes, or question structures (especially avoid any similarity in Q1-4 or early questions).
- Vary correct answer letters (no patterns).
- For multi-correct questions: At least 2–3 correct options; distractors seem valid in isolation but break under full interplay.
- Include at least 3–4 questions with security implications or cross-domain failures.
- The entire set must resist image recognition and quick LLM prompting through personalized, synthesis-heavy design.

OUTPUT ONLY VALID JSON (nothing else).

JSON Schema:
{{
  "title": "string",
  "objective": "string",
  "difficulty": "brutal",
  "pass_rate_target": "5-10%",
  "total_questions": 20,
  "time_constraints": "15s for Q1-10 (short questions), 20s for Q11-15, 25s for Q16-20",
  "mcqs": [
    {{
      "id": int,
      "type": "single" | "multi" | "special",
      "question": "string",
      "options": ["A. ...", "B. ...", "C. ...", "D. ..."] or more,
      "correct": "A. ..." or ["B. ...", "D. ..."] or "none of the above",
      "explanation": "string (2-3 sentences max)"
    }}
  ]
}}

Generate the JSON now. Make Q1-10 short but brutally insightful, Q1-20 ensure zero repetition, and maintain elite-level rigor throughout."""
        
        return prompt
    
    @staticmethod
    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(RateLimitError)
    )
    async def generate_stream(self, request: AssignmentRequest) -> AsyncGenerator[str, None]:
        """Generate assignment using streaming (like old working code)"""
        start_time = time.time()
        prompt = AssignmentGenerator._build_prompt(request.skills, request.exp_level)
        
        try:
            stream = await groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a technical examiner. Generate ONLY valid JSON. No markdown. No explanations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=7000,
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
                logger.error(f"JSON decode error: {str(e)}")
                yield json.dumps({
                    "type": "error",
                    "error": f"Invalid JSON: {str(e)}",
                    "raw_output_preview": full_response[:300],
                    "cost_inr": 0.0
                }) + "\n"
                
        except RateLimitError as e:
            logger.warning(f"Rate limit hit, retried")
            yield json.dumps({
                "type": "error",
                "error": "Rate limit exceeded. Retrying...",
                "cost_inr": 0.0
            }) + "\n"
            
        except Exception as e:
            logger.error(f"Generation failed: {str(e)}")
            yield json.dumps({
                "type": "error",
                "error": str(e),
                "cost_inr": 0.0
            }) + "\n"


async def generate_quiz(student_id: str, student_name: str, skills: List[str], exp_level: str) -> dict:
    """Helper function to generate quiz - returns full assignment dict"""
    request = AssignmentRequest(
        student_id=student_id,
        student_name=student_name,
        skills=skills,
        exp_level=exp_level
    )
    
    full_response = ""
    try:
        async for chunk in AssignmentGenerator.generate_stream(request):
            data = json.loads(chunk)
            if data.get("type") == "token":
                full_response += data.get("content", "")
            elif data.get("type") == "complete":
                return data.get("assignment", {})
            elif data.get("type") == "error":
                logger.error(f"Generation error: {data.get('error')}")
                return {"assignment": {"title": "", "skills": skills, "difficulty": "hard", "mcqs": []}}
    except Exception as e:
        logger.error(f"Stream error: {e}")
    
    # Try to parse accumulated response
    try:
        return json.loads(full_response)
    except:
        return {"assignment": {"title": "", "skills": skills, "difficulty": "hard", "mcqs": []}}


if __name__ == "__main__":
    async def test():
        result = await generate_quiz("test_user", "Test User", ["Python"], "5 years")
        print(json.dumps(result, indent=2)[:2000])
    
    asyncio.run(test())