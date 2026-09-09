# 🧪 EdgeSync Automated Test Suite

This directory contains automated unit and property-based verification tests for the **EdgeSync** distributed system.

---

## 📋 Test Inventory

### 1. `test_units.py` — Algorithmic & Unit Verification
- **Haversine Distance**: Validates great-circle geographical distance calculations between Mumbai GPS coordinates against standard geodetic baselines.
- **Traffic Speed Factors**: Verifies that speed coefficients across traffic modes (`Low`, `Medium`, `High`) scale travel times accurately.
- **Delivery Stage Decomposition**: Validates that total ETA matches:
  $$\text{ETA} = \max(\text{Pickup Time}, \text{Preparation Time}) + \text{Delivery Time}$$
- **Geographic Partitioning**: Asserts that points within Mumbai boundaries resolve unambiguously to `EAST`, `WEST`, or `CENTRAL` regions.

### 2. `test_gossip_properties.py` — Distributed State & CRDT Property Tests
- **CRDT Idempotence**: Verifies that merging the same observation state repeatedly produces identical results:
  $$S \sqcup S = S$$
- **CRDT Commutativity**: Asserts that the order of receiving gossip state from peer nodes does not affect the reconciled state:
  $$S_A \sqcup S_B = S_B \sqcup S_A$$
- **CRDT Associativity**: Asserts that batching and grouping state exchanges yields invariant outcomes:
  $$(S_A \sqcup S_B) \sqcup S_C = S_A \sqcup (S_B \sqcup S_C)$$
- **Vector Clock Monotonicity**: Verifies that logical clock timestamps advance monotonically on local updates and merge operations.

---

## 🚀 Running the Tests

Execute all tests using Python's built-in `unittest` runner:

```bash
python -m unittest discover tests
```

### Verbose Output

To view each individual test execution:
```bash
python -m unittest discover -s tests -v
```

Expected output:
```text
test_haversine_distance (test_units.TestUnits.test_haversine_distance) ... ok
test_eta_calculation (test_units.TestUnits.test_eta_calculation) ... ok
test_geofence_partitioning (test_units.TestUnits.test_geofence_partitioning) ... ok
test_gossip_idempotence (test_gossip_properties.TestGossipProperties.test_gossip_idempotence) ... ok
test_gossip_commutativity (test_gossip_properties.TestGossipProperties.test_gossip_commutativity) ... ok
test_gossip_associativity (test_gossip_properties.TestGossipProperties.test_gossip_associativity) ... ok
test_vector_clock_monotonicity (test_gossip_properties.TestGossipProperties.test_vector_clock_monotonicity) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.002s

OK
```
