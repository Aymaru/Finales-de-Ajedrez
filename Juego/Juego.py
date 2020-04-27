from Juego import Tablero

class Juego:

    def __init__(self,turno,piezas_iniciales,tipo_de_juego):
        self.turno = turno
        self.J1 = ''
        self.J2 = ''
        self.tipo_de_juego = tipo_de_juego
        self.tablero = Tablero.Tablero()
        self.colocar_piezas_iniciales(piezas_iniciales)
    
    def colocar_piezas_iniciales(self,piezas_iniciales):
        piezas = piezas_iniciales.split(",") ##Esto creo que se debe cambiar por espacios, a como lo pide el profe y cambiar las comas por espacios en los archivos de juego
        piezas_iniciales = []
        for pieza in piezas:
            piezas_iniciales.append(list(pieza))
        self.tablero.colocar_piezas_iniciales(piezas_iniciales)

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
