import json
import re

def load_skills(skills_file="skills.json"):
    with open(skills_file, "r") as f:
        return set(json.load(f)["skills"])

def load_aliases(config_file="config.json"):
    with open(config_file, "r") as f:
        return json.load(f).get("skill_aliases", {})

def normalize_text(text, alias_map):
    for alias, standard in alias_map.items():
        text = re.sub(rf'\b{re.escape(alias)}\b', standard, text, flags=re.IGNORECASE)
    return text

def extract_skills(text, skills_set, alias_map):
    text = normalize_text(text, alias_map)
    found = set()
    for skill in skills_set:
        if re.search(rf'\b{re.escape(skill)}\b', text, re.IGNORECASE):
            found.add(skill)
    return list(found)
