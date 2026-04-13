from domain.entities.equipo import Equipo

class EquipoUseCase:

    def __init__(self, repo):
        self.repo = repo

    def crear_equipo(self, id, descripcion):
        equipo = Equipo(id=id, descripcion=descripcion)
        self.repo.save(equipo)

    def listar(self):
        return self.repo.get_all()
