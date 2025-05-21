from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from fit_score_engine import compute_fit_score
from skill_extractor import extract_skills, normalize_skills
from typing import List

# Load config and resources
with open("config.json") as f:
    config = json.load(f)

with open("skills.json") as f:
    skills_config = json.load(f)

with open("learning_paths.json") as f:
    learning_paths = json.load(f)

skill_alias_map = config["skill_alias_map"]
fit_score_cutoffs = config["fit_score_cutoffs"]
max_steps = config["max_learning_steps_per_skill"]

# Initialize FastAPI app
app = FastAPI(title="Resume–Role Fit Evaluator", version="1.0.0")


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
    status: str = "success"


@app.post("/evaluate-fit", response_model=FitResponse)
def evaluate_fit(request: FitRequest):
    resume_skills_raw = extract_skills(request.resume_text)
    job_skills_raw = extract_skills(request.job_description)

    resume_skills = normalize_skills(resume_skills_raw, skill_alias_map)
    job_skills = normalize_skills(job_skills_raw, skill_alias_map)

    matched_skills = [skill for skill in job_skills if skill in resume_skills]
    missing_skills = [skill for skill in job_skills if skill not in resume_skills]

    fit_score = compute_fit_score(matched_skills, job_skills)

    if fit_score >= fit_score_cutoffs["strong_fit"]:
        verdict = "strong_fit"
    elif fit_score >= fit_score_cutoffs["moderate_fit"]:
        verdict = "moderate_fit"
    else:
        verdict = "weak_fit"

    # Learning track generator
    recommended_learning_track = []
    for skill in missing_skills:
        if skill in learning_paths:
            steps = learning_paths[skill][:max_steps]
            recommended_learning_track.append({
                "skill": skill,
                "steps": steps
            })

    return {
        "fit_score": round(fit_score, 2),
        "verdict": verdict,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommended_learning_track": recommended_learning_track,
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"model_version": "1.0.0"}