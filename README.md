# workhunter

## Purpose

An AI-native environment providing modular components for job hunting tasks. Each module is self-documenting and designed to be discovered and used by agentic AI systems.

## Structure

This workspace follows the **IKEA pattern** for organizing documentation and tools for AI agents.
**New here?** Read [IKEA.md](./IKEA.md) to understand how this workspace is structured and why.

```filesystem
workhunter/
├── README.md
├── IKEA.md
├── pyproject.toml      # uses uv for environment management
├── context/            # Shared information (CVs, profile, etc.)
├── shared_formats/     # Shared data rules and types
├── work/               # Outputs from modules
└── modules/
    └── job_search/     # Each module in its own directory
        ├── INSTRUCTIONS.md
        ├── *.py        # Implementation
        └── components/ # Internal module components
```

## Environment

- **Operating System:** Linux (development environment)
- **How to run scripts:** Prefix all Python commands with `uv run` (e.g., `uv run python modules/job_search/job_search.py`)
- **Special requirements:** API keys should be provided in a `.env` file at the root.

## For AI Agents

**Your role:** Execute tasks using existing modules. The workspace structure is maintained by humans.

1. List `modules/` to see available capabilities
2. Read the `INSTRUCTIONS.md` in each module directory for complete documentation
3. Check `shared_formats/types.py` for input/output schemas
4. Execute modules as documented
5. Do NOT modify project files or the environment unless explicitly instructed.

## Shared Information

The `context/` directory contains information that applies across multiple modules:

- User CVs and profile details relevant to job hunting.
- See `context/README.md` for details (if available).

## Working Area

Modules read and write files in the `work/` directory. Check individual module `INSTRUCTIONS.md` to understand what each module expects to find or will produce there.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
