# Eder Gutiérrez

I design and build backend systems, integrations, and data pipelines where reliability, consistency, and throughput matter. Right now that means Kafka-based event ingestion, GTFS-realtime transit telemetry, bidirectional ERP synchronization, and the pipelines in between.

[View selected work](/projects) · [GitHub](https://github.com/EderGtz) · [Resume](/resume/Eder_Gutierrez_Resume.pdf)

## Selected engineering work

Systems, pipelines, and tools built to solve concrete engineering problems.

**Flagship:** [GTFS Realtime Stream Engine](/projects/gtfs-realtime-stream-engine)

_A real-time transit data pipeline — raw vehicle telemetry → validated, enriched event stream._

Consumes the MBTA's raw binary **GTFS-Realtime VehiclePositions** protobuf feed on a 15-second interval. Decodes the binary payload, validates telemetry integrity, enriches each ping against GTFS-static stop/trip metadata, and publishes normalized JSON events to **Apache Kafka**. Downstream DuckDB analytics perform deduplication, data-quality scoring, and temporal validation of schedule adherence.

```
┌─────────────┐   ┌──────────────────┐   ┌───────────────┐   ┌────────────────┐
│   INPUT     │   │   PROCESSING     │   │   STREAMING   │   │   ANALYTICS    │
├─────────────┤   ├──────────────────┤   ├───────────────┤   ├────────────────┤
│ MBTA Feed   │──→│ Protobuf Decoder │──→│ Kafka Producer│──→│  DuckDB        │
│ .pb payload │   │ gtfs-realtime    │   │ raw.vehicle   │   │  deduplication │
│ 15s poll    │   │ bindings         │   │ -positions    │   │  data quality  │
└─────────────┘   │ TypeScript/Node  │   │ 4 partitions  │   │  temporal val  │
                  └──────────────────┘   │ KRaft mode    │   └────────────────┘
                                         └───────────────┘
```

[TypeScript] [Apache Kafka] [DuckDB] [Protobuf] [GTFS] [Docker] [Vitest]

[Repository](https://github.com/EderGtz/GTFS-Realtime-Stream-Engine)

[Autonomous AI Code Agent](/projects/llm-agent)

_An experimental CLI agent that uses an LLM with tool calling to read, write, and execute code in a sandboxed workspace._

A Python CLI that bridges a large language model to real filesystem operations. The agent receives a task, calls Gemini's function-calling API to decide which tool to invoke, executes the tool in a confined working directory, and feeds the result back into the loop — repeating until the model signals completion or an iteration cap is reached.

```text
USER TASK
     │
     ▼
 ┌───────────────────────────────┐
 │  LLM  Gemini API              │
 │  function-calling enabled     │
 │  polarized loop               │
 │  memory of prior tool results │
 └───────────────┬───────────────┘
                 │ selects tool
                 ▼
        ┌──────────────────┐
        │  TOOL SELECTION  │
        │  read / write /   │
        │  execute          │
        └──────┬───────────┘
               │
               ▼
        ┌────────────────────────┐
        │ SANDBOX EXECUTION      │
        │ working-directory      │
        │ isolation              │
        │ read file · write file │
        │ run command · list dir │
        └──────────┬─────────────┘
                   │
                   ▼
              ┌──────────┐
              │  RESULT  │
              │ + prior  │
              │ context  │
              └────┬─────┘
                   │
        feedback ↺─┘
configurable iteration cap prevents runaway loops
```

[Python] [Gemini API] [Bash] [Git]

[Repository](https://github.com/EderGtz/LLM-Agent)

**From scratch:** [Static Site Generator](/projects/ssg)

*A custom-built Python SSG — written from scratch to understand how tools like Jekyll and Hugo work under the hood.*

Transforms a directory of Markdown files and static assets into a complete HTML website. The entire engine — block parsing, inline conversion, an intermediate TextNode representation, and a Composite-Pattern HTML node tree — was built from the ground up as a learning project. No third-party SSG libraries.

```text
Markdown Files        Block Parser        Inline Converter      TextNode IR       HTML Renderer        HTML output
(content/)           (md-blocks.py)     (md-inline-          (textnode.py)     (htmlnode.py)       (docs/)
                     ┌─────┐             converter.py)                        ┌──────┐
                     │head-│             ┌──────────────┐                    │Leaf- │
                     │ings │             │bold · italic │                    │Node ·│
                     │lists │             │code · links  │                    │Parent│
                     │code  │             │· images      │                    │Node   │
                     │block-│             └──────────────┘                    │recursive
                     │quotes│                                                        │rendering
                     │parags│                                                        └──────┘
                     └──┬───┘
                        │
                        ▼
              recursive directory walk → mirrors source tree
this portfolio is generated by the same SSG
```

[Python] [unittest] [Regex] [Composite Pattern]

[Repository](https://github.com/EderGtz/SSG)

## Professional experience

I'm a backend engineer who got into this through the data side, and ended up somewhere between data engineering and backend systems. I like building the parts of a system that are invisible when they work and obvious when they don't: pipelines, integrations, event streams.

One year of backend and integration work, concentrated on systems where data moves between services and correctness matters. The internship threads below are the work I'd point to first — not because they're the longest, but because they're where the trade-offs were real.

### Odoo ↔ TikTok Shop — Bidirectional Inventory Synchronization

*Wayakna · Backend & Integration Engineer (Internship) · Mérida, Yucatán · Jan–Jul 2026*

Built the integration layer that keeps Odoo ERP inventory consistent with TikTok Shop stock on the other side. The hard part isn't moving data — it's making sure the two systems don't fight each other when both are trying to update the same record.

```text
     ┌─────────┐         ┌──────────────────┐         ┌────────────┐
     │ Odoo    │◀───────▶│  Integration     │◀───────▶│ TikTok Shop│
     │ ERP     │         │  Layer           │         │            │
     │ inventory│        │  Kafka · HMAC-   │        │ inventory  │
     │ source  │        │  SHA256 · retries│        │ sink       │
     └─────────┘         └──────────────────┘         │ consumer   │
                                                       └────────────┘
bidirectional sync · convergence strategy (converges inbound polling over outbound pushes)
HMAC-SHA256 signature verification on every payload
```

* **HMAC-SHA256** signature verification for cryptographic validation of each payload
* Real-time client updates consumed from multiple **Kafka** producers, routed to downstream systems by payload type
* Bidirectional race conditions resolved with a convergence strategy that prioritizes inbound polling over outbound stock pushes
* Warehouse cross-referencing system with isolated per-client execution loops — a single API failure never halts global sync
* Diff-based change detection + persistent **MongoDB** TTL cache to reduce API calls
* Generic HTTP retry utility with exponential backoff for 429 / 5xx handling

### Stream-Based ETL — SAT Tax Blacklist

*Wayakna · Backend & Integration Engineer (Internship)*

A stream-based ETL pipeline processing SAT tax blacklist records from compressed archives — reading, transforming, validating, and loading into MongoDB without holding the whole dataset in memory.

```text
500K+ records processed     6,348 records/sec      51 MB peak memory
─────────────────────────     ──────────────────      ─────────────────
SAT tax blacklist,          measured throughput     footprint across
compressed archives,        under standard load    the full 500K+
end-to-end pipeline                                  record run
```

```text
SOURCE DATA ──→ EXTRACTION ──→ TRANSFORMATION ──→ VALIDATION ──→ LOAD
                                                        │
                                                        ▼
                                                  MongoDB · TTL cache
```

The pipeline is deliberately memory-conscious: it processes records in streams rather than loading the full dataset, which is what keeps the peak footprint at 51 MB across 500K+ records. Diff-based change detection avoids re-sending records that haven't changed, and the MongoDB TTL cache gives repeated lookups a fast path.

## Technical capabilities

Technologies grouped by what I use them for.

Not a proficiency grid. These are the tools that show up in the systems I build — grouped by the role they play.

**Systems**

Apache Kafka · RabbitMQ · Docker · Linux

**Data**

MongoDB · PostgreSQL · SQL

**Backend**

Python · TypeScript · JavaScript · REST APIs · ETL pipelines

**Testing & delivery**

Jest · GitHub Actions · Git · Vitest · unittest

The common thread is event-driven architecture: systems where components communicate through messages rather than direct calls, where failures are expected and handled rather than exceptional, and where correctness under load matters more than speed of first implementation.

## About

Backend engineer. Big Data coursework.

I'm a backend engineer who got into this through the data side — Big Data specialization, distributed computing, NoSQL systems — and ended up somewhere between data engineering and backend systems. I like building the parts of a system that are invisible when they work and obvious when they don't: pipelines, integrations, event streams.

Currently based in Mérida, Yucatán. Degree in progress at UVEG, additional backend/CS work through Boot.dev.

**Education**

**B.S. in Software Engineering** — Big Data specialization
Universidad Virtual del Estado de Guanajuato (UVEG)
Coursework completed Jul 2026 · degree in progress

Core: Software Engineering, Data Structures, OOP, Database Design (SQL & NoSQL), Computer Networks, AI Fundamentals, Probability & Statistics.
Big Data track: Distributed Computing, Data Analysis, Big Data Administration, NoSQL Database Systems.

**Backend & Computer Science Engineering path**
Boot.dev — Online Computer Science Academy · 2025–present

Distributed Systems & Networking: Pub/Sub Messaging (RabbitMQ), HTTP Servers & Clients (TypeScript), File Servers & CDNs (S3/CloudFront).
CS Core: Advanced OOP & Functional Programming (Python), Algorithms & Data Structures, Docker Containerization, Deep Git Version Control, Linux Systems Administration.

## Contact

Currently exploring backend and data engineering opportunities. If your team is working with data pipelines, API integrations, or stream processing, reach out.

[GitHub — EderGtz](https://github.com/EderGtz) · [LinkedIn](https://linkedin.com/in/edergutierrezc) · [Email](mailto:gutierrezeder64@gmail.com) · [Resume](/resume/Eder_Gutierrez_Resume.pdf)

Mérida, Yucatán — Mexico
