# Job Search Module

This script provides a programmatic interface for job search tasks using the Adzuna API. It allows agents to discover, filter, and rank job listings.

## Usage

Run the search using `uv run modules/job_search/job_search.py`. The output is **always structured JSON**.

### CLI Arguments

| Argument | Description | Required | Default |
| :--- | :--- | :--- | :--- |
| `--keywords` | Job titles or skills (e.g., "Data Analyst") | Yes | - |
| `--location` | Town, city, or UK postcode | Yes | - |
| `--salary-min` | Minimum annual salary (GBP) | No | - |
| `--salary-max` | Maximum annual salary (GBP) | No | - |
| `--distance` | Search radius in miles | No | 10 |
| `--results-per-page` | Number of raw results to fetch | No | 20 |
| `--page` | Start at specific page | No | 1 |
| `--target-count` | Fetch until N filtered results found (auto-pagination) | No | - |
| `--sort-by` | Sort server-side: `date` or `salary` | No | - |
| `--what-exclude` | Exclude keywords from results (e.g., "senior") | No | - |
| `--full-time` | Filter to full-time positions only | No | False |
| `--permanent` | Filter to permanent positions only | No | False |
| `--contract` | Filter to contract positions only | No | False |
| `--part-time` | Filter to part-time positions only | No | False |
| `--days-old` | Maximum posting age in days (e.g., 7) | No | - |
| `--page` | Start at specific page | No | 1 |

### Example Command

```bash
uv run modules/job_search/job_search.py --keywords "Data Analyst" --location "Reading" --salary-min 30000
```

### Additional Examples

```bash
# Full-time permanent positions only, sorted by most recent
uv run modules/job_search/job_search.py --keywords "Data Analyst" --location "Reading" --salary-min 30000 --full-time --permanent --sort-by date

# Exclude certain keywords (e.g., exclude senior/lead roles)
uv run modules/job_search/job_search.py --keywords "Data Analyst" --location "Reading" --what-exclude "senior lead manager"

# Jobs posted within last 7 days
uv run modules/job_search/job_search.py --keywords "Data Analyst" --location "Reading" --days-old 7

# Salary range with contract positions
uv run modules/job_search/job_search.py --keywords "Data Scientist" --location "Reading" --salary-min 35000 --salary-max 50000 --contract
```

## Output Format

The output is a JSON array of job objects. Key fields include:
- `id`: Unique job identifier.
- `title`: Job title.
- `company`: Name of the employer.
- `location`: Human-readable location.
- `salary_min` / `salary_max`: Yearly salary range.
- `description`: Snippet of the job description.
- `redirect_url`: Direct link to the listing.

### Error Handling
Errors are returned as JSON to `stderr`:
`{"error": "description of what went wrong"}`

## Rate Limit Management

Adzuna's free tier has strict limits. This tool automatically tracks usage in `.adzuna_usage.json`:
- **Current Limits**: 25/min, 250/day, 1,000/week, 2,500/month.
- **Error Handling**: If exceeded, the script returns a structured JSON error to `stderr`:
  `{"error": "rate_limit_exceeded", "limit_info": {...}}`

## Agent Strategies for Efficiency

1.  **Use `--target-count`**: Instead of scanning pages manually, set `--target-count 5` to let the script handle pagination logic.
2.  **Location Fallback**: The script attempts to fallback if a specific postcode returns 0 results. If you get 0 results, try a broader town name.
3.  **Check Usage**: If you are performing a large batch of tasks, monitor your quota to avoid blocking yourself.
4.  **Result Filtering**: Be aware that the script automatically prevents results being returned that have been served to the user in previous sessions.
5.  **Server-side Filtering**: Use flags like `--full-time`, `--permanent`, `--sort-by`, and `--what-exclude` to reduce data transfer and improve performance. Only use client-side filtering when server-side options are insufficient.
6.  **Date Filtering**: Use `--days-old` to focus on recent postings without needing to manually check dates.

## API Interaction Features

The script interfaces directly with Adzuna's search API and supports the following optimizations:

- **Server-side Filtering**: Contract type and keyword exclusion are handled by Adzuna's API, reducing bandwidth and improving response times
- **Server-side Sorting**: Results can be sorted by `date` or `salary` at the API level
- **Salary Range**: Both minimum and maximum salary bounds can be specified to narrow results
- **JSON Responses**: Explicitly sets `content-type=application/json` for reliable structured output
- **Date-based Filtering**: The `--days-old` parameter filters job postings by age using the `created` timestamp field

The script also implements client-side deduplication using MD5 hashes of job signatures to prevent returning the same role across search sessions.

---

## Agent Task Completion Requirements

You are expected to curate job search results based on user input. Acting as a job scout your role is to:
- Run multiple searches with different keywords/parameters if needed
- Review job descriptions and filter out poor matches
- Identify the best opportunities based on requirements
- Add context or notes explaining why you selected certain jobs

The task is NOT complete until you output curated results to the `work/` directory.

### Required Workflow

```bash
# 1. Run searches (potentially multiple times)
uv run modules/job_search/job_search.py --keywords "Data Analyst" --location "Reading" --salary-min 30000 > raw1.json
uv run modules/job_search/job_search.py --keywords "Business Analyst" --location "Reading" --salary-min 30000 > raw2.json

# 2. Review, filter, and curate results (you can do this programmatically or by analysis)

# 3. Output your curated JSON and save
echo '[{"title": "...", "company": "...", ...}]' | uv run modules/job_search/save_search.py
```

### Curated JSON Output Schema

After your analysis, output a JSON array with this structure:

```json
[
  {
    "title": "Senior Data Analyst",
    "company": "Tech Innovations Ltd",
    "location": "Reading, Berkshire",
    "salary_min": 45000,
    "salary_max": 55000,
    "redirect_url": "https://www.adzuna.co.uk/jobs/details/1234567890",
    "description": "Job description snippet...",
    "agent_notes": "Strong match - emphasizes Python and SQL which align with requirements. Team size is 5-10 analysts."
  }
]
```

**Required fields for each job**:
- `title` (string)
- `company` (string)
- `location` (string)
- `salary_min` (number or null)
- `salary_max` (number or null)
- `redirect_url` (string) - **CRITICAL: Must always be included**
- `description` (string) - Can be a snippet or summary

**Optional but recommended**:
- `agent_notes` (string) - Your reasoning for why this job is a good match

### Saving Your Curated Results

Pipe your final JSON to `save_search.py`:

```bash
# From a file
cat curated_jobs.json | uv run modules/job_search/save_search.py

# Or directly from your script/command
uv run your_curation_script.py | uv run modules/job_search/save_search.py
```

This automatically creates:
- `work/jobsearch_YYYYMMDD_N.json` - Your curated JSON
- `work/jobsearch_YYYYMMDD_N.md` - Human-readable report with ALL job URLs

### Output File Naming

Files follow the pattern: `jobsearch_YYYYMMDD_#`
- Date is automatically added (e.g., `20260108`)
- Counter auto-increments if you run multiple searches per day (e.g., `_1`, `_2`, `_3`)
- The `work/` folder is at the project root for easy access

### Manual Markdown Formatting (Optional)

If you need to format existing JSON separately:

```bash
uv run modules/job_search/components/format_markdown.py < jobs.json > report.md
```

### What Must Be In Your Final Output

Every job in your curated list MUST include:
1. Job title
2. Company name
3. Salary range (even if one bound is null)
4. Location
5. **The `redirect_url` - this is critical**
6. Description or summary

Optional but valuable:
- Your notes on why this job is a good match
- Any concerns or caveats
- Comparison notes if multiple similar positions exist