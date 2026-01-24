from typing import List
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone

# Add project root to sys.path to allow importing shared types
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from shared_formats.types import JobListing, SearchCriteria


class Engine:
    def __init__(self, criteria: SearchCriteria):
        self.criteria = criteria

    def filter_jobs(self, listings: List[JobListing]) -> List[JobListing]:
        filtered = []
        raw_keywords = self.criteria.keywords.lower()
        keyword_list = raw_keywords.split()

        cutoff_date = None
        if self.criteria.days_old:
            cutoff_date = datetime.now(timezone.utc) - timedelta(
                days=self.criteria.days_old
            )

        for job in listings:
            title = job.title.lower()

            # Date filtering
            if cutoff_date and job.created:
                try:
                    job_date = datetime.fromisoformat(
                        job.created.replace("Z", "+00:00")
                    )
                    if job_date < cutoff_date:
                        continue
                except (ValueError, AttributeError):
                    pass

            # Keyword matching
            if raw_keywords in title:
                filtered.append(job)
                continue
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
                score -= 5.0  # Penalty for low salary

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
