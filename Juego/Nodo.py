
import copy
from collections import deque

from Juego.Evaluador import Evaluador
from Juego import Tablero
from Juego import Movimiento
from Juego import Estado
from Juego import Turno
from Juego import Enrroque
from Juego import Tablero


class Nodo:

    def __init__(self,id,tablero,turno,enrroque,nivel,estado,valor,MAX_NODE):
        self.id = id ## identifica al nodo, lista con los movimientos que llevaron a ese estado
        self.tablero = tablero ## tablero del juego
        self.turno = turno ## turno del movimiento, se usa para generar movimientos legales
        
        self.enrroque = enrroque
        self.movimientos_legales = deque() ## Posibles nodos hijos
        
        self.hijos = deque() ## Nodos hijos
        
        self.nivel = nivel ## Nivel del nodo, se utiliza para saber si un nodo es max o min y para encontrar la profundidad maxima
        self.estado = estado #SOLUCIONADO, VIVO
        self.valor = valor
        self.MAX_NODE = MAX_NODE ## Nivel maximo de profundidad del arbol
        self.iniciar_nodo()

        self.evaluador = None

    def iniciar_nodo(self):      
        #print(self.id)
        if self.id:
            movimiento = self.get_id_nodo()
            self.mover_pieza(movimiento)
        self.generar_movimientos_legales()
        ##generar movimientos legales

    def buscar_nodo(self,id):
        if self.es_nodo(id):
            return self
        else:            
            for nodo_tmp in self.hijos:
                #nodo_tmp = self.hijos[index]
                if nodo_tmp.es_nodo(id):
                    return nodo_tmp
                if nodo_tmp.es_predecesor(id):
                    nodo_tmp = nodo_tmp.buscar_nodo(id)
                    if nodo_tmp != None:
                        return nodo_tmp
            return None

    def mover_pieza(self,movimiento):
        self.actualizar_estado_enrroque(movimiento)
        if self.tablero.es_movimiento_enrroque(movimiento):
            self.tablero.realizar_enrroque(movimiento)
        elif self.tablero.es_movimiento_coronacion(movimiento):
            if self.turno == Turno.Turno.BLANCAS:
                self.turno == Turno.Turno.NEGRAS
                pieza_de_coronacion = 5
            elif self.turno == Turno.Turno.NEGRAS:
                self.turno == Turno.Turno.BLANCAS
                pieza_de_coronacion = -5
            self.tablero.realizar_coronamiento(movimiento,pieza_de_coronacion)
        else:
            self.tablero.mover_pieza(movimiento)
    
    def eliminar_hijos(self):
        #cantidad_hijos = self.cantidad_de_hijos()
        # for index in range(cantidad_hijos-1,-1,-1):
        #     self.hijos[index].eliminar_hijos()
        #     self.hijos.pop(index)
        while(self.hijos):
            nodo_tmp = self.hijos.popleft()
            nodo_tmp.eliminar_hijos

    def actualizar_estado_enrroque(self,movimiento):
        pieza_a_mover = abs(self.tablero.obtener_pieza_de_casilla(movimiento.casilla_inicial))
        if self.turno == Turno.Turno.BLANCAS:
            if pieza_a_mover == 6:
                self.enrroque.blancas_corto = False    
                self.enrroque.blancas_largo = False
            elif pieza_a_mover == 4:
                if movimiento.casilla_inicial.columna == 0:
                    self.enrroque.blancas_largo = False
                elif movimiento.casilla_inicial.columna == 7:
                    self.enrroque.blancas_corto = False
        elif self.turno == Turno.Turno.NEGRAS:
            if pieza_a_mover == 6:
                self.enrroque.negras_corto = False    
                self.enrroque.negras_largo = False
            elif pieza_a_mover == 4:
                if movimiento.casilla_inicial.columna == 0:
                    self.enrroque.negras_largo = False
                elif movimiento.casilla_inicial.columna == 7:
                    self.enrroque.negras_corto = False

    def generar_movimientos_legales(self):

        posibles_movimientos = self.tablero.generar_posibles_movimientos()
        turno = self.turno_to_string()
        self.movimientos_legales = deque(self.tablero.obtener_movimientos_legales(posibles_movimientos,turno)) #de momento transformo lista en deque, luego cambio tablero para que trabaje con deque
        self.generar_movimientos_de_enrroque(posibles_movimientos)
        
        #posibles_movimientos = self.tablero.generar_posibles_movimientos()
        
        self.set_es_jaque(posibles_movimientos)
        self.set_jaque_mate()
        self.set_es_tablas()
        #if self.es_terminal():
            #self.movimientos_legales = []

    
    def generar_movimientos_de_enrroque(self,posibles_movimientos):
        if self.turno == Turno.Turno.BLANCAS:
            posibles_movimientos_negras = self.tablero.posibles_movimientos_de_negras(posibles_movimientos)
            if self.enrroque.blancas_corto:
                enrroque_bc = self.tablero.generar_enrroque_blancas_corto(posibles_movimientos_negras)
                if enrroque_bc != None:
                    self.movimientos_legales.appendleft(enrroque_bc)
            if self.enrroque.blancas_largo:
                enrroque_bl = self.tablero.generar_enrroque_blancas_largo(posibles_movimientos_negras)
                if enrroque_bl != None:
                    self.movimientos_legales.appendleft(enrroque_bl)

        elif self.turno == Turno.Turno.NEGRAS:
            posibles_movimientos_blancas = self.tablero.posibles_movimientos_de_blancas(posibles_movimientos)
            if self.enrroque.negras_corto:
                enrroque_nc = self.tablero.generar_enrroque_negras_corto(posibles_movimientos_blancas)
                if enrroque_nc != None:
                    self.movimientos_legales.appendleft(enrroque_nc)
            if self.enrroque.negras_largo:
                enrroque_nl = self.tablero.generar_enrroque_negras_largo(posibles_movimientos_blancas)
                if enrroque_nl != None:
                    self.movimientos_legales.appendleft(enrroque_nl)

    def turno_to_string(self):
        if self.turno == Turno.Turno.BLANCAS:
            return "B"
        elif self.turno == Turno.Turno.NEGRAS:
            return "N"

    def es_terminal(self):
        #print("nivel: ",self.nivel)
        #print("max node: ",self.MAX_NODE)
        if self.nivel == self.MAX_NODE or self.es_jaque_mate or self.es_tablas:
            return True
        else:    
            return False

    def set_es_jaque(self,posibles_movimientos):
        self.es_jaque = self.tablero.hay_jaque(posibles_movimientos,self.turno)

    def set_jaque_mate(self):
        if self.es_jaque and len(self.movimientos_legales) == 0:
            self.es_jaque_mate = True
        else:
            self.es_jaque_mate = False

    def set_es_tablas(self):
        if not self.es_jaque and len(self.movimientos_legales) == 0:
            self.es_tablas = True
        else:
            self.es_tablas = False
    
    def es_min(self):
        #print("es min" ,self.nivel)
        return (self.nivel % 2) != 0

    def es_max(self):
        #print("es max" ,self.nivel)
        return (self.nivel % 2) == 0

    def cantidad_de_hijos_max(self):
        return len(self.movimientos_legales)

    def cantidad_de_hijos(self):
        return len(self.hijos)

    def es_predecesor(self,id):
        if not self.id:
            return True
        elif len(self.id) >= len(id):
            return False
        else:
            for id_predecesor,id_actual in zip(self.id,id):
                if not id_actual.equals(id_predecesor):
                    return False
            return True
        #     for index in range(0,len(self.id)):
        #         if not self.id[index].equals(id[index]):
        #             return False
        #     return True
    
    def es_sucesor(self,id):
        if not self.id:
            return False
        elif len(self.id) <= len(id):
            return False
        else:
            for id_sucesor,id_actual in zip(self.id,id):
                if not id_actual.equals(id_sucesor):
                    return False
            return True

    ## def generar todos los hijos
    ## def generar el primer hijo
    ## def generar hijos (aqui decide cual de las dos anteriores utilizar)
    def get_id_padre(self):
        if not self.id:
            return self.id
        id_padre = copy.deepcopy(self.id)
        id_padre.pop()
        return id_padre
        
    def get_id_nodo(self):
        if not self.id:
            return self.id
        else:
            return self.id[len(self.id)-1]

    ## def # hijo 
    def buscar_nodo_hijo(self,id):
        index = 0
        for movimiento in self.movimientos_legales:
            if movimiento.equals(id):
                return index
            else:
                index += 1
        return None

    def es_nodo(self,id):
        if len(self.id) != len(id):
            return False
        for id_nodo,id_actual in zip(self.id,id):
            if not id_actual.equals(id_nodo):
                return False
        return True
    
    def get_nodo_hijo(self,hijo): ## devuelve el nodo en la posicion hijo
        return self.hijos[hijo]
        
    ## def actualizar valor
    def actualizar_valor(self):  
        valor = Evaluador(self.tablero.tablero).evaluar_tablero(self.turno)
        if (self.es_min() and self.turno == Turno.Turno.BLANCAS) or (self.es_max() and self.turno == Turno.Turno.NEGRAS):
            valor = valor * -1

        self.valor = min(self.valor,valor)

    def set_valor(self,valor):
        self.valor = valor

    def solucionar_nodo(self):
        self.estado = Estado.Estado.SOLUCIONADO
    
    def set_estado(self,estado):
        self.estado = estado

    def generar_hijo(self,hijo,valor,estado): ##hijo es el indice en el que se encuentra el movimiento en movimientos legales
        
        movimiento = self.movimientos_legales[hijo]
        id = copy.deepcopy(self.id)
        id.append(movimiento)
        tablero = copy.deepcopy(self.tablero)
        if self.turno == Turno.Turno.BLANCAS:
            turno = Turno.Turno.NEGRAS
        else:
            turno = Turno.Turno.BLANCAS
        enrroque = copy.deepcopy(self.enrroque)
        nivel = 1 + self.nivel
        nodo_hijo = Nodo(id,tablero,turno,enrroque,nivel,estado,valor,self.MAX_NODE) #(self,id,tablero,turno,enrroque,nivel,estado,valor,MAX_NODE)
        
        self.hijos.append(nodo_hijo)

    def generar_todos_los_hijos(self):
        total_de_hijos = self.cantidad_de_hijos_max()
        for index in range (0,total_de_hijos):
            self.generar_hijo(index,self.valor,self.estado)


