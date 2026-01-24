# IKEA.md

This document is a straightforward blueprint for structuring multitask automation environments.

It describes a lightweight pattern for organising documents and tools, to make workspaces that are simple for humans and agents to understand.

## Core Principles

- **Self-Contained Modules:** Every module contains everything it needs to work.
- **Minimal Shared State:** An agent using one module does not need to know about or interact with other modules.
- **Names Tell You What They Do:** An agent or human should understand the capabilities of the workspace by reading the list of module directories.
- **Documentation First Design**: How a workspace or module functions, what it needs, and what it produces, are defined by its instructions.

## What IKEA is NOT

- **Not Language Specific:** A module might use Python, Rust, Bash, or just be plain language documentation.
- **Not an Orchestrator:** IKEA doesn't say when things happen. It's a way of creating spaces *for* things to happen. It doesn't dictate any path or use case.
- **Not "DRY"**: IKEA favours modularity and portability over code deduplication. A helper should be copied per module if it improves independence.
- **Not a Complete Specification:** IKEA is deliberately minimal. It doesn't prescribe details like output structure or shared format handling. These are the modules' responsibilty.

## Workspace-level documentation

> The **map and guide** for the workspace. Humans and agents use it to orient themselves before exploring individual modules.

In the root of the workspace is the root **README.md** that:

- Links to this document, to orient the agent and set its assumptions and expectations of the environment it is in.
- Explains the purpose of the workspace.
- Explains important features of the environment - are we on Windows? are we on macOS? how do we run scripts / executables?
- Explains how to find global shared information in `./context/`
- Explains how to list capabilities by checking `./modules/` for module names. Modules are discovered by their presence, rather than listed in a registry that requires maintenance.

## Module-level documentation

> The **instructions** for a single module. It defines the contract for that specific task, ensuring an agent knows exactly what to do without needing to see the rest of the workspace.

Inside each directory within `./modules/` is the module's **INSTRUCTIONS.md** that:

- Explains what the module does.
- Details the actions an agent must perform, as part of its contract with the module.
- Defines the requirements for what the agent must produce, and what it has to do with that product - Saving a file to a location in `./work/` or using a helper script that enforces naming, location, format etc.

## Shared formats / contracts

- If modules need to exchange information, we define clear, explicit formats in a shared location. This could be in the form of code-based definitions (e.g. type classes) or just documentation.

## Directory Structure

```filesystem
<workspace root>/
├── README.md             # overview and guide for the whole workspace
├── context/              # optional: shared information
├── shared_formats/       # optional: shared data rules
├── work/                 # outputs from modules
└── modules/
    ├── noun_verber/      # module names are self documenting: what is it for?
    │   ├── INSTRUCTIONS.md
    │   └── components/   # any file that isn't primary documentation or tools
    └── thingamajig_shuffler/
        ├── INSTRUCTIONS.md
        ├── shuffle_thingamajig.script
        ├── output_shuffled_thingamajigs.script
        └── components/
```

## Agent Prompting

One aim of self-documenting workspaces is that prompts can be minimal:

```prompt
Study README.md, then [do the task]
```

Example: `Study README.md, then shuffle 5 thingamajigs`
