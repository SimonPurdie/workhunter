# Application Method Guide

## Purpose

Determine how the user should apply for the job and provide clear, actionable instructions. The goal is advisory - tell the user exactly what they need to do, not to automate the application itself.

## Process

1. Use web_fetch to retrieve the job posting at the `redirect_url`
2. Analyze the page to determine the application method
3. Extract any specific requirements or instructions
4. Write clear, step-by-step guidance for the user

## Common Application Methods

### Direct Email Applications
**Indicators:**
- Email address listed on the page
- Instructions like "Send CV to..."
- "Email your application to..."

**What to extract:**
- Email address to send to
- Any specific requirements (subject line format, file formats, what to include)
- Deadline if mentioned

### Online Application Portals
**Indicators:**
- "Apply Now" button that leads to a form
- Links to company career sites
- Third-party platforms (Workday, Greenhouse, Lever, etc.)

**What to note:**
- Platform name if identifiable (helps user know what to expect)
- Whether account creation is required
- Any unusual requirements mentioned (portfolios, assessments, etc.)

### Application Aggregator Systems
**Indicators:**
- "Apply on Adzuna" or similar
- Forms embedded in the job board page
- Quick apply buttons

**What to note:**
- Whether it's a one-click application or requires information entry
- What information is typically needed

### Hybrid Methods
**Indicators:**
- "Email CV and apply through our portal"
- Multiple methods mentioned

**What to do:**
- List all methods
- Note if one seems preferred or if both are required

## What to Check For

- **Deadlines** - Application closing dates
- **Required documents** - CV, cover letter, portfolio, references, etc.
- **Specific instructions** - Subject line formats, file naming, what to include in the body
- **Contact person** - If a specific person is named
- **Accessibility issues** - If the application method seems broken or unclear

## Output Format

```markdown
# Application Instructions: [Job Title] at [Company]

## Method
[Email / Online Portal / Aggregator / Hybrid]

## Steps
1. [First step]
2. [Second step]
3. [Continue...]

## Requirements
- [Required document 1]
- [Required document 2]

## Important Details
- Deadline: [Date or "Not specified"]
- Contact: [Email/person or "Not specified"]
- Notes: [Any other relevant information]

## Recommendations
[Any advice about how to approach this particular application]
```

## Quality Guidelines

**Good instructions:**
- Are specific and actionable
- List exact steps in order
- Note any potential issues or complications
- Mention what documents/information the user needs to prepare

**Poor instructions:**
- Are vague ("apply through their website")
- Miss important requirements
- Don't warn about unusual steps (account creation, assessments)
- Assume the user knows platform-specific conventions

## Platform-Specific Notes

### Workday
- Requires account creation
- Often lengthy with many fields
- Sometimes asks for full work history dates

### Greenhouse
- Usually straightforward
- May allow uploading multiple documents
- Often has optional demographic questions

### Email Applications
- Suggest professional subject line format
- Note whether cover letter should be in body or attached
- Remind about file naming conventions

## If Information is Missing

If you cannot determine the application method:
- Document what you tried
- Note any issues with the page (broken links, unclear instructions)
- Suggest the user contact the company directly for clarification
- Provide any partial information you did find

## Example Output

```markdown
# Application Instructions: Senior Data Analyst at DataCorp

## Method
Email Application

## Steps
1. Prepare your CV as a PDF (they specifically request PDF format)
2. Write a cover letter addressing why you're interested in DataCorp's analytics platform work
3. Email both documents to recruitment@datacorp.com
4. Use subject line: "Application: Senior Data Analyst - [Your Name]"

## Requirements
- CV (PDF)
- Cover letter (PDF or in email body)
- They mention "please include examples of SQL work" - consider adding a brief portfolio link or examples

## Important Details
- Deadline: January 31, 2026
- Contact: recruitment@datacorp.com
- Notes: They mention reviewing applications on a rolling basis, so earlier is better

## Recommendations
Since this is an email application, you have flexibility in how you present yourself. Consider putting the cover letter in the email body for immediate visibility, with CV attached. Their job posting emphasizes "clear communication" so a well-written email makes a good first impression.
```