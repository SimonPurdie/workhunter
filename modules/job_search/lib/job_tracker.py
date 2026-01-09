import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Set

TRACKING_FILE = Path("workspace/job_search/seen_jobs.json")

def generate_hash(company: str, title: str, location: str) -> str:
    """Generate a unique ID for a job based on its signature."""
    signature = f"{company.strip().lower()}|{title.strip().lower()}|{location.strip().lower()}"
    return hashlib.md5(signature.encode()).hexdigest()

def load_seen_jobs() -> List[Dict]:
    """Load seen jobs from the tracking file."""
    if not TRACKING_FILE.exists():
        return []
    
    try:
        with open(TRACKING_FILE, 'r') as f:
            data = json.load(f)
            return data.get("jobs", [])
    except (json.JSONDecodeError, IOError):
        return []

def save_seen_jobs(jobs: List[Dict]):
    """Save seen jobs to the tracking file."""
    TRACKING_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TRACKING_FILE, 'w') as f:
        json.dump({"jobs": jobs}, f, indent=2)

def is_seen(job_hash: str, seen_hashes: Set[str]) -> bool:
    """Check if a job has already been seen."""
    return job_hash in seen_hashes

def add_seen_jobs(new_jobs: List[Dict]):
    """Add new jobs to the tracking record."""
    seen_jobs = load_seen_jobs()
    seen_hashes = {j["hash"] for j in seen_jobs}
    
    added = False
    for job in new_jobs:
        job_hash = generate_hash(job["company"], job["title"], job["location"])
        if job_hash not in seen_hashes:
            seen_jobs.append({
                "hash": job_hash,
                "company": job["company"],
                "title": job["title"],
                "location": job["location"],
                "first_seen": datetime.now().strftime("%Y-%m-%d"),
                "redirect_url": job.get("redirect_url", "")
            })
            seen_hashes.add(job_hash)
            added = True
            
    if added:
        save_seen_jobs(seen_jobs)

def cleanup_old_entries(days: int = 60):
    """Remove entries older than the specified number of days."""
    seen_jobs = load_seen_jobs()
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    filtered_jobs = [
        job for job in seen_jobs 
        if job.get("first_seen", "0000-00-00") >= cutoff_date
    ]
    
    if len(filtered_jobs) < len(seen_jobs):
        save_seen_jobs(filtered_jobs)
