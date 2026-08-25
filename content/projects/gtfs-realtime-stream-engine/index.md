description: Event-driven pipeline that decodes raw MBTA GTFS-Realtime vehicle-position protobufs, validates telemetry, and publishes normalized events to Apache Kafka. Enriches telemetry with GTFS stop metadata and uses DuckDB for deduplication, data-quality analysis, and temporal validation.

---

# GTFS-Realtime Stream Engine

[< Back Home](/)

[< Projects](/projects)

A real-time transit telemetry pipeline that decodes MBTA GTFS-Realtime feeds, validates vehicle position data, and streams normalized events through Apache Kafka for downstream analytics.

## Overview

The GTFS-Realtime Stream Engine is an event-driven pipeline that consumes raw GTFS-Realtime protobuf data from the MBTA (Massachusetts Bay Transportation Authority) vehicle positions feed. It decodes the binary protobuf messages, validates telemetry integrity, and publishes clean normalized events to Kafka topics for consumption by analytics and monitoring systems.

The pipeline is built in two stages: a TypeScript ingestion service that handles decoding, validation, and Kafka publishing, and a Python analytics engine using DuckDB that performs deduplication, data-quality analysis, and temporal validation on the captured stream.

## Architecture

```
MBTA GTFS-Realtime Feed
       |
       v
+-----------------------+
|  INPUT                |
|  Protobuf Decoder     |
|  (TypeScript)         |
|  gtfs-realtime-       |
|  bindings             |
+-----------------------+
       |
       v
+-----------------------+
|  PROCESSING           |
|  Telemetry Validator  |
|  - coordinate bounds  |
|  - finite checks      |
|  - timestamp parse    |
|  - vehicle ID present |
+-----------------------+
       |
       v
+-----------------------+
|  STREAMING            |
|  Kafka Producer       |
|  raw.vehicle-positions|
|  4 partitions         |
|  KRaft mode           |
|  keyed by vehicle ID  |
+-----------------------+
       |
       v
+-----------------------+
|  ANALYTICS            |
|  DuckDB               |
|  - deduplication      |
|  - data quality       |
|  - temporal validation|
|  - stop matching      |
+-----------------------+
```

## Key Components

### Protobuf Decoding

Uses the official `gtfs-realtime-bindings` library to decode raw GTFS-Realtime binary data into structured JavaScript objects. The decoder handles the `FeedMessage` envelope and extracts the `entity` array, which may contain `VehiclePosition`, `TripUpdate`, and `Alert` message types.

The decoder is tested against a real captured MBTA feed fixture and rejects garbage input with a thrown error rather than silently returning junk.

### Telemetry Validation

Validates incoming telemetry against sanity checks before publishing:

- Position coordinate bounds (latitude/longitude within valid geographical ranges)
- Numeric finiteness checks (rejects NaN, undefined, null coordinates)
- Timestamp parseability (must produce a valid Date)
- Vehicle ID presence (entities without a vehicle ID are skipped and counted)

The validator does not check speed or heading plausibility — those fields are often absent in the MBTA feed and are not reliable enough to gate on.

### Kafka Publishing

Normalized JSON events are published to the `raw.vehicle-positions` Kafka topic with the vehicle ID as the message key (partitioning by vehicle). Each message includes:

- The validated telemetry fields (vehicle ID, trip ID, route ID, location, timestamp, bearing, speed, stop fields, status)
- `agency id` set to "mbta" (fixed for now; multi-agency support is future work)
- `ingested at` timestamp for freshness tracking

The producer is configured with idempotency enabled. Topic creation with 4 partitions is handled automatically on startup.

### DuckDB Analytics

The analytics engine consumes the Kafka stream and performs offline analysis:

- **Deduplication** on `(vehicle ID, timestamp)` — 22.4% of raw pings are duplicates (same vehicle, same timestamp), which MongoDB's unique index would reject at write time anyway
- **Data quality** — null rate analysis by route, `current status` distribution, field completeness
- **Temporal validation** — gap analysis between consecutive pings per vehicle, silent-vehicle detection
- **Stop matching** — 99.5% of pings already carry a `stop ID` from the MBTA feed; the remaining 0.5% concentrate in Shuttle-Generic routes with no schedule data

## Problems Solved

### Data validation

The MBTA feed contains entities without positions, without vehicle IDs, and with unparseable timestamps. The validator filters these out and counts them, so the pipeline publishes only telemetry that can be used downstream.

### Duplicate events

22.4% of captured pings are duplicates — the same vehicle reporting the same timestamp multiple times within a single 15-second poll cycle. Deduplication on `(vehicle ID, timestamp)` before analysis prevents these from creating false zero-second gaps.

### Temporal consistency

