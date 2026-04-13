from dataclasses import dataclass, asdict

@dataclass
class Sesion:
    camper_id: str
    equipo_id: str
    inicio: str
    fin: str = None

    def to_dict(self):
        return asdict(self)
