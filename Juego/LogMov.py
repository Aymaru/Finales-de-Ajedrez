from Juego.Tipos import EstadosLog
from Juego.Tipos import Pieza

class LogMov:

    def __init__(self,movimiento):
        self.movimiento = movimiento
        self.log_movimiento = ""

        ## Para implementar retroceder
        ## self.es_captura = True/False
        ## self.es_enrroque = True/False
        ## self.enrroque_largo = True/False
        ## self.es_coronamiento = True/False
        ## self.pieza_capturada = Pieza IMG
        ## self.pieza_coronada

    def escribir_movimiento(self,tablero):
        pieza_inicial = tablero.get_pieza(self.movimiento.casilla_inicial)
        pieza_objetivo = tablero.get_pieza(self.movimiento.casilla_objetivo)
        str_posicion_inicial = self.movimiento.casilla_inicial.get_posicion_tablero_str()
        str_posicion_objetivo = self.movimiento.casilla_objetivo.get_posicion_tablero_str()
        if pieza_inicial == Pieza.PEON:
            self.log_movimiento = "Peon "
        elif pieza_inicial == Pieza.CABALLO:
            self.log_movimiento = "Caballo " + str_posicion_inicial + " "
        elif pieza_inicial == Pieza.ALFIL:
            self.log_movimiento = "Alfil " + str_posicion_inicial + " "
        elif pieza_inicial == Pieza.TORRE:
            self.log_movimiento = "Torre " + str_posicion_inicial + " "
        elif pieza_inicial == Pieza.DAMA:
            self.log_movimiento = "Dama " + str_posicion_inicial + " "
        elif pieza_inicial == Pieza.REY:
            self.log_movimiento = "Rey " + str_posicion_inicial + " "

        if pieza_objetivo == Pieza.PEON:
            self.log_movimiento = self.log_movimiento + "captura peon de " + str_posicion_objetivo
        elif pieza_objetivo == Pieza.CABALLO:
            self.log_movimiento = self.log_movimiento + "captura caballo de " + str_posicion_objetivo
        elif pieza_objetivo == Pieza.ALFIL:
            self.log_movimiento = self.log_movimiento + "captura alfil de " + str_posicion_objetivo
        elif pieza_objetivo == Pieza.TORRE:
            self.log_movimiento = self.log_movimiento + "captura torre de " + str_posicion_objetivo
        elif pieza_objetivo == Pieza.DAMA:
            self.log_movimiento = self.log_movimiento + "captura dama de " + str_posicion_objetivo
        else:
            self.log_movimiento = self.log_movimiento + "--> " + str_posicion_objetivo

        return
    
    def escribir_estado(self,estado):
        if estado == EstadosLog.JAQUE:
            self.log_movimiento = self.log_movimiento + " JAQUE!"
        elif estado == EstadosLog.JAQUEMATE:
            self.log_movimiento = self.log_movimiento + " JAQUE MATE!"
        elif estado == EstadosLog.TABLAS:
            self.log_movimiento = self.log_movimiento + " TABLAS!"
        return