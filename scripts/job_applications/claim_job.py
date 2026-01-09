"""
script: scripts/job_applications/claim_job.py
description: Claims the next job from the queue, moves it to a unique application folder, and updates the queue.
"""

import os
import json
import glob
from datetime import datetime
from pathlib import Path

# Configuration
ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
QUEUE_DIR = ROOT_DIR / "workspace" / "applications" / "queue"
APPS_DIR = ROOT_DIR / "workspace" / "applications"

def get_next_application_folder():
    """
    Determines the next available folder name based on the date and an incremental counter.
    Format: job-YYYYMMDD-#
    """
    date_str = datetime.now().strftime("%Y%m%d")
    
    # Ensure directory exists
    os.makedirs(APPS_DIR, exist_ok=True)
    
    # Find existing folders for today
    pattern = APPS_DIR / f"job-{date_str}-*"
    existing_dirs = glob.glob(str(pattern))
    
    max_count = 0
    for path in existing_dirs:
        try:
            # Extract the number at the end
            folder_name = os.path.basename(path)
            count = int(folder_name.split('-')[-1])
            if count > max_count:
                max_count = count
        except (ValueError, IndexError):
            continue
            
    new_count = max_count + 1
    new_folder_name = f"job-{date_str}-{new_count}"
    return APPS_DIR / new_folder_name

def claim_job():
    """
    Main logic to pop a job from the queue and set up the workspace.
    """
    # 1. Find the first available JSON file in the queue
    queue_files = sorted(list(QUEUE_DIR.glob("*.json")))
    
    if not queue_files:
        print("No jobs found in queue.")
        return

    target_file = queue_files[0]
    
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            jobs = json.load(f)
            
        # Handle case where file is a list or a single object
        if isinstance(jobs, dict):
            jobs = [jobs]
            
        if not jobs:
            print(f"Queue file {target_file.name} is empty. Removing.")
            os.remove(target_file)
            # Recursively try next file
            claim_job() 
            return

        # 2. Pop the first job
        current_job = jobs.pop(0)
        
        # 3. Create the new application folder
        new_app_dir = get_next_application_folder()
        os.makedirs(new_app_dir, exist_ok=True)
        
        # 4. Write the job.json to the new folder
        job_file_path = new_app_dir / "job.json"
        with open(job_file_path, 'w', encoding='utf-8') as f:
            json.dump(current_job, f, indent=2)
            
        # 5. Update or Delete the source queue file
        if len(jobs) == 0:
            os.remove(target_file)
        else:
            with open(target_file, 'w', encoding='utf-8') as f:
                json.dump(jobs, f, indent=2)
                
        # 6. Output the result for the Agent to capture
        print(f"SUCCESS: Job claimed.")
        print(f"DIRECTORY: {new_app_dir}")
        print(f"JOB_TITLE: {current_job.get('title', 'Unknown')}")
        print(f"COMPANY: {current_job.get('company', 'Unknown')}")

    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON in {target_file.name}")
    except Exception as e:
        print(f"Error claiming job: {str(e)}")

if __name__ == "__main__":
    claim_job()