modules/job_applications/claim_job.py should implement the following functionality:

When claim_job.py creates a new role dossier directory, it currently uses naming pattern:

```job-YYYYMMDD-#```

REQUESTED CHANGE:
Use the 'company' field from the json job record being claimed, using the pattern:

```YYYYMMDD-#-<company>```

Where <company> is **slugified** and abbreviated to 16 characters maximum.

EXAMPLE:
record: {"company": "Technological Solutions Inc."}
output directory name: 20250111-1-technological-so