import argparse
import json
import sys
from workhunter.discovery.adzuna import AdzunaClient, RateLimitExceeded
from workhunter.models import SearchCriteria
from workhunter.filtering import Engine

def main():
    parser = argparse.ArgumentParser(description="WorkHunter PoC - Job Search Helper")
    parser.add_argument("--keywords", type=str, required=True, help="Job keywords")
    parser.add_argument("--location", type=str, required=True, help="Location (e.g., postcode or town)")
    parser.add_argument("--distance", type=int, default=10, help="Distance in miles")
    parser.add_argument("--salary-min", type=float, help="Minimum salary")
    parser.add_argument("--results-per-page", type=int, default=20, help="Results per page")
    parser.add_argument("--page", type=int, default=1, help="Page number")
    parser.add_argument("--target-count", type=int, help="Target number of filtered results")
    
    args = parser.parse_args()
    
    criteria = SearchCriteria(
        keywords=args.keywords,
        location=args.location,
        distance=args.distance,
        salary_min=args.salary_min,
        results_per_page=args.results_per_page,
        page=args.page,
        target_count=args.target_count
    )
    
    try:
        client = AdzunaClient()
        engine = Engine(criteria)
        
        all_matches = []
        current_page = criteria.page
        target = criteria.target_count or criteria.results_per_page
        
        while len(all_matches) < target:
            listings = client.search_jobs(criteria)
            
            if not listings and current_page == 1 and any(c.isdigit() for c in criteria.location):
                # Simple fallback: if location looks like a postcode and returns 0, try stripping it
                # or just warn the agent. For PoC, let's try a broader search or just report 0.
                # Actually, many UK postcodes have a town name nearby. 
                # Let's just log that we are trying a broader search if 0 found.
                break 

            filtered = engine.filter_jobs(listings)
            all_matches.extend(filtered)
            
            if len(listings) < criteria.results_per_page or not criteria.target_count:
                break
                
            current_page += 1
            criteria.page = current_page
            
        ranked_listings = engine.rank_jobs(all_matches)
        
        # Limit to target if we over-fetched
        final_list = ranked_listings[:target]
        
        output = [job.model_dump() for job in final_list]
        print(json.dumps(output, indent=2))
        
    except RateLimitExceeded as e:
        print(json.dumps({
            "error": "rate_limit_exceeded",
            "message": str(e),
            "limit_info": e.limit_info
        }), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
