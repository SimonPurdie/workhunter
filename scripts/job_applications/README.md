# Application Assistance Module

This module guides agents through the job application process. Unlike other modules, this is primarily **documentation-driven** - agents use their existing capabilities (web_search, web_fetch, file reading) to complete tasks following structured workflows.

## Purpose

Assist the user in applying to jobs by:
1. Researching companies to understand context and culture
2. Determining the application method and providing clear instructions
3. Reviewing the user's CV and suggesting relevant modifications
4. Drafting cover letters and application emails where appropriate

## Workflow Overview

### Input
Jobs to apply for are located in `workspace/applications/queue/`. They will be in the form of one or more JSON files that contain one or more Job records.
Job Record structure:
- `title` - Job title
- `company` - Company name
- `location` - Job location
- `redirect_url` - Link to the job posting
- `description` - Job description or summary
- `salary_min` / `salary_max` - Salary range (may be null)

### Process
For each job in the queue, complete these steps in order:

1. **Company Research** - Investigate the company to gather context for the application
   - See `docs/research.md` for detailed guidance
   
2. **Application Method Analysis** - Visit the job posting and determine how to apply
   - See `docs/application_method.md` for detailed guidance

3. **CV Review** - Compare the user's CV (in `userprofile/`) against job requirements
   - See `docs/cv_review.md` for detailed guidance

4. **Draft Materials** - Create cover letter and/or email as appropriate
   - See `docs/materials.md` for detailed guidance

### Output
Create a complete application package in `workspace/applications/job-YYYYMMDD-#/`:

```
workspace/applications/job-20260109-1/
├── job.json                    # Original job details
├── research.md                 # Company research findings
├── application_instructions.md # How to apply
├── cv_suggestions.md          # Recommended CV modifications
└── draft_materials.md         # Cover letter/email drafts
```

Use the date format YYYYMMDD and auto-increment the counter if multiple applications are processed on the same day.

### Completion
Once the application package is complete:
1. Inform the user that the package is ready for review
2. Move the job file from `queue/` to `completed/` to avoid reprocessing

## Task Completion Checklist

An application assistance task is complete when:
- [ ] Company research has been conducted and documented
- [ ] Application method has been determined with clear instructions
- [ ] CV has been reviewed with specific, actionable suggestions
- [ ] Draft materials have been created (if applicable for the application method)
- [ ] All outputs are bundled in a single dated folder
- [ ] The user has been notified that the package is ready for review

## Notes for Agents

- Use your judgment about depth - some steps may require more investigation than others
- If information is unavailable (e.g., company is very small/private), document what you tried and what you couldn't find
- Always prioritize actionable, specific advice over generic observations
- The user will review everything before actually applying, so err on the side of providing more context rather than less
- Consult the detailed guidance docs for each phase to ensure quality and consistency