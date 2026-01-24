# Refactoring Proposal: Aligning workhunter with IKEA Specification

This document outlines the discrepancies between the current `workhunter` project structure and the `IKEA.md` specification, and proposes specific actions to resolve them.

## 1. Directory & Naming Discrepancies

The following table maps current resources to their IKEA-compliant counterparts.

| Resource Type | Current Name | IKEA Spec Name | Action |
| :--- | :--- | :--- | :--- |
| **Output Directory** | `workspace/` | `work/` | Rename directory. Update paths in code and documentation. |
| **Shared Information** | `userprofile/` | `context/` | Rename directory. Update references in code and documentation. |
| **Shared Contracts** | `shared/` | `shared_formats/` | Rename directory. Update Python imports and documentation. |
| **Module Assets** | `lib/` | `components/` | Rename subdirectory within modules. Update imports and documentation. |
| **Module Docs** | `README.md` | `INSTRUCTIONS.md` | Rename files. Update internal and external links. |

Note: Every file/directory restructuring operation must be accompanied by a comprehensive search and update of all affected references across the entire codebase and documentation set.

## 2. Root README Updates

The root `README.md` will be rewritten to:

1. Follow the structure defined in `TEMPLATE-README.md`.
2. Reflect the new directory structure (`work/`, `context/`, `shared_formats/`).
3. Include the "For AI Agents" section referencing `IKEA.md`.

## 3. Implementation Plan

### A. File System Operations

Use `git mv` where possible to preserve history.

1. **Root Directories:**

    ```bash
    git mv workspace work
    git mv userprofile context
    git mv shared shared_formats
    ```

2. **Module Internals:**

    ```bash
    git mv modules/job_search/lib modules/job_search/components
    git mv modules/job_search/README.md modules/job_search/INSTRUCTIONS.md
    git mv modules/job_applications/README.md modules/job_applications/INSTRUCTIONS.md
    ```

### B. Code and Documentation Updates

All changes below require updating both executable code and relevant documentation files (e.g., Markdown, docstrings, comments).

1. **`modules/job_search/job_search.py` and related docs**:
    * Update import: `from shared.types` -> `from shared_formats.types`
    * Update import: `from lib` -> `from components`
    * Update sys.path: `... / "lib"` -> `... / "components"`

2. **`modules/job_applications/claim_job.py` and related docs**:
    * Update constants:
        * `QUEUE_DIR`: `... / "workspace" / ...` -> `... / "work" / ...`
        * `APPS_DIR`: `... / "workspace" / ...` -> `... / "work" / ...`

3. **Global Documentation Audit**:
    * Search all `.md` files for legacy paths (`workspace/`, `userprofile/`, `shared/`) and update them to the new IKEA-compliant names.
    * Update any internal cross-references to `README.md` files that have been renamed to `INSTRUCTIONS.md`.
