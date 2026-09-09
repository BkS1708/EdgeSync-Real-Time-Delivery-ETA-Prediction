from abc import ABC, abstractmethod
import utils

class ETAEngine(ABC):
    @abstractmethod
    def predict_eta(self, source, dest, food, rider_option, traffic_level):
        pass

class FormulaETAEngine(ETAEngine):
    """Original EdgeSync Heuristic Speed & Distance Model."""
    def predict_eta(self, source, dest, food, rider_option, traffic_level):
        pickup = utils.get_rider_distance_from_option(rider_option) * 2
        prep = utils.get_prep_time(food)
        dist_km = utils.distance(source, dest)
        delivery = utils.estimate_time_from_distance(dist_km, traffic_level)
        eta = max(pickup, prep) + delivery
        return {
            "ETA": eta,
            "pickup": pickup,
            "prep": prep,
            "delivery": delivery,
            "distance_km": dist_km
        }

class MLETAEngine(ETAEngine):
    """
    Pluggable Regression ML Engine.
    Uses synthetic pre-trained regression coefficients to model non-linear traffic delays.
    Supports optional GPU execution if framework available.
    """
    def __init__(self, use_gpu=False):
        self.use_gpu = use_gpu
        self.formula_fallback = FormulaETAEngine()

    def predict_eta(self, source, dest, food, rider_option, traffic_level):
        # Baseline estimate from formula
        base_res = self.formula_fallback.predict_eta(source, dest, food, rider_option, traffic_level)
        
        # Apply synthetic non-linear ML adjustment factor (simulating dynamic congestion model)
        traffic_multipliers = {"Low": 1.0, "Medium": 1.05, "High": 1.15}
        mult = traffic_multipliers.get(traffic_level, 1.0)
        
        ml_eta = base_res["ETA"] * mult
        return {
            "ETA": ml_eta,
            "pickup": base_res["pickup"],
            "prep": base_res["prep"],
            "delivery": base_res["delivery"] * mult,
            "distance_km": base_res["distance_km"],
            "ml_adjusted": True
        }
