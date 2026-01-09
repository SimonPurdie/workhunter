# Application Assistance Module

This module guides agents through the job application process. This is primarily **documentation-driven** - agents use their existing capabilities (web_search, web_fetch, file reading) to complete tasks following structured workflows.

## Purpose

Assist the user in applying to jobs by:
1. Researching companies to understand context and culture
2. Determining the application method and providing clear instructions
3. Reviewing the user's CV and suggesting relevant modifications
4. Drafting cover letters and application emails where appropriate

## Workflow Overview

**IMPORTANT:** Agents must claim a single job using the provided helper script. This ensures that multiple agents can work in parallel without overwriting each other's work.

### Step 0: Claim a Job
Run the following script to extract a job from the queue and generate a working directory:

`python scripts/job_applications/claim_job.py`

If the script returns "No jobs found", the process is complete.
If successful, the script will output a `DIRECTORY` path. **This is your workspace for this session.**

### Process
Once a job is claimed and the workspace is created, complete these steps in order inside the provided directory:

1. **Company Research** - Investigate the company to gather context for the application
   - See `docs/research.md` for detailed guidance
   
2. **Application Method Analysis** - Visit the job posting and determine how to apply
   - See `docs/application_method.md` for detailed guidance

3. **CV Review** - Compare the user's CV (in `userprofile/`) against job requirements
   - See `docs/cv_review.md` for detailed guidance

4. **Draft Materials** - Create cover letter and/or email as appropriate
   - See `docs/materials.md` for detailed guidance

### Output Structure
The helper script automatically generates the folder name (e.g., `job-20260109-1`).
Your task is to populate this folder with the required artifacts.

```
workspace/applications/job-20260109-1/
├── job.json                    # Original job details
├── research.md                 # Company research findings
├── application_instructions.md # How to apply
├── cv_suggestions.md          # Recommended CV modifications
└── draft_materials.md         # Cover letter/email drafts
```

### Completion
Once the application package is populated:
1. Double check that all artifacts (research, instructions, cv_suggestions, drafts) exist in the folder.
2. Inform the user that the package is ready for review, referencing the specific folder name.
*(Note: You do not need to move files to a 'completed' folder; the claiming script has already removed the job from the pending queue.)*

## Task Completion Checklist

An application assistance task is complete when:
- [ ] **Job Claimed**: Script run and working directory identified
- [ ] **Research**: Company research has been conducted and documented
- [ ] **Method**: Application method has been determined with clear instructions
- [ ] **CV Review**: CV has been reviewed with specific, actionable suggestions
- [ ] **Drafts**: Draft materials have been created (if applicable for the application method)
- [ ] **Notification**: The user has been notified that the package is ready for review

## Notes for Agents

- Use your judgment about depth - some steps may require more investigation than others
- If information is unavailable (e.g., company is very small/private), document what you tried and what you couldn't find
- Always prioritize actionable, specific advice over generic observations
- Consult the detailed guidance docs for each phase to ensure quality and consistency