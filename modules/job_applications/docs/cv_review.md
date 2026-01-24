# CV Review Guide

## Purpose

Compare the user's CV against the job requirements and provide specific, actionable suggestions for modifications. The goal is advisory - suggest changes the user might want to consider, not to rewrite the CV.

## Important Context

**You are advising, not deciding.** LLMs can be perceptive about CV optimization but also make poor suggestions. Frame everything as recommendations the user should evaluate.

## Process

1. Read the user's current CV from `context/`
2. Analyze the job description for key requirements, skills, and keywords
3. Identify gaps, matches, and opportunities for better alignment
4. Provide specific, actionable suggestions

## What to Analyze

### Skills Alignment
- Which required skills are on the CV?
- Which are missing but the user likely has?
- Which should be emphasized more prominently?
- Are there skill synonyms to consider? (e.g., "data visualization" vs "Tableau/PowerBI")

### Experience Relevance
- Which roles/projects are most relevant to this position?
- Should certain achievements be highlighted more?
- Are there quantifiable results that match what the job seeks?

### Keywords for ATS
- Does the CV include the key terms from the job description?
- Are there important industry terms or technologies mentioned in the posting?
- Are qualifications/certifications mentioned that the user has?

### Formatting and Emphasis
- Is the most relevant information prominently placed?
- Could section ordering be improved for this application?
- Are there minor wording changes that would strengthen alignment?

## Types of Suggestions

### High-Priority Suggestions
Things that significantly improve the match:
- Adding missing but relevant skills the user clearly has
- Re-emphasizing experience that directly matches the role
- Including keywords for critical requirements

### Nice-to-Have Suggestions
Things that might strengthen the application:
- Minor rewordings for better alignment
- Adjusting emphasis on certain projects
- Adding context to existing items

### Questions to Consider
When you're not sure if something applies:
- "Do you have experience with [tool mentioned in posting]?"
- "The role mentions [skill] - is this something from your [project] work?"

## What NOT to Suggest

- Don't suggest fabricating experience or skills
- Don't suggest major CV rewrites (formatting changes, complete restructuring)
- Don't suggest removing experience to "make room" unless it's clearly irrelevant
- Don't suggest generic improvements unrelated to this specific job
- Don't assume the user lacks something just because it's not on their CV

## Output Format

```markdown
# CV Review: [Job Title] at [Company]

## Overall Assessment
[2-3 sentences on how well the current CV matches this role]

## High-Priority Suggestions
### [Suggestion Category]
**Current:** [What the CV currently shows]
**Suggestion:** [Specific change to consider]
**Rationale:** [Why this would help for this role]

[Repeat for each high-priority item]

## Nice-to-Have Improvements
- [Suggestion 1 with brief rationale]
- [Suggestion 2 with brief rationale]

## Keywords to Consider Adding
[If naturally appropriate and accurate]
- [Keyword 1]: [Where it could fit]
- [Keyword 2]: [Where it could fit]

## Questions for You
- [Question 1]
- [Question 2]

## What's Already Strong
[Acknowledge what already matches well - this helps the user feel confident]
- [Strength 1]
- [Strength 2]
```

## Quality Guidelines

**Good suggestions:**
- Are specific ("Add 'SQL' to your skills section" not "Emphasize technical skills")
- Explain why the change helps
- Reference specific parts of the job description
- Acknowledge when you're uncertain
- Recognize what's already working

**Poor suggestions:**
- Are vague ("Make it more relevant")
- Don't explain the rationale
- Suggest things that aren't accurate to the user's experience
- Ignore what's already strong
- Recommend wholesale changes

## Example Suggestions

**Good:**
```
### Technical Skills Placement
**Current:** Python and SQL are mentioned in a project description
**Suggestion:** Add a "Technical Skills" section near the top that lists: Python, SQL, Excel, Tableau
**Rationale:** The job posting lists these as "required technical skills" and uses these exact terms. Having them prominently placed helps both ATS scanning and human reviewers quickly confirm you meet requirements.
```

**Poor:**
```
### Skills
You should emphasize your technical abilities more to match what they're looking for.
```

## Balancing Honesty and Optimization

The CV should always accurately represent the user's experience. The goal is to:
- Frame existing experience in ways that highlight relevance
- Include skills the user actually has but may have understated
- Use terminology that matches the job posting when it's accurate

It's NOT to:
- Exaggerate capabilities
- Add skills the user doesn't have
- Misrepresent the nature or scope of past work

When in doubt, phrase as a question: "Do you have experience with [X]? If so, consider adding it because..."

## Remember

You're helping the user present their genuine qualifications effectively, not helping them pretend to be someone they're not. The best CV suggestions make the user's real strengths more visible to the employer.