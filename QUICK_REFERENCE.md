# WorkHunter Quick Reference

Keep this handy while using WorkHunter!

**Windows Users:** All commands work on Windows too! Use PowerShell or Command Prompt. The `uv run` commands are the same on all platforms.

## Quick Start Checklist

- [ ] Git cloned the repo: `git clone https://github.com/SimonPurdie/workhunter.git`
- [ ] Installed UV: https://docs.astral.sh/uv/getting-started/installation/
- [ ] Created `.env` file with Adzuna API keys
- [ ] Ran `uv sync` to install dependencies
- [ ] Added CV to `context/` folder
- [ ] Launched AI agent (opencode/cursor/codex)

## Common Commands

### Finding Jobs
```bash
# Basic search
uv run modules/job_search/job_search.py --keywords "Data Analyst" --location "Reading" --salary-min 30000

# With filters
uv run modules/job_search/job_search.py --keywords "Developer" --location "London" --salary-min 40000 --full-time --permanent --days-old 7

# Exclude keywords
uv run modules/job_search/job_search.py --keywords "Analyst" --location "Manchester" --what-exclude "senior lead"
```

### Claiming a Job (for application)
```bash
uv run modules/job_applications/claim_job.py
```

## What to Tell the AI Agent

**For job searching:**
- "Find me [job type] jobs in [location] with salary at least £[amount]"
- "Search for [keywords] roles within [X] miles of [postcode]"
- "Look for [job type] positions posted in the last [X] days"

**For job applications:**
- "Help me apply to the first/second/third job from [date]"
- "Create an application package for job ID [number]"
- "Research the company and draft materials for this role"

**For reviewing results:**
- "Show me yesterday's job search results"
- "Filter the results to only show remote positions"
- "Rank these jobs by best match for my skills"

## Useful Filters

| Filter | Example | What it does |
|--------|---------|--------------|
| `--salary-min` | `--salary-min 30000` | Minimum annual salary (£) |
| `--salary-max` | `--salary-max 50000` | Maximum annual salary (£) |
| `--distance` | `--distance 25` | Search radius in miles |
| `--days-old` | `--days-old 7` | Only jobs posted in last 7 days |
| `--full-time` | `--full-time` | Full-time only |
| `--permanent` | `--permanent` | Permanent contracts only |
| `--contract` | `--contract` | Contract roles only |
| `--what-exclude` | `--what-exclude "senior"` | Exclude keywords |
| `--sort-by` | `--sort-by date` | Sort by date or salary |

## File Locations

| What | Where |
|------|-------|
| Your CV | `context/` folder |
| Search results | `work/jobsearch_YYYYMMDD_*.json` |
| Search reports | `work/jobsearch_YYYYMMDD_*.md` |
| Job application packages | `work/roles/YYYYMMDD-N-company/` |
| API usage tracker | `.adzuna_usage.json` |

## Adzuna Rate Limits

- **25 requests per minute**
- **250 requests per day**
- **1,000 requests per week**
- **2,500 requests per month**

If you hit a limit, wait and try again later.

## Emergency Commands

**Check if setup is correct:**
```bash
# Linux/macOS:
uv run python -c "import sys; print('Python OK')"
ls -la .env  # Should show your .env file exists

# Windows:
uv run python -c "import sys; print('Python OK')"
dir .env  # Should show your .env file exists
```

**Reset job tracker (if needed):**
Delete `work/job_search/seen_jobs.json` to start fresh

**See all module capabilities:**
```bash
# Linux/macOS:
ls modules/

# Windows:
dir modules\
```

## Workflow Reminder

1. **Search** → Tell agent to find jobs with your criteria
2. **Review** → Check the generated markdown report
3. **Select** → Pick jobs you want to apply to
4. **Apply** → Tell agent "help me apply to job [X]"
5. **Review** → Check the application package in `work/roles/`
6. **Personalise** → Edit the AI-drafted materials
7. **Submit** → Apply using the instructions provided

---

**Stuck?** Ask the AI: "How do I use this workspace?" or read the full guide in `SETUP_GUIDE.md`
