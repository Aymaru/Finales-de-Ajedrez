from Juego import Tablero
from Juego import Movimiento

class Juego:

    def __init__(self,turno,piezas_iniciales,tipo_de_juego):
        self.turno = turno
        self.J1 = ''
        self.J2 = ''
        self.tipo_de_juego = tipo_de_juego
        self.tablero = Tablero.Tablero()
        self.colocar_piezas_iniciales(piezas_iniciales)
        self.set_movimientos_legales()
        self.casilla_inicial = None
        self.casilla_objetivo = None
    
    def colocar_piezas_iniciales(self,piezas_iniciales):
        piezas = piezas_iniciales.split(",") ##Esto creo que se debe cambiar por espacios, a como lo pide el profe y cambiar las comas por espacios en los archivos de juego
        piezas_iniciales = []
        for pieza in piezas:
            piezas_iniciales.append(list(pieza))
        self.tablero.colocar_piezas_iniciales(piezas_iniciales)

    def set_movimientos_legales(self):
        self.movimientos_legales = self.tablero.obtener_movimientos_legales(self.tablero.generar_posibles_movimientos(),self.turno)

    def print_movimientos_legales(self):
        for movimiento in self.movimientos_legales:
            movimiento.imprimir()

    def set_casilla_inicial(self,posicion):
        self.casilla_inicial = posicion
    
    def set_casilla_objetivo(self,posicion):
        self.casilla_objetivo = posicion

    #def set_movimiento_a_realizar(self,posicion):
    #    self.movimiento_a_realizar = Movimiento.Movimiento(self.casilla_seleccionada,posicion)

    def limpiar_casilla_inicial(self):
        self.casilla_inicial = None
    
    def limpiar_casilla_objetivo(self):
        self.casilla_objetivo = None

    def limpiar_movimiento_a_realizar(self):
       self.movimiento_a_realizar = None

    def mover_pieza(self):
        
        if self.turno == 'B':
            pieza_de_coronamiento = 5
            self.turno = 'N'
        else:
            pieza_de_coronamiento = -5
            self.turno = 'B'
        self.tablero.mover_pieza(self.movimiento_a_realizar,pieza_de_coronamiento)
        self.limpiar_casilla_inicial() 
        self.limpiar_casilla_objetivo()
        self.limpiar_movimiento_a_realizar()
        self.set_movimientos_legales()

    def es_casilla_inicial_permitida(self):
        for movimiento in self.movimientos_legales:
            if(self.casilla_inicial.equals(movimiento.casilla_inicial)):
                return True
        return False

    def es_movimiento_a_realizar_legal(self):
        self.movimiento_a_realizar = Movimiento.Movimiento(self.casilla_inicial,self.casilla_objetivo)
        for movimiento in self.movimientos_legales:
            if (self.movimiento_a_realizar.equals(movimiento)):
                return True
        self.limpiar_movimiento_a_realizar()
        return False

    def turno_to_string(self):
        if self.turno == "B":
            return "Blancas"
        else:
            return "Negras"
    # def iniciar_juego(self):

    #     ##Pendiente el log en archivo log_partida = [log_de_tablero_inicial,log_de_movimientos]
    #     ##log_de_tablero_inicial = copy.deepcopy(tablero)
    #     ##log_de_movimientos = []

    #     while True:
    #         posibles_movimientos = self.tablero.generar_posibles_movimientos()
    #         movimientos_legales = self.tablero.obtener_movimientos_legales(posibles_movimientos,self.turno)
    #         if self.hay_jaque_mate:
    #             print("juego terminado")
    #             break

    #         jaque = self.tablero.hay_jaque(posibles_movimientos,self.turno)
            
    #         if self.turno == 'B':
    #             pieza_de_coronamiento = 5
    #         else:
    #             pieza_de_coronamiento = -5

    #         if self.turno == J1: ## Turno del jugador, espera que el jugador ingrese el movimiento
    #             print("Ingrese la casilla a mover y la casilla donde se mueve, con formato: \ncolumna fila. Ejm (a7)")
    #             posicion_inicial = input("Ingrese la casilla inicial: ")
    #             posicion_destino = input("Ingrese la casilla destino: ")
    #             if not(validar_posicion_real(posicion_inicial) and validar_posicion_real(posicion_destino)):
    #                 print("Error en las posiciones ingresadas")
    #                 continue
                
    #             posicion_inicial = convertir_posicion_real_a_representacion([posicion_inicial[0],posicion_inicial[1]])
    #             posicion_destino = convertir_posicion_real_a_representacion([posicion_destino[0],posicion_destino[1]])
    #             movimiento = [posicion_inicial,posicion_destino]

    #             tablero = mover_pieza(tablero,movimiento,pieza_de_coronamiento)
    #             turno = J2
    #         else:
    #             movimiento = [] ## Obtener movimiento usando minimax
    #             tablero = mover_pieza(tablero,movimiento,pieza_de_coronamiento)
    #             turno = J1          
