from infrastructure.persistence.json_manager import ensure_data

from infrastructure.persistence.repositories.equipo_json_repo import EquipoJSONRepository
from infrastructure.persistence.repositories.sesion_json_repo import SesionJSONRepository

from application.use_cases.equipo_usecase import EquipoUseCase
from application.use_cases.sesion_usecase import SesionUseCase

from interface.cli.menu import menu


def main():
    ensure_data()

    equipo_repo = EquipoJSONRepository()
    sesion_repo = SesionJSONRepository()

    equipo_uc = EquipoUseCase(equipo_repo)
    sesion_uc = SesionUseCase(sesion_repo)

    menu(equipo_uc, sesion_uc)


if __name__ == "__main__":
    main()
