# Job Search Helper Scripts — PoC Spec

## **Objective**

Enable an autonomous agent (coding agent / AI assistant) to perform **arbitrary job search tasks** for Data Analyst roles in the UK South region. Tasks include discovering, filtering, ranking — all via programmatic interfaces without brittle browser scraping.

---

## **Scope**

1. **Job Discovery**

   * Query job listing APIs (official or aggregator) for specified roles.
   * Support search by:

     * **Keywords** (e.g., “Data Analyst”, “Business Intelligence Analyst”)
     * **Location** (e.g., from a given UK postcode, return jobs only within a given distance)
     * **Filters** (salary range, remote/hybrid, company size)
   * Retrieve structured job data (title, company, location, salary, description, URL, posting date).

2. **Job Filtering & Ranking**

   * Filter results based on:

     * Role specificity (exclude unrelated titles)
     * Location proximity within UK South
     * Salary thresholds / contract type
   * Rank results by relevance, freshness, or custom scoring function.

---

## **Data Sources**

* **Primary:** Adzuna UK API (job search, regional filtering)
* **Secondary:** Aggregator APIs (Mantiks, DevITjobs), optional open feeds

---

## **PoC Workflow**

1. **Agent issues search task**: “Find Data Analyst roles in South East UK, salary > £40k.”
2. **Job Discovery Module** queries API(s) → returns raw listings.
3. **Filtering Module** applies agent-defined criteria → produces refined list.
4. **Agent evaluates results** and optionally requests additional iterations (e.g., adjust filters, expand location, refine keywords).

---

## **Requirements**

* Must be **modular**, agent-callable, and **API-driven**.
* Must support **structured, machine-readable outputs** (JSON or similar).
* Should be **scalable for periodic queries** and capable of handling multiple role/location combinations.
* Must avoid direct scraping of sites to maintain compliance.

---

## **Success Criteria for PoC**

1. Agent can search for UK South Data Analyst roles using keywords and location filters.
2. Filtered, ranked job list is returned in structured format.
3. All modules callable in isolation and composable into arbitrary job-search workflows.

---

This PoC spec defines a **minimal, modular framework** where an AI agent can orchestrate job hunting autonomously without violating site terms, while keeping outputs structured and actionable.

