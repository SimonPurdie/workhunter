# WorkHunter Quick Reference

Keep this handy while using WorkHunter!

**Windows Users:** This repo was made and tested in Linux, using WSL on Windows. I'd recommend running it in WSL for compatibility if you can, but you can just try running it natively in Windows instead and it *should* be fine?

## Quick Start Checklist

Check SETUP_GUIDE.md for more details on these steps:

- [ ] Git cloned the repo: `git clone https://github.com/SimonPurdie/workhunter.git`
- [ ] Installed UV: https://docs.astral.sh/uv/getting-started/installation/
- [ ] Created `.env` file with Adzuna API keys
- [ ] Ran `uv sync` to install dependencies
- [ ] Added your CV and any other relevant information about you to `context/` folder
- [ ] Launched AI agent (opencode/antigravity/cursor/codex)

## What to Tell the AI Agent

**For job searching:**
- "Study README.md and find me some jobs!"
- "Study README.md to orient yourself. Use the job_search module to find me [job type] jobs in [location] with salary at least £[amount]"
- "Study README.md to get an idea of where you are. Search for [keywords] roles within [X] miles of [postcode]"

Any kind of natural language command should be fine. Some models respond better to different kinds of instructions.

The environment is set up so you should be able to give very minimal hints. The agent should find you appropriate roles based on your CV, and other info you choose to give it in `context/`.

**For job applications:**

Before starting, take one of the jobsearch json files from a job search (they get saved in the work/ folder)
Delete any jobs from it that you don't want to process for application details.
Then put the file in `work/roles/queue/`

- "Study `README.md` and use the applications module to process a job"

**For reviewing results:**
job searches are saved in `work/` as json and markdown files.
job application packs are saved in `work/roles/` with a dedicated folder for each job containing
- application instructions
- cv suggestions
- draft cover letter suggestions
- research about the company
Remember not to take everything the LLM says as being good advice! Think of it as a starting point rather than a finished product.

## File Locations

| What | Where |
|------|-------|
| Your CV | `context/` folder |
| Search results | `work/jobsearch_YYYYMMDD_*.json` |
| Search reports | `work/jobsearch_YYYYMMDD_*.md` |
| Job application packages | `work/roles/YYYYMMDD-N-company/` |


**Reset job tracker (if needed):**
Once an agent has given you a job from a job_search, other agents shouldn't see that job again.
Delete `work/job_search/seen_jobs.json` if you want to start fresh for any reason.

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
