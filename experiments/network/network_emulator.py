import time
import random
import os

NETWORK_PROFILES = {
    "local_edge": {"latency_ms": 1.0, "jitter_ms": 0.2, "loss_rate": 0.0},
    "metro_edge": {"latency_ms": 5.0, "jitter_ms": 1.0, "loss_rate": 0.001},
    "regional": {"latency_ms": 20.0, "jitter_ms": 3.0, "loss_rate": 0.005},
    "degraded": {"latency_ms": 50.0, "jitter_ms": 10.0, "loss_rate": 0.01},
    "high_latency": {"latency_ms": 100.0, "jitter_ms": 20.0, "loss_rate": 0.02},
    "severe": {"latency_ms": 200.0, "jitter_ms": 50.0, "loss_rate": 0.05},
    "ideal": {"latency_ms": 0.0, "jitter_ms": 0.0, "loss_rate": 0.0}
}

class NetworkEmulator:
    def __init__(self, profile_name="ideal"):
        self.set_profile(profile_name)

    def set_profile(self, profile_name):
        if profile_name in NETWORK_PROFILES:
            self.profile = NETWORK_PROFILES[profile_name]
            self.profile_name = profile_name
        else:
            self.profile = NETWORK_PROFILES["ideal"]
            self.profile_name = "ideal"

    def inject_delay(self):
        """Simulates network latency and jitter."""
        base = self.profile["latency_ms"]
        jitter = self.profile["jitter_ms"]
        loss_rate = self.profile["loss_rate"]

        if loss_rate > 0 and random.random() < loss_rate:
            raise ConnectionError(f"Simulated network packet drop (Profile: {self.profile_name}, loss={loss_rate})")

        if base > 0:
            actual_delay_ms = max(0.0, base + random.gauss(0, jitter))
            time.sleep(actual_delay_ms / 1000.0)
            return actual_delay_ms
        return 0.0

    def set_custom_delay(self, latency_ms, jitter_ms=0.0, loss_rate=0.0):
        """Configure a custom latency delay profile."""
        self.profile = {
            "latency_ms": float(latency_ms),
            "jitter_ms": float(jitter_ms),
            "loss_rate": float(loss_rate)
        }
        self.profile_name = f"custom_{latency_ms}ms"

    def inject_custom_delay(self, latency_ms, jitter_ms=0.0, loss_rate=0.0):
        """Directly inject a configured network latency delay on the communication path."""
        if latency_ms > 0:
            if loss_rate > 0 and random.random() < loss_rate:
                raise ConnectionError(f"Simulated network packet drop (latency={latency_ms}, loss={loss_rate})")
            actual_delay_ms = max(0.0, latency_ms + (random.gauss(0, jitter_ms) if jitter_ms > 0 else 0.0))
            time.sleep(actual_delay_ms / 1000.0)
            return actual_delay_ms
        return 0.0

# Singleton instance
global_emulator = NetworkEmulator("ideal")

def set_network_profile(profile_name):
    global_emulator.set_profile(profile_name)
    print(f"[NetworkEmulator] Profile set to: {profile_name}")

def apply_network_delay():
    return global_emulator.inject_delay()

def apply_custom_network_delay(latency_ms, jitter_ms=0.0):
    return global_emulator.inject_custom_delay(latency_ms, jitter_ms)
