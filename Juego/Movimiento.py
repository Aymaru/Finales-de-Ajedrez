from Juego import Posicion

class Movimiento:

    def __init__(self,casilla_inicial,casilla_objetivo):
        self.casilla_inicial = casilla_inicial
        self.casilla_objetivo = casilla_objetivo
    
    def equals(self,movimiento):
        return self.casilla_inicial.equals(movimiento.casilla_inicial) and self.casilla_objetivo.equals(movimiento.casilla_objetivo)

    def imprimir(self):
        print("Casilla Inicial -> Fila: %s, Columna: %s | Casilla Objetivo -> Fila: %s, Columna: %s" % (str(self.casilla_inicial.fila),str(self.casilla_inicial.columna),str(self.casilla_objetivo.fila),str(self.casilla_objetivo.columna)))
