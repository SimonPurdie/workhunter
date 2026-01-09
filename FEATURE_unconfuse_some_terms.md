# Refactor Specification: Operation "Role Dossier"

## 1. Structural Migration

* **Rename Directory**: Move all contents from `scripts/` to `modules/`.
* **Rename applications**: Rename `workspace/applications/` to `workspace/roles/`.
* **Purpose**: To clarify that these are modular environment components and to remove software-confusing "application" terminology.

## 2. Global Terminology Mapping

Scan all `*.md` files, docstrings, and comments for the replaced terms, and implement sensible changes.