import os
import requests
from typing import List, Optional
from dotenv import load_dotenv
import sys
from pathlib import Path

# Add project root to sys.path to allow importing shared types
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from shared_formats.types import JobListing, SearchCriteria
from .state import UsageTracker


class RateLimitExceeded(Exception):
    def __init__(self, limit_info):
        self.limit_info = limit_info
        super().__init__(f"Adzuna rate limit exceeded: {limit_info}")


load_dotenv()


class AdzunaClient:
    def __init__(self):
        self.app_id = os.getenv("ADZUNA_APP_ID")
        self.app_key = os.getenv("ADZUNA_APP_KEY")
        self.base_url = "https://api.adzuna.com/v1/api/jobs/gb/search"

        if not self.app_id or not self.app_key:
            raise ValueError("ADZUNA_APP_ID and ADZUNA_APP_KEY must be set in .env")

        self.tracker = UsageTracker()

    def search_jobs(self, criteria: SearchCriteria) -> List[JobListing]:
        if not self.tracker.check_and_increment():
            raise RateLimitExceeded(self.tracker.get_limit_info())

        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "what": criteria.keywords,
            "where": criteria.location,
            "distance": int(criteria.distance),
            "results_per_page": criteria.results_per_page,
            "content-type": "application/json",
        }

        if criteria.salary_min:
            params["salary_min"] = int(criteria.salary_min)

        if criteria.salary_max:
            params["salary_max"] = int(criteria.salary_max)

        if criteria.sort_by:
            params["sort_by"] = criteria.sort_by

        if criteria.what_exclude:
            params["what_exclude"] = criteria.what_exclude

        if criteria.full_time:
            params["full_time"] = 1

        if criteria.permanent:
            params["permanent"] = 1

        if criteria.contract:
            params["contract"] = 1

        if criteria.part_time:
            params["part_time"] = 1

        url = f"{self.base_url}/{criteria.page}"
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])

        listings = []
        for res in results:
            listings.append(
                JobListing(
                    id=str(res.get("id")),
                    title=res.get("title", ""),
                    company=res.get("company", {}).get("display_name", ""),
                    location=res.get("location", {}).get("display_name", ""),
                    salary_min=res.get("salary_min"),
                    salary_max=res.get("salary_max"),
                    description=res.get("description", ""),
                    redirect_url=res.get("redirect_url", ""),
                    created=res.get("created", ""),
                    category=res.get("category", {}).get("label"),
                    contract_time=res.get("contract_time"),
                    contract_type=res.get("contract_type"),
                )
            )
        return listings
