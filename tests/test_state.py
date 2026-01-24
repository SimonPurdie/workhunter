import os
import time
import json
import pytest
from modules.job_search.components.state import UsageTracker


@pytest.fixture
def temp_usage_file(tmp_path):
    usage_file = tmp_path / "test_usage.json"
    return str(usage_file)


def test_usage_tracker_init(temp_usage_file):
    tracker = UsageTracker(state_file=temp_usage_file)
    assert tracker.state == {"requests": []}


def test_usage_tracker_increment(temp_usage_file):
    tracker = UsageTracker(state_file=temp_usage_file)
    assert tracker.check_and_increment() is True
    assert len(tracker.state["requests"]) == 1


def test_usage_tracker_limits(temp_usage_file):
    tracker = UsageTracker(state_file=temp_usage_file)
    # Set a small limit for testing
    tracker.limits["minute"] = 2

    assert tracker.check_and_increment() is True
    assert tracker.check_and_increment() is True
    assert tracker.check_and_increment() is False


def test_usage_tracker_persistence(temp_usage_file):
    tracker1 = UsageTracker(state_file=temp_usage_file)
    tracker1.check_and_increment()

    tracker2 = UsageTracker(state_file=temp_usage_file)
    assert len(tracker2.state["requests"]) == 1


def test_usage_tracker_clean_old(temp_usage_file):
    tracker = UsageTracker(state_file=temp_usage_file)
    # Add an old request (31 days ago)
    old_ts = time.time() - (31 * 24 * 60 * 60)
    tracker.state["requests"].append(old_ts)
    tracker._save_state()

    tracker.get_counts()  # This calls _clean_old_requests
    assert len(tracker.state["requests"]) == 0
