# WorkHunter Setup & Usage Guide

A friendly guide to getting started with AI-assisted job hunting. No coding experience required!

## What is WorkHunter?

WorkHunter is a workspace where AI coding agents (like OpenCode, Cursor, or Codex) help you find and apply for jobs. You give the agent simple instructions like "find me data analyst jobs in Manchester", and it does the searching, filtering, and research for you.

## Prerequisites

Before you start, you'll need:

1. **A computer** running Linux, macOS, or **Windows** (all supported!)
2. **Python 3.11 or higher** installed
3. **UV** - a modern Python package manager ([install instructions](https://docs.astral.sh/uv/getting-started/installation/))
4. **An AI coding agent** - one of:
   - **OpenCode** (free, open-source)
   - **Cursor** (free tier available)
   - **GitHub Copilot/Codex** (requires subscription)
   - **Claude Code** (requires subscription)
5. **An Adzuna API account** (free) - for searching job listings

**Windows Users:** Everything works natively on Windows (no WSL required). Just use PowerShell or Command Prompt instead of the bash commands shown below.

## Step 1: Get Your Adzuna API Keys

WorkHunter uses Adzuna to search for jobs. You need free API credentials:

1. Go to [developer.adzuna.com](https://developer.adzuna.com/)
2. Click "Sign Up" and create an account
3. Once logged in, go to your dashboard
4. Create a new app (give it any name you like)
5. Copy your **Application ID** and **Application Key**

You'll use these in the next step.

## Step 2: Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/SimonPurdie/workhunter.git
cd workhunter
```

## Step 3: Set Up Your API Keys

1. In the `workhunter` folder, create a new file called `.env`
2. Open it in any text editor and add:

```
ADZUNA_APP_ID=your_application_id_here
ADZUNA_APP_KEY=your_application_key_here
```

3. Replace `your_application_id_here` and `your_application_key_here` with the keys you got from Adzuna
4. Save the file

## Step 4: Install Dependencies

In the terminal (inside the workhunter folder), run:

```bash
uv sync
```

This downloads all the necessary packages. It might take a minute or two.

## Step 5: Add Your CV/Resume

1. Create a folder called `context`:
   - **Linux/macOS:** `mkdir -p context`
   - **Windows:** `mkdir context` (or just create it in File Explorer)
2. Copy your CV/resume into that folder
3. Name it something clear like `My CV.md` or `Resume.txt`

The AI agent will read this when helping you apply for jobs.

## How to Use WorkHunter

### Starting the AI Agent

Open your AI coding agent in the workhunter folder. For example:

**With OpenCode:**
```bash
opencode
```

**With Cursor:**
Open the workhunter folder in Cursor and start a chat with the AI.

### Basic Workflow

Once the agent is running, give it simple commands:

#### 1. Finding Jobs

Say something like:
> "Find me software developer jobs in London with a minimum salary of £40,000"

The agent will:
- Search for jobs using the job_search module
- Filter and rank results
- Save a curated list to the `work/` folder

#### 2. Applying to Jobs

Once you have jobs saved, say:
> "Help me apply to the first job from yesterday's search"

The agent will:
- Claim that job from the queue
- Research the company
- Review your CV and suggest changes
- Draft application materials (cover letter, email)
- Create a folder in `work/roles/` with everything you need

### Understanding the Folder Structure

```
workhunter/
├── modules/
│   ├── job_search/          # Searches and finds jobs
│   └── job_applications/    # Helps you apply to jobs
├── context/                  # Your CV and personal info
├── work/
│   ├── jobsearch_*.json     # Search results
│   └── roles/               # Application packages for each job
└── .env                      # Your API keys (keep secret!)
```

## Example Commands

Here are some things you can ask the agent to do:

**Search for jobs:**
- "Search for marketing manager roles in Bristol"
- "Find remote data analyst jobs with salary between £30k-£45k"
- "Look for junior developer positions in Manchester posted in the last 7 days"

**Filter and refine:**
- "Show me only full-time permanent positions"
- "Exclude senior or lead roles from the results"
- "Sort by most recent postings"

**Application help:**
- "Research the company for the first job"
- "Review my CV against this job description"
- "Draft a cover letter for this role"
- "Create an application package for job #3"

## Understanding Your Results

After a job search, you'll find files in `work/`:

- `jobsearch_YYYYMMDD_1.json` - The raw job data
- `jobsearch_YYYYMMDD_1.md` - A human-readable report with links

When applying to a job, you'll get a folder like:
```
work/roles/20260124-1-company-name/
├── job.json                    # Job details
├── research.md                 # Company research
├── application_instructions.md # How to apply
├── cv_suggestions.md          # CV tips
└── draft_materials.md         # Cover letter/email drafts
```

## Tips for Success

1. **Be specific** - Tell the agent exactly what you want (salary, location, job type)
2. **Review the results** - Check the markdown reports before applying
3. **Iterate** - If the first search isn't great, try different keywords
4. **Personalise** - Always review and personalise the AI-drafted materials
5. **Track usage** - Adzuna has rate limits (25/min, 250/day). Check `.adzuna_usage.json` if you hit limits

## Troubleshooting

**"uv: command not found"**
→ You need to install UV. See the prerequisites section.

**"No jobs found"**
→ Try broadening your search (larger location radius, fewer filters, different keywords)

**"Rate limit exceeded"**
→ You've hit Adzuna's API limits. Wait a bit and try again.

**The agent doesn't understand my request**
→ Be more specific. Instead of "find jobs", say "find data analyst jobs in Reading with minimum salary £30000"

**Windows-specific issues**
→ On Windows, use `python` or `py` instead of `python3`. UV works the same way on all platforms.

## Next Steps

Once you're comfortable with the basics:

1. Explore different search strategies (different keywords, locations)
2. Customise the context/README.md with your specific job preferences
3. Review and improve the AI-generated application materials
4. Apply for jobs using the prepared packages!

## Getting Help

- Check the module INSTRUCTIONS.md files in `modules/job_search/` and `modules/job_applications/` for detailed technical info
- Look at existing work in `work/roles/` to see examples
- Ask the AI agent: "How do I use this workspace?" - it can read the documentation too!

---

**Remember:** The AI agent is your helper, not a replacement for your judgment. Always review its work before applying to jobs!
