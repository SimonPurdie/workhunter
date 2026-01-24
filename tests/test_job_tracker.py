import json
import pytest
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from modules.job_search.components.job_tracker import (
    generate_hash,
    load_seen_jobs,
    save_seen_jobs,
    is_seen,
    add_seen_jobs,
    cleanup_old_entries,
)


@pytest.fixture
def temp_tracking_file(tmp_path):
    """Create a temporary tracking file path."""
    tracking_file = tmp_path / "seen_jobs.json"
    with patch(
        "modules.job_search.components.job_tracker.TRACKING_FILE", tracking_file
    ):
        yield tracking_file


def test_generate_hash():
    """Test that hash generation is consistent and normalized."""
    h1 = generate_hash("Company", "Title", "Location")
    h2 = generate_hash(" company ", " TITLE ", " location ")
    assert h1 == h2
    assert len(h1) == 32  # MD5 hex digest length


def test_load_seen_jobs_missing(temp_tracking_file):
    """Test loading when file doesn't exist."""
    assert load_seen_jobs() == []


def test_load_seen_jobs_valid(temp_tracking_file):
    """Test loading valid jobs from file."""
    jobs = [{"hash": "abc", "company": "Test"}]
    with open(temp_tracking_file, "w") as f:
        json.dump({"jobs": jobs}, f)

    loaded = load_seen_jobs()
    assert loaded == jobs


def test_save_seen_jobs(temp_tracking_file):
    """Test saving jobs to file."""
    jobs = [{"hash": "abc", "company": "Test"}]
    save_seen_jobs(jobs)

    assert temp_tracking_file.exists()
    with open(temp_tracking_file, "r") as f:
        data = json.load(f)
        assert data["jobs"] == jobs


def test_add_seen_jobs(temp_tracking_file):
    """Test adding new jobs and deduplication."""
    initial_jobs = [
        {
            "hash": generate_hash("Old Co", "Old Title", "Old Loc"),
            "company": "Old Co",
            "title": "Old Title",
            "location": "Old Loc",
            "first_seen": "2026-01-01",
        }
    ]
    save_seen_jobs(initial_jobs)

    new_jobs = [
        {"company": "Old Co", "title": "Old Title", "location": "Old Loc"},  # Duplicate
        {"company": "New Co", "title": "New Title", "location": "New Loc"},  # New
    ]

    add_seen_jobs(new_jobs)

    loaded = load_seen_jobs()
    assert len(loaded) == 2
    assert any(j["company"] == "New Co" for j in loaded)


def test_cleanup_old_entries(temp_tracking_file):
    """Test removing old entries."""
    now = datetime.now()
    old_date = (now - timedelta(days=70)).strftime("%Y-%m-%d")
    recent_date = (now - timedelta(days=10)).strftime("%Y-%m-%d")

    jobs = [
        {"hash": "old", "first_seen": old_date},
        {"hash": "recent", "first_seen": recent_date},
    ]
    save_seen_jobs(jobs)

    cleanup_old_entries(days=60)

    loaded = load_seen_jobs()
    assert len(loaded) == 1
    assert loaded[0]["hash"] == "recent"
