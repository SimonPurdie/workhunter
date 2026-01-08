from typing import List
import re
import sys
from pathlib import Path

# Add project root to sys.path to allow importing shared types
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from shared.types import JobListing, SearchCriteria

class Engine:
    def __init__(self, criteria: SearchCriteria):
        self.criteria = criteria

    def filter_jobs(self, listings: List[JobListing]) -> List[JobListing]:
        filtered = []
        # Multi-keyword matching: prioritize titles that contain the full phrase
        raw_keywords = self.criteria.keywords.lower()
        keyword_list = raw_keywords.split()
        
        for job in listings:
            title = job.title.lower()
            # If the full phrase is in the title, it's a definite keep
            if raw_keywords in title:
                filtered.append(job)
                continue
                
            # Otherwise, if it's a multi-word search, check if most significant keywords match
            # For simplicity: keep if at least one keyword matches
            if any(kw in title for kw in keyword_list):
                filtered.append(job)
        
        return filtered

    def score_job(self, job: JobListing) -> float:
        score = 0.0
        
        # Freshness (hypothetical, Adzuna 'created' is a string)
        # For now, let's just use some heuristics
        
        # Salary scoring
        if job.salary_min and self.criteria.salary_min:
            if job.salary_min >= self.criteria.salary_min:
                score += 10.0
            else:
                score -= 5.0 # Penalty for low salary
        
        # Title relevance
        keywords = self.criteria.keywords.lower().split()
        title_lower = job.title.lower()
        match_count = sum(1 for kw in keywords if kw in title_lower)
        score += match_count * 5.0
        
        # Full-time preference (assumption)
        if job.contract_time == "full-time":
            score += 2.0
            
        return score

    def rank_jobs(self, listings: List[JobListing]) -> List[JobListing]:
        # Pair each job with its score
        scored_jobs = []
        for job in listings:
            score = self.score_job(job)
            scored_jobs.append((score, job))
            
        # Sort by score descending
        scored_jobs.sort(key=lambda x: x[0], reverse=True)
        
        return [job for score, job in scored_jobs]
