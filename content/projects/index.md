---

title: Projects — Eder Gutiérrez

---

# Projects

[< Back Home](/)

A selection of systems, tools, and data projects built to solve concrete engineering problems.

## [GTFS-Realtime Stream Engine](/projects/gtfs-realtime-stream-engine)

**Flagship — Tier 1.** Event-driven pipeline that decodes raw MBTA GTFS-Realtime vehicle-position protobufs, validates telemetry, and publishes normalized events to Apache Kafka. Enriches telemetry with GTFS stop metadata and uses DuckDB for deduplication, data-quality analysis, and temporal validation. Containerized with Docker and covered by Vitest tests for protobuf decoding, validation, polling, Kafka publishing, and topic setup.

**Stack:** TypeScript, Python, Apache Kafka, DuckDB, Docker

[View on GitHub](https://github.com/EderGtz/GTFS-Realtime-Stream-Engine)

---

## [Autonomous AI Code Agent CLI](/projects/llm-agent)

**Tier 2 — Systems and tooling.** CLI agent leveraging Gemini's function-calling API to read, write, and execute files through an iterative tool-calling loop. Implements an iterative agent loop with tool dispatch, working-directory sandboxing, and configurable iteration limits to prevent runaway executions.

**Stack:** Python, LLM APIs, Bash, Git

[View on GitHub](https://github.com/EderGtz/LLM-Agent)

---

## [PyWeaver — Static Site Generator](/projects/ssg)

**Tier 2 — Systems and tooling.** A from-scratch Python static site generator with a node-based HTML engine (Composite Pattern), custom Markdown parsing (block-level + inline syntax), recursive directory generation, and 71 unit tests. Built as part of the Boot.dev backend course to understand how static site generators work internally.

This portfolio is generated with the same SSG.

**Stack:** Python, unittest, Regex

[View on GitHub](https://github.com/EderGtz/SSG)

---

## [CipherHook (OS-Level File Encryption)](/projects/cipherhook)

**Tier 3 — Earlier work.** Earlier work. An OS-level file encryption daemon built in Python. It uses watchdog to react to filesystem events and PyCryptodome to encrypt files using AES-256-EAX, with RSA-2048 used to wrap the symmetric session key.

**Stack:** Python, Watchdog, PyCryptodome, AES-256-EAX, RSA-2048

[View on GitHub](https://github.com/EderGtz/CipherHook-File-Encrypt)

---

## [RecursiveForecast (Python vs. R)](/projects/recursiveForecast)

**Tier 3 — Academic / exploratory.** An analytical project comparing recursive forecasting models implemented in both Python and R. Developed as part of Reto 4 at UVEG, implements the Exponential Smoothing algorithm to predict 2020 values from historical 2015-2019 data across 10 economic indicators.

**Stack:** Python, R, NumPy, Matplotlib, purrr

[View on GitHub](https://github.com/EderGtz/RecursiveForecast---Python-vs.-R)

[View on GitHub](https://github.com/EderGtz/RecursiveForecast---Python-vs.-R)