# workhunter

## Purpose

An AI-native environment providing modular components for job hunting tasks. Each module is self-documenting and designed to be discovered and used by agentic AI systems.

## Structure

**IMPORTANT:** Read [IKEA.md](./IKEA.md) to understand how to navigate and use this workspace.

## Environment

- **Operating System:** Linux, macOS, or Windows (all supported)
- **How to run scripts:** Prefix all Python commands with `uv run` (e.g., `uv run python modules/job_search/job_search.py`)
- **Special requirements:** API keys should be provided in a `.env` file at the root.

## For AI Agents

**Your role:** Execute tasks using existing modules. The workspace structure is maintained by humans.

1. List `modules/` to discover capabilities by module name
2. Read the `INSTRUCTIONS.md` in each module directory for complete documentation
3. If you need a new module, missing dependency, or structural change - ask the human user rather than implementing it yourself

## Shared Information

The `context/` directory contains information that applies across multiple modules:

- User CVs and profile details relevant to job hunting.
- See `context/README.md` for details (if available).

## Working Area

Modules read and write files in the `work/` directory. Check individual module `INSTRUCTIONS.md` to understand what each module expects to find or will produce there.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
