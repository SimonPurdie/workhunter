# workhunter

An AI-native environment providing modular components for job hunting tasks. Each module is self-documenting and designed to be discovered and used by agentic AI systems.

## Philosophy

**Self-Contained Modules**: Each module lives in its own directory with complete documentation. Modules are independent and can be understood in isolation.

**Documentation is Interface**: AI agents discover capabilities by reading documentation within each module directory. Docs describe purpose, inputs, outputs, and usage.

**Separation Over DRY**: Modules are kept separate even if it means some code duplication. This maintains clarity and reduces coupling. The only shared elements are type definitions that form contracts between modules.

## Structure

```
workhunter/
├── README.md           # This file
├── userprofile/        # relevant details about the user
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

## Adding New Modules

Create a new directory under `modules/` with:
- Complete implementation
- `README.md` explaining purpose, usage, inputs, and outputs
- Any module-specific dependencies or configuration
- Put any helper modules that aren't meant to be executed directly in a lib/ subdirectory.

Keep modules independent. Shared type definitions go in `shared/types.py`.
