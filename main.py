from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
import uuid

from skill_extractor import load_skills, load_aliases, extract_skills
from fit_score_engine import compute_fit_score, get_verdict, load_cutoffs

import json

app = FastAPI()
skills_set = load_skills()
aliases = load_aliases()
cutoffs = load_cutoffs()

# Load learning paths once
with open("learning_paths.json") as f:
    learning_paths = json.load(f)

class FitRequest(BaseModel):
    resume_text: str
    job_description: str

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
    resume_skills = extract_skills(data.resume_text, skills_set, aliases)
    jd_skills = extract_skills(data.job_description, skills_set, aliases)

    matched = list(set(resume_skills) & set(jd_skills))
    missing = list(set(jd_skills) - set(resume_skills))

    score = compute_fit_score(data.resume_text, data.job_description)
    verdict = get_verdict(score, cutoffs)

    track = []
    for skill in missing:
        if skill in learning_paths:
            steps = learning_paths[skill]["steps"][:4]  # Limit to 4
            track.append({"skill": skill, "steps": steps})

    return {
        "fit_score": score,
        "verdict": verdict,
        "matched_skills": matched,
        "missing_skills": missing,
        "recommended_learning_track": track,
        "status": "success"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/version")
def version():
    return {"model_version": "1.0.0"}
