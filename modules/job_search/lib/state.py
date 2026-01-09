import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, Any

class UsageTracker:
    def __init__(self, state_file: str = ".adzuna_usage.json"):
        # Put state file in project root
        self.state_file = os.path.join(os.getcwd(), state_file)
        self.limits = {
            "minute": 25,
            "day": 250,
            "week": 1000,
            "month": 2500
        }
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        return {
            "requests": [] # List of timestamps (floats)
        }

    def _save_state(self):
        with open(self.state_file, "w") as f:
            json.dump(self.state, f)

    def _clean_old_requests(self):
        now = time.time()
        # Keep requests from the last 30 days (roughly a month)
        one_month_ago = now - (30 * 24 * 60 * 60)
        self.state["requests"] = [ts for ts in self.state["requests"] if ts > one_month_ago]

    def get_counts(self) -> Dict[str, int]:
        now = time.time()
        self._clean_old_requests()
        
        counts = {
            "minute": 0,
            "day": 0,
            "week": 0,
            "month": 0
        }
        
        minute_ago = now - 60
        day_ago = now - (24 * 60 * 60)
        week_ago = now - (7 * 24 * 60 * 60)
        month_ago = now - (30 * 24 * 60 * 60)
        
        for ts in self.state["requests"]:
            if ts > minute_ago:
                counts["minute"] += 1
            if ts > day_ago:
                counts["day"] += 1
            if ts > week_ago:
                counts["week"] += 1
            if ts > month_ago:
                counts["month"] += 1
                
        return counts

    def check_and_increment(self) -> bool:
        """Checks if any limits are exceeded. Increments if safe. Returns True if OK."""
        counts = self.get_counts()
        
        for period, limit in self.limits.items():
            if counts[period] >= limit:
                return False
                
        self.state["requests"].append(time.time())
        self._save_state()
        return True

    def get_limit_info(self) -> Dict[str, Any]:
        counts = self.get_counts()
        return {
            "current": counts,
            "limits": self.limits
        }
