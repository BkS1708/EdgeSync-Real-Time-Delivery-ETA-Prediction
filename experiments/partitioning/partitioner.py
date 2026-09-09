from abc import ABC, abstractmethod

class RegionPartitioner(ABC):
    @abstractmethod
    def get_region(self, lat: float, lon: float) -> str:
        pass

class StaticPartitioner(RegionPartitioner):
    """Original EdgeSync Mumbai coordinate partitioner."""
    def get_region(self, lat: float, lon: float) -> str:
        if lat < 19.05:
            return "CENTRAL"
        elif lon < 72.85:
            return "WEST"
        else:
            return "EAST"

class GridPartitioner(RegionPartitioner):
    """Grid partitioner dividing coordinates into 3 balanced spatial latitude sectors."""
    def __init__(self, lat_min=18.90, lat_max=19.30):
        self.lat_min = lat_min
        self.lat_max = lat_max
        self.lat_step = (lat_max - lat_min) / 3.0

    def get_region(self, lat: float, lon: float) -> str:
        if lat < (self.lat_min + self.lat_step):
            return "CENTRAL"
        elif lat < (self.lat_min + 2 * self.lat_step):
            return "WEST"
        else:
            return "EAST"
