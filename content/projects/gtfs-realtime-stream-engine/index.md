# GTFS-Realtime Stream Engine

[< Back Home](/)

[< Projects](/projects)

A real-time transit telemetry pipeline that decodes MBTA GTFS-Realtime feeds, validates vehicle position data, and streams normalized events through Apache Kafka for downstream analytics.

## Overview

The GTFS-Realtime Stream Engine is an event-driven pipeline that consumes raw GTFS-Realtime protobuf data from the MBTA (Massachusetts Bay Transportation Authority) vehicle positions feed. It decodes the protobuf messages, validates telemetry integrity, enriches the data with GTFS stop metadata and static schedule references, and publishes clean normalized events to Kafka topics for consumption by analytics and monitoring systems.

## Architecture

```
MBTA GTFS-Realtime Feed
        |
        v
+-----------------------------+
|  Protobuf Decoder           |
|  (TypeScript —             |
|   gtfs-realtime-bindings)  |
+-----------------------------+
        |
        v
+-----------------------------+
|  Telemetry Validator        |
|  (checksum, monotonicity,  |
|   freshness checks)         |
+-----------------------------+
        |
        v
+-----------------------------+
|  Enricher                   |
|  (GTFS-Static stop lookup,  |
|   trip metadata)            |
+-----------------------------+
        |
        v
+-----------------------------+
|  Kafka Producer             |
|  (normalized JSON events    |
|   -> topic)                 |
+-----------------------------+
        |
        v
+-----------------------------+
|  DuckDB Analytics           |
|  (deduplication, data-      |
|   quality, temporal val)    |
+-----------------------------+
```

## Key Components

### Protobuf Decoding

Uses the official `gtfs-realtime-bindings` library to decode raw GTFS-Realtime binary data into structured JavaScript objects. Handles `VehiclePosition`, `TripUpdate`, and `Alert` message types.

### Telemetry Validation

Validates incoming telemetry against sanity checks:

- Position coordinate bounds (latitude/longitude within service area)
- Speed and heading plausibility
- Timestamp monotonicity (no backward clock jumps)
- Record freshness (stale vehicles flagged and filtered)

### Enrichment

Joins vehicle telemetry against GTFS-Static reference data:

- Stop IDs → stop names and geospatial coordinates
- Route IDs → route short names and types
- Trip IDs → scheduled service patterns

### Kafka Publishing

Normalized JSON events are published to Kafka topics with schema-compatible keys. Supports multiple topic strategies (raw, validated, enriched) for different consumer needs.

### DuckDB Analytics

Uses DuckDB for offline analysis of the telemetry stream:

- Deduplication of repeated position updates
- Data-quality metrics (completeness, freshness, accuracy)
- Temporal validation (route adherence, schedule deviation)

## Technology Stack

**Ingestion & decoding:** TypeScript, Node.js

**Stream transport:** Apache Kafka

**Analytics:** DuckDB, Python

**Containerization:** Docker, Docker Compose

**Testing:** Vitest

## Testing

The project includes a comprehensive Vitest test suite covering:

- Protobuf decoding correctness
- Validation rule enforcement
- Kafka producer/consumer integration
- Polling and topic setup logic

## Repository

[github.com/EderGtz/GTFS-Realtime-Stream-Engine](https://github.com/EderGtz/GTFS-Realtime-Stream-Engine)
