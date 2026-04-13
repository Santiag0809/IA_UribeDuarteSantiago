def menu(equipo_uc, sesion_uc):
    while True:
        print("""
1. Crear equipo
2. Listar equipos
3. Check-in
0. Salir
        """)

        op = input("> ")

        if op == "1":
            eid = input("ID: ")
            desc = input("Desc: ")
            equipo_uc.crear_equipo(eid, desc)

        elif op == "2":
            for e in equipo_uc.listar():
                print(e)

        elif op == "3":
            c = input("Camper: ")
            e = input("Equipo: ")
            sesion_uc.check_in(c, e)

        elif op == "0":
            break
