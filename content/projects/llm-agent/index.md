---

description: CLI agent leveraging Gemini's function-calling API to autonomously read, write, and execute files on a local filesystem — an experimental CLI coding agent.

---

# LLM Code Agent CLI

[< Back Home](/)

[< Projects](/projects)

A command-line agent that leverages Google's Gemini model with function-calling capabilities to autonomously read, write, and execute files on a local filesystem — an experimental CLI coding agent.

## Overview

LLM-Agent is a CLI-based autonomous agent that bridges the gap between large language models and real filesystem operations. It uses Gemini's function-calling (tool-use) API to let the model decide which actions to take — reading files, writing code, running shell commands — within a sandboxed working directory.

The agent operates in an iterative loop: it receives a task, calls Gemini's API to select a tool, executes the tool in the sandbox, feeds the result back, and repeats until the model signals completion or an iteration cap is reached.

## Architecture

The agent operates in an iterative loop:

```
User Prompt
    |
    v
+-----------------------+
|  LLM                  |
|  Gemini API           |
|  function-calling     |
|  enabled              |
|  memory of prior      |
|  tool results         |
+-----------------------+
    |
    v
+-----------------------+
|  Tool Selection       |
|  read / write /       |
|  execute / list       |
+-----------------------+
    |
    v
+-----------------------+
|  Sandbox Execution    |
|  working-directory    |
|  isolation            |
|  read file            |
|  write file           |
|  run command          |
|  list directory       |
+-----------------------+
    |
    v
+-----------------------+
|  Result + prior       |
|  context              |
+-----------------------+
    |
    feedback loop -->
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

### Interactive and Scriptable Mode

Can run interactively (prompt, agent, response) or in scripted mode for batch tasks.

## Interesting Engineering Constraints

### Runaway execution

Without an iteration cap, an agent loop could run indefinitely — the model might keep calling tools in a cycle that never converges. The configurable iteration limit is the primary safeguard: when the cap is reached, the agent stops and reports what it accomplished rather than continuing silently.

### Filesystem boundaries

The sandbox is a working-directory isolation, not a full container or virtual machine. The agent is confined to a configurable directory for file operations, but the constraints are enforced in application code rather than by an external sandboxing layer. This is sufficient for a CLI tool operating on a local workspace, but it is not a security boundary for untrusted models or adversarial prompts.

### Tool failures

When a tool fails — a file does not exist, a command returns a non-zero exit code, the working directory is inaccessible — the error is returned to the model as the tool result. The model sees the failure and can decide to try a different approach, but the agent does not have built-in recovery logic beyond what the model itself generates.

### Context management

Each iteration appends the tool result to the conversation history. Over many iterations, the context grows. The agent does not implement summarization or context pruning — the full history of tool calls and results is passed back to the model each iteration. For long-running tasks this becomes a practical limit, but for the typical scoped task (read a few files, write some code, run a command) it is not a constraint.

### No autonomous goal decomposition

The agent does not break a user's task into subtasks on its own. It executes one tool at a time based on what the model selects. If the task requires multiple dependent steps, the model must handle the sequencing through the iterative loop — selecting a tool, seeing the result, then selecting the next tool.

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
