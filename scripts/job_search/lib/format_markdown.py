#!/usr/bin/env python3
"""
Converts job search JSON output to a formatted markdown report.
Usage: python scripts/job_search/format_markdown.py < jobs.json > output.md
"""

import json
import sys
from datetime import datetime

def format_salary(job):
    """Format salary range as a readable string."""
    min_sal = job.get('salary_min')
    max_sal = job.get('salary_max')
    
    if min_sal and max_sal:
        return f"£{min_sal:,.0f} - £{max_sal:,.0f}"
    elif min_sal:
        return f"£{min_sal:,.0f}+"
    elif max_sal:
        return f"Up to £{max_sal:,.0f}"
    else:
        return "Salary not specified"

def main():
    try:
        # Read JSON from stdin
        data = json.load(sys.stdin)
        
        # Generate report
        print(f"# Job Search Results")
        print(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"**Total Results**: {len(data)}")
        print()
        print("---")
        print()
        
        for idx, job in enumerate(data, 1):
            print(f"## {idx}. {job.get('title', 'Unknown Title')}")
            print()
            print(f"**Company**: {job.get('company', 'Not specified')}")
            print(f"**Location**: {job.get('location', 'Not specified')}")
            print(f"**Salary**: {format_salary(job)}")
            print()
            
            # Description snippet
            desc = job.get('description', '').strip()
            if desc:
                # Limit to ~200 chars
                if len(desc) > 200:
                    desc = desc[:197] + "..."
                print(f"**Description**: {desc}")
                print()
            
            # Application URL
            url = job.get('redirect_url', '')
            if url:
                print(f"**Apply**: {url}")
            else:
                print("**Apply**: URL not available")
            
            # Agent notes if present
            notes = job.get('agent_notes', '').strip()
            if notes:
                print()
                print(f"**Agent Notes**: {notes}")
            
            print()
            print("---")
            print()
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()