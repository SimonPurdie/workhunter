# [Workspace Name]

## Purpose

[One paragraph: What is this workspace for? What work gets done here?]

## Structure

This workspace follows the **IKEA pattern** for organizing documentation and tools for AI agents.
**New here?** Read [IKEA.md](./IKEA.md) to understand how this workspace is structured and why.

## Environment

[Key information agents need to know about this environment:]

- **Operating System:** [e.g., macOS, Windows, Linux]
- **How to run scripts:** [e.g., `bash script.sh`, `python script.py`, `./executable`]
- **Special requirements:** [e.g., "Docker must be running", "API keys in .env file", "requires Python 3.9+"]

## For AI Agents

**Your role:** Execute tasks using existing modules. The workspace structure is maintained by humans.
When working here:

1. List `modules/` to discover capabilities by module name
2. Read a module's README for complete instructions
3. If you need a new module, missing dependency, or structural change - ask the human user rather than implementing it yourself

## Shared Information

The `context/` directory contains information that applies across multiple modules:

- [List key shared docs, or say "See context/README.md for details"]

## Working Area

Modules read and write files in the `work/` directory. Check individual module READMEs to understand what each module expects to find or will produce there.
