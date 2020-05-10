from Juego import Tablero
from Juego import Movimiento

from GUI import Ajedrez

class Juego:

    def __init__(self,master,turno,jug_1,piezas_iniciales,tipo_de_juego,es_juego_inicial):
        self.master = master
        self.tablero = Tablero.Tablero()

        
        self.J1 = jug_1
        self.J2 = ""
        self.colocar_piezas_iniciales(piezas_iniciales)        
        self.tipo_de_juego = tipo_de_juego
        self.es_juego_inicial = es_juego_inicial
        if self.es_juego_inicial:
            self.turno = 'B'
            self.enrroque_blancas_corto = True
            self.enrroque_blancas_largo = True
            self.enrroque_negras_corto = True
            self.enrroque_negras_largo = True
        else:
            self.turno = turno
            self.enrroque_blancas_corto = False
            self.enrroque_blancas_largo = False
            self.enrroque_negras_corto = False
            self.enrroque_negras_largo = False

        self.movimientos_legales = []
        self.posibles_movimientos = []
        self.posibles_movimientos_blancas = []
        self.posibles_movimientos_negras = []
        
        self.es_jaque = False
        self.jaque_mate = False
        self.es_tablas = False
        self.es_turno_pc = False
        
        
        
        self.casilla_inicial = None
        self.casilla_objetivo = None
        self.movimiento_a_realizar = None

        self.actualizar_estado_de_tablero()
        ##Se instancia la interfaz
        #self.GUI_ajedrez = Ajedrez.Ajedrez(self.master)

    def generar_movimientos_de_enrroque(self):
        if self.turno == 'B':

            if self.enrroque_blancas_corto:
                print("A")
                enrroque_bc = self.tablero.generar_enrroque_blancas_corto(self.posibles_movimientos_negras)
                if enrroque_bc != None:
                    print("A.1")
                    self.movimientos_legales.append(enrroque_bc)
            if self.enrroque_blancas_largo:
                print("B")
                enrroque_bl = self.tablero.generar_enrroque_blancas_largo(self.posibles_movimientos_negras)
                if enrroque_bl != None:
                    print("B.1")
                    self.movimientos_legales.append(enrroque_bl)

        else:

            if self.enrroque_negras_corto:
                print("C")
                enrroque_nc = self.tablero.generar_enrroque_negras_corto(self.posibles_movimientos_blancas)
                if enrroque_nc != None:
                    print("C.1")
                    self.movimientos_legales.append(enrroque_nc)
            if self.enrroque_negras_largo:
                print("D")
                enrroque_nl = self.tablero.generar_enrroque_negras_largo(self.posibles_movimientos_blancas)
                if enrroque_nl != None:
                    print("D.1")
                    self.movimientos_legales.append(enrroque_nl)

    def actualizar_estado_de_tablero(self):
        self.set_posibles_movimientos()
        self.set_movimientos_legales()        
        self.set_posibles_movimientos_blancas()
        self.set_posibles_movimientos_negras()
        self.generar_movimientos_de_enrroque()
        self.actualizar_turno_pc()
        self.set_es_jaque()
        self.set_jaque_mate()
        self.set_es_tablas()

    def actualizar_turno_pc(self):
        if self.tipo_de_juego == 1:
            self.es_turno_pc = False
        elif self.tipo_de_juego == 2:
            if self.turno != self.j1:
                self.es_turno_pc = True
            else:
                self.es_turno_pc = False
        elif self.tipo_de_juego == 3:
            self.es_turno_pc = True

    def disable_enrroque_blancas_corto(self):
        self.enrroque_blancas_corto = False

    def disable_enrroque_blancas_largo(self):
        self.enrroque_blancas_largo = False

    def disable_enrroque_negras_corto(self):
        self.enrroque_negras_corto = False

    def disable_enrroque_negras_largo(self):
        self.enrroque_negras_largo = False

    def set_posibles_movimientos_blancas(self):
        self.posibles_movimientos_blancas = []
        self.posibles_movimientos_blancas = self.tablero.posibles_movimientos_de_blancas(self.posibles_movimientos)

    def set_posibles_movimientos_negras(self):
        self.posibles_movimientos_negras = []
        self.posibles_movimientos_negras = self.tablero.posibles_movimientos_de_negras(self.posibles_movimientos)

    def set_jugadores(self):
        
        if self.J1 == "B":
            self.J2 = "N"
        else:
            self.J2 = "B"
    
    def set_es_jaque(self):
        self.es_jaque = self.tablero.hay_jaque(self.posibles_movimientos,self.turno)

    def set_jaque_mate(self):
        if self.es_jaque and len(self.movimientos_legales) == 0:
            self.jaque_mate = True
        else:
            self.jaque_mate = False

    def set_es_tablas(self):
        if not self.es_jaque and len(self.movimientos_legales) == 0:
            self.es_tablas = True
        else:
            self.es_tablas = False

    def colocar_piezas_iniciales(self,piezas_iniciales):
        piezas = piezas_iniciales.split(",") ##Esto creo que se debe cambiar por espacios, a como lo pide el profe y cambiar las comas por espacios en los archivos de juego
        piezas_iniciales = []
        for pieza in piezas:
            piezas_iniciales.append(list(pieza))
        self.tablero.colocar_piezas_iniciales(piezas_iniciales)

    def set_movimientos_legales(self):
        self.movimientos_legales = []
        self.movimientos_legales = self.tablero.obtener_movimientos_legales(self.posibles_movimientos,self.turno)
        

    def set_posibles_movimientos(self):
        self.posibles_movimientos = []
        self.posibles_movimientos = self.tablero.generar_posibles_movimientos()

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
        
        if self.tablero.es_movimiento_enrroque(self.movimiento_a_realizar):
            self.tablero.realizar_enrroque(self.movimiento_a_realizar)
            self.master.GUI_ajedrez.colocar_enrroque(self.movimiento_a_realizar)
        elif self.tablero.es_movimiento_coronacion(self.movimiento_a_realizar):
            self.tablero.realizar_coronamiento(self.movimiento_a_realizar,pieza_de_coronamiento)
            self.master.GUI_ajedrez.colocar_coronamiento(self.movimiento_a_realizar,pieza_de_coronamiento)
        else:
            self.tablero.mover_pieza(self.movimiento_a_realizar)
            self.master.GUI_ajedrez.mover_pieza(self.movimiento_a_realizar)
        
        self.actualizar_turno_pc()
        self.actualizar_estado_de_tablero()
        self.master.GUI_ajedrez.actualizar_estado_de_pantalla()
        self.limpiar_casilla_inicial() 
        self.limpiar_casilla_objetivo()
        self.limpiar_movimiento_a_realizar()
        self.ejecutar()

        ##if tipo == 1 (todos los movimientos son del jug)

        ##if tipo == 2 (calcula el siguiente movimiento de la pc)

        ##if tipo == 3 (todos los mov de la pc)

    def ejecutar(self):
        if self.tipo_de_juego == 1:
            return
        elif self.tipo_de_juego == 2:
            if self.es_turno_pc:
                #self.movimiento_a_realizar = realizar_movimiento_de_pc
                #self.mover_pieza()
                print("no implementado")
                return
            else:
                return
        elif self.tipo_de_juego == 3:
            #self.movimiento_a_realizar = realizar_movimiento_de_pc
            #self.mover_pieza()  
            print("no implementado")
            return

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
