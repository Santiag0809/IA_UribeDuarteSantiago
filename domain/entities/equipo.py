from dataclasses import dataclass, asdict

@dataclass
class Equipo:
    id: str
    descripcion: str
    estado: str = "operativo"
    horas_uso: int = 0

    def to_dict(self):
        return asdict(self)
