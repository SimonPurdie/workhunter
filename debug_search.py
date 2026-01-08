from workhunter.discovery.adzuna import AdzunaClient
from workhunter.models import SearchCriteria

client = AdzunaClient()
criteria = SearchCriteria(
    keywords="Data Analyst",
    location="Wallingford",
    distance=15,
    results_per_page=50
)
listings = client.search_jobs(criteria)
print(f"Raw listings found: {len(listings)}")
for l in listings:
    print(f"- {l.title} ({l.company})")
