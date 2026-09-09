# 📜 EdgeSync Runtime Logs & Gossip Traces

This directory contains real-time execution logs and decentralized gossip message traces captured during the operation of the EdgeSync microservices.

---

## 📁 Directory Structure

```text
logs/
└── gossip/
    ├── gossip_central.jsonl    # Gossip events recorded by CENTRAL node (:10000)
    ├── gossip_east.jsonl       # Gossip events recorded by EAST node (:8000)
    └── gossip_west.jsonl       # Gossip events recorded by WEST node (:9000)
```

---

## 🔬 Event Log Format (JSONL)

Each line in `logs/gossip/*.jsonl` is a JSON object representing an isolated network send or receive event during a gossip synchronization round.

### Example: Outgoing Send Event
```json
{
  "timestamp": 1787482032.2003298,
  "region": "EAST",
  "event_type": "SEND",
  "peer": "http://localhost:9000",
  "payload_size_bytes": 81,
  "details": {
    "sent_observations": 0
  }
}
```

### Example: Incoming Receive & State Reconciliation Event
```json
{
  "timestamp": 1787482036.185121,
  "region": "EAST",
  "event_type": "RECEIVE",
  "peer": "CENTRAL",
  "payload_size_bytes": 84,
  "details": {
    "received_obs": 0,
    "new_added": 0,
    "new_avg_eta": 0.0,
    "total_samples": 0
  }
}
```

---

## 📊 Telemetry Fields

| Field | Type | Description |
| :--- | :--- | :--- |
| `timestamp` | `float` | Unix epoch time with microsecond resolution. |
| `region` | `string` | The recording edge region (`EAST`, `WEST`, or `CENTRAL`). |
| `event_type` | `string` | Gossip interaction type (`SEND`, `RECEIVE`, `HEARTBEAT`). |
| `peer` | `string` | URL or region identifier of the counterpart peer node. |
| `payload_size_bytes` | `integer` | Size of the serialized gossip payload transmitted over HTTP. |
| `details` | `object` | Reconciliation details (new observations merged, updated average ETA, sample count). |
