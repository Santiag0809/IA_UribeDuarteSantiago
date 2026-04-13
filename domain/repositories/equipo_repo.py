from abc import ABC, abstractmethod

class EquipoRepository(ABC):

    @abstractmethod
    def save(self, equipo): pass

    @abstractmethod
    def get_all(self): pass
