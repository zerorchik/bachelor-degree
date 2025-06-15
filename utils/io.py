import os
import json
from models.candidate_response import CandidateResponse
from models.recruiter import Recruiter
from models.candidate import Candidate
from models.vacancy import Vacancy
from models.criteria import Criteria
import re

def generate_next_id(folder_path: str, prefix: str) -> str:
    existing_ids = []
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return f"{prefix}001"

    for name in os.listdir(folder_path):
        match = re.match(f"{prefix}(\\d{{3}})\\.json", name)
        if match:
            existing_ids.append(int(match.group(1)))

    next_num = 1
    while next_num in existing_ids:
        next_num += 1

    return f"{prefix}{next_num:03d}"

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_all_candidates(path):
    return [Candidate.from_dict(load_json(os.path.join(path, f)), CandidateResponse)
            for f in os.listdir(path) if f.endswith(".json")]

def load_all_vacancies(path):
    return [Vacancy.from_dict(load_json(os.path.join(path, f)))
            for f in os.listdir(path) if f.endswith(".json")]

def load_criteria_bank(path):
    return {f.split(".")[0]: Criteria.from_dict(load_json(os.path.join(path, f)))
            for f in os.listdir(path) if f.endswith(".json")}

def save_recruiter(recruiter, path):
    save_json(recruiter.to_dict(), os.path.join(path, f"{recruiter.id}.json"))

def load_all_recruiters(path):
    return [
        Recruiter.from_dict(load_json(os.path.join(path, fname)))
        for fname in os.listdir(path) if fname.endswith(".json")
    ]
