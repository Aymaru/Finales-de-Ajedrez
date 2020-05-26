from enum import Enum

class TipoDeJuego(Enum):
    Jugador_v_Jugador = 1
    Jugador_v_PC = 2
    PC_v_PC = 3

class Turno(Enum):
    BLANCAS = 1,
    NEGRAS = 2


class Estado(Enum):
    VIVO = 1,
    SOLUCIONADO = 2
    
class Pieza(Enum):
    PEON = 1,
    CABALLO = 2,
    ALFIL = 3,
    TORRE = 4,
    DAMA = 5,
    REY = 6,
    VACIO = 0

class Casilla(Enum):
    ATACA = 1,
    DEFIENDE = 2,
    AMENAZADA = 3,
    ATACADA = 4,
    DEFENDIDA = 5,
    ZONA_DEL_REY = 6

class TipoEvaluacion(Enum):
    MATERIAL = 1,
    MOVILIDAD = 2,
    ESTRUCTURA_DE_PEONES = 3,
    ATAQUE_AL_REY = 4

class FaseDeJuego(Enum):
    INICIO = 0,
    DESARROLLO = 1,
    FINAL = 2

class EstructuraDePeon(enum):
    ADELANTADO = 0,
    AISLADO = 1,
    ATRASADO = 2,
    AVANZADO = 3,
    DOBLADO = 4,
    PASADO = 5,
    BLOQUEADO = 6,
    ENCADENADO = 7,

    