Gap analysis between consecutive pings per vehicle reveals the real update frequency. The median gap is ~16 seconds, p99 is 62 seconds (after excluding a 10-minute infrastructure incident). A silent-vehicle threshold of 77 seconds (p99 + one poll interval) detects genuinely disconnected vehicles while accounting for the poll cycle itself.

### Stale telemetry

A 10-minute system-wide incident (17:17 to 17:27 local) was identified through clustering analysis — multiple unrelated vehicles showing large gaps in the same minute window. The incident window was excluded from the baseline, reducing contaminated gaps from 12,107 to 1,808 clean entries.

### Spatial validation

Position coordinates are checked against valid latitude/longitude bounds. Entities with coordinates outside [-90, 90] / [-180, 180] are rejected.

### Enrichment

99.5% of pings carry a `stop ID` directly from the MBTA feed. A direct join against GTFS-static `stops.txt` provides stop names and coordinates with no inference required. The remaining 0.5% of null-stop pings concentrate entirely in Shuttle-Generic routes with no schedule data.

### Streaming delivery

Kafka decouples the ingestion service from downstream consumers. The producer is idempotent, topics are created automatically, and the vehicle ID is used as the message key for partition affinity.

## Engineering Decisions

### Why protobuf

The MBTA feed is a binary GTFS-Realtime protobuf stream. Using the official `gtfs-realtime-bindings` library avoids hand-writing a decoder and gives correct parsing of the `FeedMessage` schema, including `VehiclePosition`, `TripUpdate`, and `Alert` entity types.

### Why Kafka

Kafka provides durable, ordered event storage with consumer group semantics. The ingestion service publishes once and any number of downstream consumers (analytics, monitoring, API) can read independently. The 4-partition topic with vehicle-ID partitioning keeps each vehicle's events co-located.

### Why GTFS static data is needed

GTFS-Realtime provides vehicle positions and trip references but not stop names, coordinates, or route short names. Joining against GTFS-static `stops.txt` and `routes.txt` turns opaque IDs into human-readable, geographically-grounded data. Without this enrichment, the telemetry is just a stream of coordinates with no context.

### Why DuckDB

DuckDB handles the analytical queries (deduplication, gap analysis, distribution statistics, joins against GTFS-static CSVs) directly on the captured data without needing a full database server. It's used in Jupyter notebooks for exploration and baseline derivation.

### How validation works

The validator checks each entity for: a present vehicle object, a present position with finite numeric coordinates within geographical bounds, a parseable timestamp, and a present vehicle ID. Entities failing any check are skipped and counted. Optional fields (bearing, speed, stop sequence, stop ID, status) are stored as null when absent rather than causing the entity to be skipped.

### How deduplication and temporal analysis work

Deduplication uses `DISTINCT ON (vehicle ID, timestamp)` in DuckDB, keeping the most recent ingest of each duplicate pair. Gap analysis uses `LAG()` partitioned by vehicle to compute the time delta between consecutive pings. Silent vehicles are detected by comparing each vehicle's gap against a threshold derived from the p99 of movement-only gaps plus one poll interval.

## Metrics

24,000 pings captured from Kafka (representative sample spanning at least two full poll cycles).

- **22.4% duplication rate** — same vehicle, same timestamp reported multiple times within a poll cycle
- **Median gap between pings:** 16 seconds
- **p99 gap (movement only, incident excluded):** 62 seconds
- **Silent-vehicle threshold:** 77 seconds (p99 + 15s poll interval)
- **p95 feed latency:** ~46 seconds (MBTA reported timestamp to ingestion time)
- **99.5% stop ID coverage** — direct from MBTA feed, no inference needed
- **0.03% backwards stop-sequence jumps** — 6 instances out of 18,530 consecutive same-trip observations
- **10-minute infrastructure incident excluded** — reduced contaminated gaps from 12,107 to 1,808 clean baseline entries

## Testing

The ingestion service includes a Vitest test suite covering:

- Protobuf decoding correctness (real fixture + synthetic messages + garbage rejection)
- Validation rule enforcement (coordinate bounds, NaN, undefined, missing vehicle ID, missing timestamp)
- Kafka producer behavior (message shape, keys, agency ID injection, timestamp formatting, error propagation)
- Poll cycle wiring (fetch, decode, validate, publish, failure propagation, logging)
- Polling loop behavior (consecutive failure counting, backoff computation, recovery detection, alert threshold)

## Technology Stack

**Ingestion & decoding:** TypeScript, Node.js

**Stream transport:** Apache Kafka (KRaft mode, 4 partitions)

**Analytics:** DuckDB, Python, Pandas, Jupyter

**Containerization:** Docker, Docker Compose

**Testing:** Vitest

**Protocol:** GTFS-Realtime protobuf, GTFS-static CSV

## Repository

[github.com/EderGtz/GTFS-Realtime-Stream-Engine](https://github.com/EderGtz/GTFS-Realtime-Stream-Engine)
