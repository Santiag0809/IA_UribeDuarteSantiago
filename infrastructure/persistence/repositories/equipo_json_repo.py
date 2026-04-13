from domain.repositories.equipo_repo import EquipoRepository
from infrastructure.persistence.json_manager import read_json, write_json

class EquipoJSONRepository(EquipoRepository):

    FILE = "equipos.json"

    def save(self, equipo):
        data = read_json(self.FILE)
        data.append(equipo.to_dict())
        write_json(self.FILE, data)

    def get_all(self):
        return read_json(self.FILE)
