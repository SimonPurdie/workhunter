# Instructions for AI Agents

This project provides a programmatic interface for job search tasks. You should use the provided CLI to discover, filter, and rank job listings.

## Usage

Run the search using `uv run python main.py`. The output is **always structured JSON**.

### CLI Arguments

| Argument | Description | Required | Default |
| :--- | :--- | :--- | :--- |
| `--keywords` | Job titles or skills (e.g., "Data Analyst") | Yes | - |
| `--location` | Town, city, or UK postcode | Yes | - |
| `--salary-min` | Minimum annual salary (GBP) | No | - |
| `--distance` | Search radius in miles | No | 10 |
| `--results-per-page` | Number of raw results to fetch | No | 20 |
| `--target-count` | Fetch until N filtered results found (auto-pagination) | No | - |
| `--page` | Start at specific page | No | 1 |

### Example Command

```bash
uv run python main.py --keywords "Data Analyst" --location "Reading" --salary-min 40000
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
