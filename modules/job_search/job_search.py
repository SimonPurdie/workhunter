import argparse
import json
import sys
from pathlib import Path

# Add project root and script directory to sys.path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(Path(__file__).parent))

from shared_formats.types import SearchCriteria
from components.adzuna import AdzunaClient, RateLimitExceeded
from components.engine import Engine
import components.job_tracker as job_tracker


def main():
    parser = argparse.ArgumentParser(description="WorkHunter - Job Search Helper")

    parser.add_argument("--keywords", type=str, required=True, help="Job keywords")
    parser.add_argument(
        "--location", type=str, required=True, help="Location (e.g., postcode or town)"
    )
    parser.add_argument("--distance", type=int, default=10, help="Distance in miles")
    parser.add_argument("--salary-min", type=float, help="Minimum salary")
    parser.add_argument("--salary-max", type=float, help="Maximum salary")
    parser.add_argument(
        "--results-per-page", type=int, default=20, help="Results per page"
    )
    parser.add_argument("--page", type=int, default=1, help="Page number")
    parser.add_argument(
        "--target-count", type=int, help="Target number of filtered results"
    )
    parser.add_argument("--sort-by", type=str, help="Sort results: 'date' or 'salary'")
    parser.add_argument("--what-exclude", type=str, help="Exclude keywords from search")
    parser.add_argument(
        "--full-time", action="store_true", help="Full-time positions only"
    )
    parser.add_argument(
        "--permanent", action="store_true", help="Permanent positions only"
    )
    parser.add_argument(
        "--contract", action="store_true", help="Contract positions only"
    )
    parser.add_argument(
        "--part-time", action="store_true", help="Part-time positions only"
    )

    parser.add_argument(
        "--days-old", type=int, help="Maximum age of job posting in days"
    )

    args = parser.parse_args()

    # Load seen hashes at start
    seen_jobs = job_tracker.load_seen_jobs()
    seen_hashes = {j["hash"] for j in seen_jobs}

    criteria = SearchCriteria(
        keywords=args.keywords,
        location=args.location,
        distance=args.distance,
        salary_min=args.salary_min,
        salary_max=args.salary_max,
        results_per_page=args.results_per_page,
        page=args.page,
        target_count=args.target_count,
        sort_by=args.sort_by,
        what_exclude=args.what_exclude,
        full_time=args.full_time,
        permanent=args.permanent,
        contract=args.contract,
        part_time=args.part_time,
        days_old=args.days_old,
    )

    try:
        client = AdzunaClient()
        engine = Engine(criteria)

        all_matches = []
        current_page = criteria.page
        target = criteria.target_count or criteria.results_per_page

        while len(all_matches) < target:
            listings = client.search_jobs(criteria)

            if (
                not listings
                and current_page == 1
                and any(c.isdigit() for c in criteria.location)
            ):
                # Simple fallback: if location looks like a postcode and returns 0, try stripping it
                break

            filtered = engine.filter_jobs(listings)

            # Deduplicate against seen jobs
            final_filtered = []
            for job in filtered:
                job_hash = job_tracker.generate_hash(
                    job.company, job.title, job.location
                )
                if job_hash not in seen_hashes:
                    final_filtered.append(job)
                else:
                    # Optional: log or skip
                    pass

            all_matches.extend(final_filtered)

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
        print(
            json.dumps(
                {
                    "error": "rate_limit_exceeded",
                    "message": str(e),
                    "limit_info": e.limit_info,
                }
            ),
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
