import sys
import os
import unittest
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import ObservationStore, Observation

class TestGossipProperties(unittest.TestCase):

    def test_idempotence(self):
        """Property: Merging set A into store multiple times must yield constant sample count and average."""
        store = ObservationStore()
        obs = Observation(obs_id="obs-001", eta=25.0).to_dict()

        # First add
        store.add_observation(obs)
        summary1 = store.get_summary()
        self.assertEqual(summary1["samples"], 1)
        self.assertEqual(summary1["avg_eta"], 25.0)

        # Merge exact same observation 10 times
        for _ in range(10):
            store.merge_observations([obs])

        summary10 = store.get_summary()
        # Idempotence Check: Sample count and average MUST remain 1 and 25.0
        self.assertEqual(summary10["samples"], 1)
        self.assertEqual(summary10["avg_eta"], 25.0)

    def test_commutativity(self):
        """Property: Order of merging observations does not affect the final converged state."""
        store_a = ObservationStore()
        store_b = ObservationStore()

        obs1 = Observation(obs_id="obs-101", eta=20.0).to_dict()
        obs2 = Observation(obs_id="obs-102", eta=30.0).to_dict()

        # Order A: obs1 then obs2
        store_a.merge_observations([obs1])
        store_a.merge_observations([obs2])

        # Order B: obs2 then obs1
        store_b.merge_observations([obs2])
        store_b.merge_observations([obs1])

        self.assertEqual(store_a.get_summary()["avg_eta"], store_b.get_summary()["avg_eta"])
        self.assertEqual(store_a.get_summary()["samples"], store_b.get_summary()["samples"])

    def test_associativity(self):
        """Property: (A union B) union C == A union (B union C)."""
        s1 = ObservationStore()
        s2 = ObservationStore()

        o1 = Observation(obs_id="obs-A", eta=15.0).to_dict()
        o2 = Observation(obs_id="obs-B", eta=25.0).to_dict()
        o3 = Observation(obs_id="obs-C", eta=35.0).to_dict()

        # (o1 union o2) union o3
        s1.merge_observations([o1, o2])
        s1.merge_observations([o3])

        # o1 union (o2 union o3)
        s2.merge_observations([o1])
        s2.merge_observations([o2, o3])

        self.assertEqual(s1.get_summary()["avg_eta"], s2.get_summary()["avg_eta"])
        self.assertEqual(s1.get_summary()["samples"], 3)

if __name__ == "__main__":
    unittest.main()
