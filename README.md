# workhunter

An AI-native environment providing modular components for job hunting tasks. Each module is self-documenting and designed to be discovered and used by agentic AI systems.

## Philosophy

**Self-Contained Modules**: Each module lives in its own directory with complete documentation. Modules are independent and can be understood in isolation.

**Documentation is Interface**: AI agents discover capabilities by reading documentation within each module directory. Docs describe purpose, inputs, outputs, and usage.

**Separation Over DRY**: Modules are kept separate even if it means some code duplication. This maintains clarity and reduces coupling. The only shared elements are type definitions that form contracts between modules.

## Structure

```filesystem
workhunter/
├── README.md
├── pyproject.toml      # uses uv for environment management
├── userprofile/        # *IMPORTANT* Details about the user which are relevant to job hunting activities
├── shared/
│   └── types.py        # Pydantic models (shared contracts)
└── modules/
    └── job_search/     # Each module in its own directory
        ├── README.md   # How to use this module
        ├── *.py        # Implementation
        └── lib/        # non-entry point modules
```

## For AI Agents

1. List `modules/` to see available capabilities
2. Read the `README.md` in each module directory for complete documentation
3. Check `shared/types.py` for input/output schemas
4. Execute modules as documented
5. Do NOT modify project files or the environment unless explicitly instructed.
6. Prefix all Python commands with uv run (e.g., uv run python script.py)

## Adding New Modules

Create a new directory under `modules/` with:

- Complete implementation
- `README.md` explaining purpose, usage, inputs, and outputs
- Any module-specific dependencies or configuration
- Put any helper components that aren't meant to be executed directly in a lib/ subdirectory.

Keep modules independent. Shared type definitions go in `shared/types.py`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
