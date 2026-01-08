import os
import json
from workhunter.discovery.state import UsageTracker

def test_usage_tracker():
    test_file = ".test_usage.json"
    if os.path.exists(test_file):
        os.remove(test_file)
        
    tracker = UsageTracker(test_file)
    tracker.limits = {"minute": 2, "day": 10, "week": 20, "month": 30} # Low limits for testing
    
    # Test increments
    assert tracker.check_and_increment() == True
    assert tracker.check_and_increment() == True
    
    # Test limit hit
    assert tracker.check_and_increment() == False
    
    info = tracker.get_limit_info()
    assert info["current"]["minute"] == 2
    
    print("UsageTracker test passed!")
    if os.path.exists(test_file):
        os.remove(test_file)

if __name__ == "__main__":
    test_usage_tracker()
