import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_cutoffs(config_file="config.json"):
    with open(config_file) as f:
        return json.load(f).get("fit_score_cutoffs", {})

def compute_fit_score(resume_text, jd_text):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return round(float(score), 2)

def get_verdict(score, cutoffs):
    if score >= cutoffs.get("strong_fit", 0.75): return "strong_fit"
    if score >= cutoffs.get("moderate_fit", 0.4): return "moderate_fit"
    return "weak_fit"
