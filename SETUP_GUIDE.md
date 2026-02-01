# WorkHunter Setup & Usage Guide

A friendly guide to getting started with AI-assisted job hunting. No coding experience required!

## What is WorkHunter?

WorkHunter is a workspace where AI coding agents (like OpenCode, Antigravity, Cursor, or Codex) help you find and apply for jobs. You give the agent simple instructions like "find me data analyst jobs in Manchester", and it does the searching, filtering, and research for you.

## Prerequisites

Before you start, you'll need:

1. **A computer** running Linux, macOS, or Windows
2. **Python 3.11 or higher** installed
3. **UV** - a modern Python package manager ([install instructions](https://docs.astral.sh/uv/getting-started/installation/))
4. **An AI coding agent** - such as:
   - **OpenCode** (free tier available, open-source)
   - **Google Antigravity** (free tier available)
   - **Cursor** (free tier available)
   - **GitHub Copilot (in VS Code)** (free tier available)
   - **Codex CLI** (included in OpenAI ChatGPT Plus plan - check for free offers!)
   - **Claude Code** (requires subscription)
5. **An Adzuna API account** (free) - for searching job listings

**Windows Users:** Everything *should* work natively on Windows. I'd recommend WSL instead though (Windows Subsystem for Linux). If you use windows natively you'll need to use PowerShell or Command Prompt instead of the bash commands shown below.

## Step 1: Get Your Adzuna API Keys

WorkHunter uses Adzuna to search for jobs. You need free API credentials:

1. Go to [developer.adzuna.com](https://developer.adzuna.com/)
2. Click "Sign Up" and create an account
3. Once logged in, go to your dashboard
4. Create a new app (give it any name you like)
5. Copy your **Application ID** and **Application Key**

You'll use these in the next step.

## Step 2: Clone the Repository

Install Git if you don't have it: https://git-scm.com/

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

1. Copy your CV/resume into the context/ folder. Its best if you can have it in a format that LLMs find easy to read, like markdown.
2. Name it something clear like `My CV.md` or `Resume.txt`
3. Make a file in the folder called `README.md` and enter text in it explaining info about the kind of jobs you want.
   - What locations you want, how far can you travel.
   - What salary you're looking for
   - Do you want remote work? Part time work?

The AI agent will read this when helping you apply for jobs. Think of it as instructions you'd give to a person who was a dedicated Job Scout for you.

## How to Use WorkHunter

### Starting the AI Agent

Open your AI coding agent in the workhunter folder. For example:

**With OpenCode:**
```bash
opencode
```

**With Cursor/Antigravity/VS Code:**
Open the workhunter folder in the IDE and start a chat with the AI

### Basic Workflow

Once the agent is running, ALWAYS tell it to read the README.md so it understands the context of where it is and what kind of job its doing. Then give it simple commands:

#### 1. Finding Jobs

Say something like:
> "Study README.md and find me some jobs"

The agent will:
- Search for jobs using the job_search module
- Filter and rank results
- Save a curated list to the `work/` folder

#### 2. Applying to Jobs

Once you have jobs saved, delete any jobs from the json file that you're not interested in, then put the file in
`work/roles/queue/` (make the folders if they dont exist already)
Then say something like:

> "Read README.md and use the applications module to process a job"

The agent will:
- Claim a job from the queue
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

1. **You can be specific** - Tell the agent exactly what you want (salary, location, job type), or just let it improvise.
2. **Iterate** - If the first search isn't great, try different keywords, or telling the agent how you'd like it done better.
4. **Personalise** - Always review and personalise the AI-drafted materials before applying to jobs with them.

## Troubleshooting

**"uv: command not found"**
→ You need to install UV. See the prerequisites section.

**"No jobs found"**
→ Try broadening your search (larger location radius, fewer filters, different keywords)

**"Rate limit exceeded"**
→ You've hit Adzuna's API limits. Wait a bit and try again.

**The agent doesn't understand my request**
→ Try telling it to read the README.md

**Windows-specific issues**
→ Agents might get confused about commands on Windows. If it seems to be trying to use bash commands that aren't working, try telling it that its in a Windows environment.

## Getting Help

- Check the module INSTRUCTIONS.md files in `modules/job_search/` and `modules/job_applications/` for detailed technical info
- Ask the AI agent: "How do I use this workspace?" - it can read the documentation too!
- If you have difficulty doing any part of setting up the environment, or using the coding agents, try asking a Web LLM for help - ChatGPT, Gemini or Claude. They should be able to help you find instructions for whatever you're having trouble with.
