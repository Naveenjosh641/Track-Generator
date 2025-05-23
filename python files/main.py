import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Version endpoint
@app.get("/version")
def version():
    return {"model_version": "1.0.0"}

# Input model for /evaluate-fit
class FitRequest(BaseModel):
    resume_text: str
    job_description: str

# Output model (optional, for strict typing)
class LearningStep(BaseModel):
    skill: str
    steps: List[str]

class FitResponse(BaseModel):
    fit_score: float
    verdict: str
    matched_skills: List[str]
    missing_skills: List[str]
    recommended_learning_track: List[LearningStep]
    status: str

@app.post("/evaluate-fit", response_model=FitResponse)
def evaluate_fit(data: FitRequest):
    # Dummy logic (replace with actual scoring + skill extraction)
    return {
        "fit_score": 0.46,
        "verdict": "moderate_fit",
        "matched_skills": ["Python", "Cloud Basics"],
        "missing_skills": ["Node.js", "MongoDB", "Docker", "AWS", "System Design"],
        "recommended_learning_track": [
            {
                "skill": "Node.js",
                "steps": [
                    "Install Node.js and learn basic syntax",
                    "Understand asynchronous programming in JS",
                    "Build a REST API with Express.js",
                    "Handle authentication and routing"
                ]
            },
            {
                "skill": "Docker",
                "steps": [
                    "Understand containers vs virtual machines",
                    "Install Docker CLI and Docker Desktop",
                    "Write a Dockerfile for a simple app",
                    "Build and run Docker containers locally"
                ]
            }
        ],
        "status": "success"
    }

# Optional: dynamic port for local testing
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
