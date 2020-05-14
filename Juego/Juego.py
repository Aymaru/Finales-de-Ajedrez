import copy
import time
import queue

##clases de juego
from Juego import Tablero
from Juego import Movimiento
from Juego import ArbolDecision
from Juego import Nodo
from Juego import Enrroque
from Juego import ThreadedTask

##enums
from Juego import Estado
from Juego import Turno

## GUI
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
        
        self.queue = queue.Queue()
        self.calculando_movimiento = False
        
        self.casilla_inicial = None
        self.casilla_objetivo = None
        self.movimiento_a_realizar = None

        self.actualizar_estado_de_tablero()
        #self.ejecutar()
        ##Se instancia la interfaz
        #self.GUI_ajedrez = Ajedrez.Ajedrez(self.master)

    def set_evaluacion_de_tablero(self):
        self.evaluacion_de_tablero = self.tablero.evaluacion_del_juego()
        print("Evaluacion: %d",(self.evaluacion_de_tablero))
            
    def generar_movimientos_de_enrroque(self):
        if self.turno == 'B':

            if self.enrroque_blancas_corto:
                enrroque_bc = self.tablero.generar_enrroque_blancas_corto(self.posibles_movimientos_negras)
                if enrroque_bc != None:
                    self.movimientos_legales.append(enrroque_bc)
            if self.enrroque_blancas_largo:
                enrroque_bl = self.tablero.generar_enrroque_blancas_largo(self.posibles_movimientos_negras)
                if enrroque_bl != None:
                    self.movimientos_legales.append(enrroque_bl)

        else:

            if self.enrroque_negras_corto:
                enrroque_nc = self.tablero.generar_enrroque_negras_corto(self.posibles_movimientos_blancas)
                if enrroque_nc != None:
                    self.movimientos_legales.append(enrroque_nc)
            if self.enrroque_negras_largo:
                enrroque_nl = self.tablero.generar_enrroque_negras_largo(self.posibles_movimientos_blancas)
                if enrroque_nl != None:
                    self.movimientos_legales.append(enrroque_nl)

    def actualizar_estado_de_tablero(self):
        self.set_evaluacion_de_tablero()
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
            if self.turno != self.J1:
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

    def mover_pieza(self,movimiento_a_realizar):
        
        if self.turno == 'B':
            pieza_de_coronamiento = 5
            self.turno = 'N'
        else:
            pieza_de_coronamiento = -5
            self.turno = 'B'
        
        if self.tablero.es_movimiento_enrroque(movimiento_a_realizar):
            self.tablero.realizar_enrroque(movimiento_a_realizar)
            self.master.GUI_ajedrez.colocar_enrroque(movimiento_a_realizar)
        elif self.tablero.es_movimiento_coronacion(movimiento_a_realizar):
            self.tablero.realizar_coronamiento(movimiento_a_realizar,pieza_de_coronamiento)
            self.master.GUI_ajedrez.colocar_coronamiento(movimiento_a_realizar,pieza_de_coronamiento)
        else:
            self.tablero.mover_pieza(movimiento_a_realizar)
            self.master.GUI_ajedrez.mover_pieza(movimiento_a_realizar)
        
        self.actualizar_turno_pc()
        self.actualizar_estado_de_tablero()
        self.master.GUI_ajedrez.actualizar_estado_de_pantalla()
        self.limpiar_casilla_inicial() 
        self.limpiar_casilla_objetivo()
        self.limpiar_movimiento_a_realizar()
        #time.sleep(1)
        #self.ejecutar()

        ##if tipo == 1 (todos los movimientos son del jug)

        ##if tipo == 2 (calcula el siguiente movimiento de la pc)

        ##if tipo == 3 (todos los mov de la pc)


        #ThreadedTask(self.master).start()
    def queue_movimiento_a_realizar(self):
        self.queue.put(self.movimiento_a_realizar)

    # def process_queue(self):
    #     try:
            
    #         # Show result of the task if needed
    #         #self.mover_pieza(movimiento_a_realizar)
    #         movimiento_a_realizar = self.queue.get(0)
    #         self.mover_pieza(movimiento_a_realizar)
    #     except queue.Empty:
            
    #         if self.jaque_mate or self.es_tablas: # ??mandar un mov none para indicar que se termina la partida or movimiento_a_realizar == None:
    #             ##hacer todos los procesos de finalizacion
    #             return

    #         if self.tipo_de_juego == 1:
    #             self.master.after(100, self.process_queue)
    #         elif self.tipo_de_juego == 2:
    #             if self.es_turno_pc:
    #                 if self.calculando_movimiento == False:
    #                     self.calculando_movimiento = True
    #                     ThreadedTask(self.master).start()
    #                 self.master.after(100, self.process_queue)               
    #         elif self.tipo_de_juego == 3:
                
    #             print("no implementado")
    #             return
    #         self.master.after(100, self.process_queue)
    
    def ejecutar(self):
        print("tipo de juego: %d",(self.tipo_de_juego))
        #time.sleep(1)
        if self.jaque_mate or self.es_tablas:
            return

        if self.tipo_de_juego == 1:
            return
        elif self.tipo_de_juego == 2:
            if self.es_turno_pc:
                if self.calculando_movimiento == False:
                    self.calculando_movimiento = True
                    ThreadedTask.ThreadedTask(self.master).start()
                    self.master.after(100, self.process_queue) 

                # ## valores para inicializar un nodo : id,tablero,turno,enrroque,nivel,estado,valor,MAX_NODE
                # id = [] ## Nodo inicial
                # tablero = copy.deepcopy(self.tablero) ## copia una instancia del tablero
                # if self.turno == 'B':
                #     turno = Turno.Turno.BLANCAS
                # elif self.turno == 'N':
                #     turno = Turno.Turno.NEGRAS
                # enrroque = Enrroque.Enrroque(self.enrroque_blancas_corto,self.enrroque_blancas_largo,self.enrroque_negras_corto,self.enrroque_negras_largo)
                # nivel = 0 ## nivel inicial 0
                # estado = Estado.Estado.VIVO ## Estado inicial vivo
                # valor = 100000 ## +infinito (numero suficientemente grande como para ser mayor a cualquier evaluacion de estado)
                # MAX_NODE = 2 ## Profundidad Maxima del arbol (aumentar de dos en dos)
                # nodo_inicial = Nodo.Nodo(id,tablero,turno,enrroque,nivel,estado,valor,MAX_NODE)
                # arbol_de_decision = ArbolDecision.ArbolDecision(nodo_inicial)

                # self.movimiento_a_realizar = arbol_de_decision.minimax_SSS_estrella()
                
                #self.movimiento_a_realizar.imprimir()
                #self.mover_pieza()
            else:
                return
        elif self.tipo_de_juego == 3:
            if self.calculando_movimiento == False:
                self.calculando_movimiento = True
                ThreadedTask.ThreadedTask(self.master).start()
                self.master.after(100, self.process_queue) 
            return

        
        #ThreadedTask(self.master).start()
        

    def process_queue(self):
        try:
            movimiento_a_realizar = self.queue.get(0)
            # Show result of the task if needed
            self.mover_pieza(movimiento_a_realizar)
            self.ejecutar()
            #self.prog_bar.stop()
        except queue.Empty:
            self.master.after(100, self.process_queue)



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
