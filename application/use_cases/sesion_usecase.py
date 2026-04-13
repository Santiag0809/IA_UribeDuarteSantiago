from domain.entities.sesion import Sesion
from datetime import datetime

class SesionUseCase:

    def __init__(self, repo):
        self.repo = repo

    def check_in(self, camper_id, equipo_id):
        s = Sesion(
            camper_id=camper_id,
            equipo_id=equipo_id,
            inicio=str(datetime.now())
        )
        self.repo.save(s)
