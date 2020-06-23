import threading
import copy
import time

from collections import deque

from Juego.Tipos import Turno
from Juego.Nodo import Nodo
from Juego.Enrroque import Enrroque
from Juego.ArbolDecision import ArbolDecision
from Juego.Tipos import Estado

class ThreadedTask(threading.Thread):
    
    def __init__(self, master):
        threading.Thread.__init__(self)
        self.master = master
        
    
    def run(self):
        #time.sleep(2)  # Simulate long running process
        ## valores para inicializar un nodo : id,tablero,turno,enrroque,nivel,estado,valor,MAX_NODE
        id = deque() ## Nodo inicial
        tablero = copy.deepcopy(self.master.juego.tablero) ## copia una instancia del tablero
        tablero.calculando_movimiento = True
        if self.master.juego.turno == 'B':
            turno = Turno.BLANCAS
        elif self.master.juego.turno == 'N':
            turno = Turno.NEGRAS
        enrroque = Enrroque(self.master.juego.enrroque_blancas_corto,self.master.juego.enrroque_blancas_largo,self.master.juego.enrroque_negras_corto,self.master.juego.enrroque_negras_largo)
        nivel = 0 ## nivel inicial 0
        estado = Estado.VIVO ## Estado inicial vivo
        valor = 100000 ## +infinito (numero suficientemente grande como para ser mayor a cualquier evaluacion de estado)
        MAX_NODE = 4 ## Profundidad Maxima del arbol (aumentar de dos en dos)
        nodo_inicial = Nodo(id,tablero,turno,enrroque,nivel,estado,valor,MAX_NODE)
        arbol_de_decision = ArbolDecision(nodo_inicial)

        ## meter en cola
        self.master.juego.movimiento_a_realizar = arbol_de_decision.minimax_SSS_estrella()
        self.master.juego.calculando_movimiento = False
        self.master.juego.queue.put(self.master.juego.movimiento_a_realizar)