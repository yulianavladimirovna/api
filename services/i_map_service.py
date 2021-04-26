from abc import ABC, abstractmethod


class IMapService(ABC):
    @abstractmethod
    def get_map(self, longitude, latitude, zoom, pt, l):
        pass
