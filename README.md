# Job Hunt Tools

An AI-native environment providing modular scripts for job hunting tasks. Each script is self-documenting and designed to be discovered and used by agentic AI systems.

## Philosophy

**Self-Contained Modules**: Each script lives in its own directory with complete documentation. Scripts are independent and can be understood in isolation.

**Documentation is Interface**: AI agents discover capabilities by reading documentation within each script directory. Docs describe purpose, inputs, outputs, and usage.

**Separation Over DRY**: Scripts are kept separate even if it means some code duplication. This maintains clarity and reduces coupling. The only shared elements are type definitions that form contracts between scripts.

## Structure

```
job-hunt-tools/
├── README.md           # This file
├── shared/
│   └── types.py        # Pydantic models (shared contracts)
└── scripts/
    └── job_search/     # Each script in its own directory
        ├── README.md   # How to use this script
        └── *.py        # Implementation
```

## For AI Agents

1. List `scripts/` to see available capabilities
2. Read the `README.md` in each script directory for complete documentation
3. Check `shared/types.py` for input/output schemas
4. Execute scripts as documented

## Adding New Scripts

Create a new directory under `scripts/` with:
- Complete implementation
- `README.md` explaining purpose, usage, inputs, and outputs
- Any script-specific dependencies or configuration
- Put any helper modules that aren’t meant to be executed directly in a lib/ subdirectory.

Keep scripts independent. Shared type definitions go in `shared/types.py`.