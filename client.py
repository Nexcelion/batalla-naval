import random
from rpcclient import RPCClient

def inicializar_tablero():
    """Crea un tablero vacío."""
    return [["~" for _ in range(10)] for _ in range(10)]

def imprimir_tablero(tablero):
    """Imprime el tablero en consola."""
    print("  " + " ".join([chr(65 + i) for i in range(10)]))
    for i, fila in enumerate(tablero):
        print(f"{i+1:<2} " + " ".join(fila))

def colocar_piezas():
    """Permite al jugador colocar sus piezas."""
    tablero = inicializar_tablero()
    piezas = {"Portaaviones": 5, "Acorazado": 4, "Crucero": 3, "Submarino": 3, "Destructor": 2}
    for nombre, pv in piezas.items():
        while True:
            try:
                print(f"Coloca tu {nombre} ({pv} PV):")
                imprimir_tablero(tablero)
                posicion = input("Ingresa la posición inicial (ejemplo: A1): ").strip().upper()
                if len(posicion) < 2 or not posicion[0].isalpha() or not posicion[1:].isdigit():
                    raise ValueError("Posición no válida.")
                fila = int(posicion[1:]) - 1
                columna = ord(posicion[0]) - 65
                orientacion = input("Orientación (H/V): ").strip().upper()
                if orientacion not in ["H", "V"]:
                    raise ValueError("Orientación no válida.")
                # Validar y colocar la pieza
                for i in range(pv):
                    f, c = (fila, columna + i) if orientacion == "H" else (fila + i, columna)
                    if not (0 <= f < 10 and 0 <= c < 10) or tablero[f][c] != "~":
                        raise ValueError("Posición fuera de rango o ocupada.")
                    tablero[f][c] = nombre[0]
                break
            except Exception as e:
                print(f"Error: {e}. Intenta de nuevo.")
    return tablero

def main():
    client = RPCClient(("127.0.0.1", 9999))
    server = client.get_proxy()
    jugador = input("Ingresa tu nombre: ").strip()

    while True:
        print("\n=== Menú Principal ===")
        print("1. Jugar")
        print("2. Ver resultados")
        print("3. Ayuda")
        print("4. Salir")
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            sala = server.unirse_a_sala(jugador) or server.crear_sala(jugador)
            print(f"Conectado a {sala}. Coloca tus piezas.")
            tablero = colocar_piezas()
            server.registrar_tablero(sala, jugador, tablero)
            print("Esperando al otro jugador...")
            while True:
                turno = server.obtener_turno(sala)
                if turno == jugador:
                    print("Es tu turno.")
                    posicion = input("Ingresa la posición a atacar (ejemplo: A1): ").strip().upper()
                    fila = int(posicion[1:]) - 1
                    columna = ord(posicion[0]) - 65
                    resultado = server.manejar_ataque(sala, jugador, (fila, columna))
                    print(resultado)
                else:
                    print("Esperando el turno del oponente...")
        elif opcion == "2":
            sala = input("Ingresa el ID de la sala: ").strip()
            resultados = server.obtener_resultados(sala)
            print("=== Resultados ===")
            for r in resultados:
                print(f"{r['atacante']} atacó {r['posicion']}: {r['resultado']}")
        elif opcion == "3":
            print("\n=== Ayuda ===")
            print("- Coloca tus piezas en el tablero.")
            print("- Toma turnos para atacar al oponente.")
            print("- Gana quien hunda todas las piezas del oponente.")
        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
