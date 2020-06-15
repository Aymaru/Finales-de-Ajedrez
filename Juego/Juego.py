import copy
import time
import queue

from collections import deque

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
from Juego.Tipos import Turno
from Juego.Log import Log

##Evaluador
from Juego.Evaluador import Evaluador


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

        self.movimientos_legales = deque()
        self.posibles_movimientos = deque()
        self.posibles_movimientos_blancas = deque()
        self.posibles_movimientos_negras = deque()
        
        self.es_jaque = False
        self.jaque_mate = False
        self.es_tablas = False
        self.es_turno_pc = False
        
        self.queue = queue.Queue()
        self.calculando_movimiento = False
        
        self.casilla_inicial = None
        self.casilla_objetivo = None
        self.movimiento_a_realizar = None
        
        self.__log = Log(self.tablero,piezas_iniciales,self.tipo_de_juego,self.J1,self.J2,self.turno)
        self.actualizar_estado_de_tablero()

    def guardar_log(self):
        self.__log.registrar_log()

    def set_evaluacion_de_tablero(self):
        evaluador = Evaluador(self.tablero.tablero)
        if self.turno == 'B':
            turno = Turno.BLANCAS
        else:
            turno = Turno.NEGRAS
        
        self.evaluacion_de_tablero = evaluador.evaluar_tablero(turno)
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
        #self.set_evaluacion_de_tablero()
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
        self.posibles_movimientos_blancas.clear()
        self.posibles_movimientos_blancas.extend(self.tablero.posibles_movimientos_de_blancas(self.posibles_movimientos))

    def set_posibles_movimientos_negras(self):
        self.posibles_movimientos_negras.clear()
        self.posibles_movimientos_negras.extend(self.tablero.posibles_movimientos_de_negras(self.posibles_movimientos))

    def set_jugadores(self):
        
        if self.J1 == "B":
            self.J2 = "N"
        else:
            self.J2 = "B"
    
    def set_es_jaque(self):
        self.es_jaque = self.tablero.hay_jaque(self.posibles_movimientos,self.turno)
        print(self.es_jaque)

    def set_jaque_mate(self):
        if self.es_jaque and len(self.movimientos_legales) == 0:
            self.jaque_mate = True
            if self.turno == "B":
                self.__log.resultado = Turno.NEGRAS
            elif self.turno == "N":
                self.__log.resultado = Turno.BLANCAS
            self.__log.registrar_log()
        else:
            self.jaque_mate = False

    def set_es_tablas(self):
        if not self.es_jaque and len(self.movimientos_legales) == 0:
            self.es_tablas = True
            if self.turno == "B":
                self.__log.resultado = Turno.NEGRAS
            elif self.turno == "N":
                self.__log.resultado = Turno.BLANCAS
            self.__log.registrar_log()
        else:
            self.es_tablas = False

    def colocar_piezas_iniciales(self,piezas_iniciales):
        piezas = piezas_iniciales.split(" ") ##Esto creo que se debe cambiar por espacios, a como lo pide el profe y cambiar las comas por espacios en los archivos de juego
        piezas_iniciales = []
        for pieza in piezas:
            piezas_iniciales.append(list(pieza))
        self.tablero.colocar_piezas_iniciales(piezas_iniciales)

    def set_movimientos_legales(self):
        self.movimientos_legales.clear()
        self.movimientos_legales.extend(self.tablero.obtener_movimientos_legales(self.posibles_movimientos,self.turno))        

    def set_posibles_movimientos(self):
        self.posibles_movimientos.clear()
        self.posibles_movimientos.extend(self.tablero.generar_posibles_movimientos())

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
            self.master.GUI_ajedrez.colocar_enrroque(movimiento_a_realizar)
            self.tablero.realizar_enrroque(movimiento_a_realizar)
        elif self.tablero.es_movimiento_coronacion(movimiento_a_realizar):
            self.master.GUI_ajedrez.colocar_coronamiento(movimiento_a_realizar,pieza_de_coronamiento)
            self.tablero.realizar_coronamiento(movimiento_a_realizar,pieza_de_coronamiento)
        else:
            self.master.GUI_ajedrez.mover_pieza(movimiento_a_realizar)
            self.tablero.mover_pieza(movimiento_a_realizar)

        self.master.GUI_ajedrez.limpiar_casillas_mov_anterior()
        self.master.GUI_ajedrez.marcar_movimiento_anterior(movimiento_a_realizar)
        self.actualizar_turno_pc()
        self.actualizar_estado_de_tablero()
        self.master.GUI_ajedrez.actualizar_estado_de_pantalla()
        self.__log.agregar_log(self.tablero,movimiento_a_realizar)
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

    def ejecutar(self):
        #print("tipo de juego: %d",(self.tipo_de_juego))
        #time.sleep(1)
        if self.jaque_mate or self.es_tablas:
            return

        if self.tipo_de_juego == 1:
            return
        elif self.tipo_de_juego == 2:
            if self.es_turno_pc:
                if self.calculando_movimiento == False:
                    self.calculando_movimiento = True
                    ## ejecuta el algoritmo  para seleccionar el siguiente movimiento minimax sss* 
                    ThreadedTask.ThreadedTask(self.master).start() ## se hace en un thread para no bloquear la ejecucion de mainloop y que no se bloquee la GUI
                    self.master.after(100, self.process_queue) 
            else:
                return
        elif self.tipo_de_juego == 3:
            if self.calculando_movimiento == False:
                self.calculando_movimiento = True
                ThreadedTask.ThreadedTask(self.master).start()
                self.master.after(100, self.process_queue) 
            return
        
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
    