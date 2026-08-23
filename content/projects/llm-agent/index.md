# LLM-Agent — Autonomous AI Code Agent CLI

[< Back Home](/)

[< Projects](/projects)

A command-line agent that leverages Google's Gemini model with function-calling capabilities to autonomously read, write, and execute files on a local filesystem — a self-contained AI coding assistant.

## Overview

LLM-Agent is a CLI-based autonomous agent that bridges the gap between large language models and real filesystem operations. It uses Gemini's function-calling (tool-use) API to let the model decide which actions to take — reading files, writing code, running shell commands — within a sandboxed working directory.

## Architecture

The agent operates in an iterative loop:

```
User Prompt
    |
    v
+---------------------------+
|  Gemini API (tool-       |
|  calling / function-      |
|  calling enabled)         |
+---------------------------+
    |
    v
+---------------------------+
|  Tool Dispatcher          |
|  routes read/write/       |
|  execute requests         |
+---------------------------+
    |
    v
+---------------------------+
|  Sandbox Filesystem       |
|  working-directory        |
|  isolation                |
+---------------------------+
    |
    v
+---------------------------+
|  Loop Controller          |
|  iteration limits,        |
|  stop conditions          |
+---------------------------+
```

Each iteration:

1. The model receives the user's prompt plus the results of previous tool calls.
2. The model selects a tool to call (read file, write file, execute command, etc.) with structured arguments.
3. The dispatcher executes the tool in the sandbox and returns the result.
4. The loop continues until the model signals completion or the iteration limit is reached.

## Key Features

### Function-Calling Integration

Uses Gemini's native function-calling (tools) API so the model can request structured actions with typed parameters — file paths, content, shell commands — rather than producing free-form text that must be parsed.

### Tool Dispatch

A registry of available tools the model can invoke:

- **Read file** — retrieve file contents from the sandbox
- **Write file** — create or overwrite files with model-provided content
- **Execute command** — run shell commands within the working directory
- **List directory** — inspect the sandbox filesystem

### Sandbox Isolation

All file operations are confined to a configurable working directory. The agent cannot escape the sandbox, preventing accidental or malicious access to files outside the project scope.

### Iteration Limits

A configurable maximum number of iterations prevents runaway agent loops. When the limit is reached, the agent stops and reports what it accomplished.

### Interactive & Scriptable Mode

Can run interactively (prompt → agent → response) or in scripted mode for batch tasks.

## Technology Stack

**LLM:** Google Gemini (function-calling API)

**Language:** Python

**Shell glue:** Bash

**Version control:** Git

## Use Cases

- Automated code generation and file scaffolding from natural-language prompts
- Exploratory codebase analysis ("read these files and summarize")
- Self-contained task execution where the model plans and executes steps autonomously
- Prototyping agentic workflows before committing to heavier frameworks

## Repository

[github.com/EderGtz/LLM-Agent](https://github.com/EderGtz/LLM-Agent)
