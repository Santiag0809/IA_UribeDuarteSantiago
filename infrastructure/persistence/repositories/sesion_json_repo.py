from infrastructure.persistence.json_manager import read_json, write_json

class SesionJSONRepository:

    FILE = "sesiones.json"

    def save(self, sesion):
        data = read_json(self.FILE)
        data.append(sesion.to_dict())
        write_json(self.FILE, data)
