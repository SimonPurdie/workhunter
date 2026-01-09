#!/usr/bin/env python3
"""
Saves job search results to workspace with automatic naming.
Usage: python scripts/job_search/save_search.py < jobs.json

Creates:
  - workspace/jobsearch_YYYYMMDD_N.json
  - workspace/jobsearch_YYYYMMDD_N.md
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path
import subprocess

# Add project root and script lib to sys.path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(Path(__file__).parent / "lib"))

import lib.job_tracker as job_tracker

def get_next_filename(base_dir, date_str):
    """Find next available number for today's date."""
    counter = 1
    while True:
        base = f"jobsearch_{date_str}_{counter}"
        json_path = base_dir / f"{base}.json"
        if not json_path.exists():
            return base
        counter += 1

def main():
    try:
        # Read JSON from stdin
        data = json.load(sys.stdin)
        
        # Ensure workspace directory exists
        workspace = Path("workspace")
        workspace.mkdir(exist_ok=True)
        
        # Generate filename
        date_str = datetime.now().strftime("%Y%m%d")
        base_name = get_next_filename(workspace, date_str)
        
        json_path = workspace / f"{base_name}.json"
        md_path = workspace / f"{base_name}.md"
        
        # Save JSON
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Generate markdown report
        script_dir = Path(__file__).parent
        formatter = script_dir / "lib/format_markdown.py"
        
        with open(json_path, 'r') as json_file:
            result = subprocess.run(
                ['python', str(formatter)],
                stdin=json_file,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.returncode != 0:
                print(f"Warning: Markdown generation failed - {result.stderr}", file=sys.stderr)
            else:
                with open(md_path, 'w') as f:
                    f.write(result.stdout)
        
        # Track these jobs
        job_tracker.add_seen_jobs(data)
        
        # Periodic cleanup
        job_tracker.cleanup_old_entries(days=60)

        # Output success message
        print(json.dumps({
            "status": "success",
            "files_created": [str(json_path), str(md_path)],
            "job_count": len(data)
        }, indent=2))
        
    except json.JSONDecodeError as e:
        print(json.dumps({
            "error": "invalid_json",
            "message": str(e)
        }), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "error": "save_failed",
            "message": str(e)
        }), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()