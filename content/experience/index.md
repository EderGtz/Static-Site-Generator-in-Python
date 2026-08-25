---
description: Professional experience — Odoo ↔ TikTok Shop bidirectional synchronization and SAT tax blacklist ETL pipeline.
---

# Professional Experience

[< Back Home](/)

Backend engineering work concentrated on systems where data moves between services and correctness matters — event-driven pipelines, bidirectional synchronization, and high-volume ETL.

The experience below is from a seven-month backend and integration internship at Wayakna. These are the threads I'd point to first — not because they're the longest, but because they're where the trade-offs were real and the numbers were measured.

---

## Odoo ↔ TikTok Shop — Bidirectional Inventory Synchronization

_Wayakna · Backend & Integration Engineer (Internship) · Jan–Jul 2026_

Built the integration layer that keeps Odoo ERP inventory consistent with TikTok Shop stock on the other side. The hard part isn't moving data — it's making sure the two systems don't fight each other when both are trying to update the same record.

### Problem

Two inventory systems of record, both able to update the same stock count, with no natural source of truth. Odoo updates when warehouse work happens. TikTok Shop updates when a customer buys. Each side needs to see the other's changes without overwriting them.

### Architecture

```
     ┌─────────┐         ┌──────────────────┐         ┌────────────┐
     │ Odoo    │◀───────▶│  Integration     │◀───────▶│ TikTok Shop│
     │ ERP     │         │  Layer           │         │            │
     │inventory│         │  Kafka · HMAC-   │         │ inventory  │
     │ source  │         │  SHA256 · retries│         │ consumer   │
     └─────────┘         └──────────────────┘         └────────────┘
```

The integration layer sits between the two systems. TikTok Shop pushes real-time update events into Kafka; the layer consumes them, validates them, and applies them to Odoo. The reverse direction — Odoo changes flowing back to TikTok — uses a separate polling path.

### Engineering challenges

* **HMAC-SHA256 signature verification** on every inbound payload — the integration rejects payloads whose signatures don't match, before any business logic runs.
* **Bidirectional race conditions** — both systems can update the same SKU at roughly the same time. Resolved with a convergence strategy that prioritizes inbound polling (TikTok → Odoo) over outbound stock pushes (Odoo → TikTok), so the side with fresher real-time data wins.
* **Warehouse cross-referencing** — inventory is matched to the correct warehouse using isolated per-client execution loops. A single API failure in one client's warehouse path does not halt global sync for the others.
* **Diff-based change detection** — records are compared before being sent, so unchanged inventory doesn't generate unnecessary API calls.
* **MongoDB TTL cache** — a persistent cache with a TTL reduces repeated lookups to the same inventory records.
* **Retry with exponential backoff** — a generic HTTP retry utility handles 429 and 5xx responses without manual intervention.

### Result

A synchronization layer that runs continuously across multiple clients and warehouses, with cryptographic verification on every payload and a convergence strategy that keeps the two inventory systems from fighting each other.

---

## Stream-Based ETL — SAT Tax Blacklist

_Wayakna · Backend & Integration Engineer (Internship)_

A stream-based ETL pipeline processing SAT tax blacklist records from compressed archives — reading, transforming, validating, and loading into MongoDB without holding the whole dataset in memory.

### Pipeline

```
SOURCE DATA ──→ EXTRACTION ──→ TRANSFORMATION ──→ VALIDATION ──→ LOAD
                                                        │
                                                        ▼
                                                  MongoDB · TTL cache
```

Records come from compressed archives, are extracted and transformed in streams, validated before loading, and written into MongoDB. The pipeline is deliberately memory-conscious: it processes records in streams rather than loading the full dataset, which is what keeps the peak footprint bounded across the full run.

### Measured results

```
500K+ records processed     6,348 records/sec      51 MB peak memory
─────────────────────────     ──────────────────      ─────────────────
SAT tax blacklist,          measured throughput     footprint across
compressed archives,        under standard load    the full 500K+
end-to-end pipeline                                  record run
```

### What the numbers represent

* **500K+ records** — total records processed end-to-end through the pipeline, from compressed archive to MongoDB.
* **6,348 records/sec** — measured throughput under standard load, not a synthetic benchmark.
* **51 MB peak memory** — peak memory footprint across the full 500K+ record run, measured while the pipeline was running against real archive data.

### Why it matters

The pipeline demonstrates that a high-volume ETL job doesn't need to hold its entire input in memory. Stream processing, diff-based change detection, and a MongoDB TTL cache together keep memory bounded while still processing the full dataset end-to-end.
