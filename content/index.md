# Eder Gutiérrez — Backend Developer

![Eder Gutiérrez](images/pp.jpeg)

## Resume

**Eder Gutiérrez — Backend Developer**

1 page, Updated 2026

[Download Resume (PDF)](/resume/Eder_Gutierrez_Resume.pdf)

## Technical Skills

**Languages:** Python, TypeScript, JavaScript, SQL, Bash

**Backend:** Event-Driven Architecture, REST APIs, Stream Processing, ETL Pipelines, OOP

**Infrastructure:** Apache Kafka, RabbitMQ, MongoDB, PostgreSQL, MySQL, Docker, Linux

**Testing & Tools:** Jest (Unit/Integration), Odoo ERP Custom Integrations, GitHub Actions

## Experience

### Wayakna — Backend & Integration Engineer (Internship)

Mérida, Yucatán — Jan 2026 to Jul 2026

- Engineered a bidirectional inventory synchronization system between Odoo ERP and TikTok Shop, implementing HMAC-SHA256 signature verification for cryptographic validation.
- Consumed real-time client updates from multiple Kafka producers and routed payloads to downstream systems based on payload type.
- Architected a stream-based ETL pipeline to process over 500,000 SAT tax blacklist records from compressed archives, achieving a processing speed of 6,348 records/sec with a peak memory footprint of only 51 MB.
- Resolved bidirectional race conditions during cross-system data normalization using a convergence strategy that prioritizes inbound polling over outbound stock pushes, and built a warehouse cross-referencing system with isolated per-client execution loops so single-API failures never halted global synchronization.
- Optimized API resource consumption by implementing diff-based change detection, a persistent MongoDB TTL cache, and a generic HTTP retry utility with exponential backoff for 429/5xx error handling.

## Featured Projects

- [GTFS-Realtime Stream Engine](/projects/gtfs-realtime-stream-engine) — Event-driven pipeline that decodes raw MBTA GTFS-Realtime vehicle-position protobufs, validates telemetry, and publishes normalized events to Apache Kafka. Enriches telemetry with GTFS stop metadata and uses DuckDB for deduplication, data-quality analysis, and temporal validation. Containerized with Docker and covered by Vitest tests.
- [Autonomous AI Code Agent CLI](/projects/llm-agent) — CLI agent leveraging Google's Gemini model with function-calling capabilities to autonomously read, write, and execute files on a local filesystem. Implements an iterative agent loop with tool dispatch, working-directory sandboxing, and configurable iteration limits to prevent runaway executions.
- [Static Site Generator (SSG)](/projects/ssg) — Custom-built Python SSG with a node-based HTML engine using the Composite Pattern, full Markdown parsing (inline + block-level), recursive directory generation, and 71 unit tests. Built from scratch to deeply understand how tools like Jekyll and Hugo operate.

## Education

**B.S. in Software Engineering** (Specialization in Big Data)
Universidad Virtual del Estado de Guanajuato (UVEG) — Coursework completed Jul 2026, degree in progress

Core coursework: Software Engineering, Data Structures, OOP, Database Design (SQL & NoSQL), Computer Networks, AI Fundamentals, Probability & Statistics.

Big Data track: Distributed Computing, Data Analysis, Big Data Administration, and NoSQL Database Systems.

**Backend & Computer Science Engineering path**
Boot.dev — Online Computer Science Academy (2025 - Present)

Distributed Systems & Networking: Pub/Sub Messaging (RabbitMQ), HTTP Servers & Clients (TypeScript), File Servers & CDNs (S3/CloudFront).

Computer Science Core: Advanced OOP & Functional Programming (Python), Algorithms & Data Structures, Docker Containerization, Deep Git Version Control, Linux Systems Administration.

## Contact

- [Contact me](/contact)
- [GitHub](https://github.com/EderGtz)
- [LinkedIn](https://linkedin.com/in/edergutierrezc)


This site was generated with a custom-built [static site generator](https://github.com/EderGtz/SSG) written in Python.
