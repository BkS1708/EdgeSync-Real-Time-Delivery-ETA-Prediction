import os
import json

class ExperimentConfig:
    def __init__(self, name="default_experiment", random_seed=42):
        self.name = name
        self.random_seed = random_seed
        self.nodes = {
            "EAST": "http://localhost:8000",
            "WEST": "http://localhost:9000",
            "CENTRAL": "http://localhost:10000"
        }
        self.centralized_url = "http://localhost:8000"
        self.hybrid_url = "http://localhost:8000"
        self.results_dir = os.path.join("results", "phase3", self.name)
        os.makedirs(self.results_dir, exist_ok=True)

    def to_dict(self):
        return {
            "name": self.name,
            "random_seed": self.random_seed,
            "nodes": self.nodes,
            "results_dir": self.results_dir
        }

    def save(self, filepath=None):
        path = filepath or os.path.join(self.results_dir, "config.json")
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
