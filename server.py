import random
from rpcserver import RPCServer

class BatallaNavalServer:
    def __init__(self):
        self.salas = {}  # Diccionario para almacenar salas {id_sala: {"jugadores": [], "tableros": {}, "turno": None}}
        self.sala_id = 1  # Contador para generar IDs de salas

    def crear_sala(self, jugador):
        """Crea una nueva sala y añade al jugador."""
        id_sala = f"Sala-{self.sala_id}"
        self.salas[id_sala] = {
            "jugadores": [jugador],
            "tableros": {},
            "turno": None,
            "resultados": [],
            "estado": "esperando"
        }
        self.sala_id += 1
        return id_sala

    def unirse_a_sala(self, jugador):
        """Intenta unir al jugador a una sala disponible."""
        for id_sala, datos in self.salas.items():
            if len(datos["jugadores"]) < 2:
                datos["jugadores"].append(jugador)
                datos["estado"] = "iniciada"
                datos["turno"] = random.choice(datos["jugadores"])
                return id_sala
        return None

    def registrar_tablero(self, id_sala, jugador, tablero):
        """Registra el tablero del jugador en la sala."""
        if id_sala not in self.salas:
            return "Sala no encontrada."
        self.salas[id_sala]["tableros"][jugador] = tablero
        return "Tablero registrado."

    def manejar_ataque(self, id_sala, jugador, posicion):
        """Maneja un ataque en una sala."""
        if id_sala not in self.salas:
            return "Sala no encontrada."

        datos = self.salas[id_sala]
        if datos["turno"] != jugador:
            return "No es tu turno."

        # Encontrar al oponente
        oponente = [j for j in datos["jugadores"] if j != jugador][0]

        # Validar el ataque
        tablero_oponente = datos["tableros"][oponente]
        fila, columna = posicion
        if tablero_oponente[fila][columna] != "~":
            resultado = "Impacto"
            tablero_oponente[fila][columna] = "X"  # Marcar impacto
        else:
            resultado = "Fallo"

        # Registrar el resultado
        datos["resultados"].append({"atacante": jugador, "posicion": posicion, "resultado": resultado})

        # Cambiar turno
        datos["turno"] = oponente
        return f"Resultado del ataque: {resultado}"

    def obtener_resultados(self, id_sala):
        """Devuelve los resultados de la sala."""
        if id_sala not in self.salas:
            return "Sala no encontrada."
        return self.salas[id_sala]["resultados"]

# Inicializar servidor RPC
if __name__ == "__main__":
    server = RPCServer(("0.0.0.0", 9999), BatallaNavalServer())
    print("Servidor de Batalla Naval iniciado...")
    server.serve_forever()
