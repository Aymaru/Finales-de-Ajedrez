from collections import deque

from Juego import Nodo
from Juego.Tipos import Estado
from Juego import Enrroque

class ArbolDecision:

    def __init__(self,nodo):
        self.nodo_inicial = nodo ## nodo inicial del arbol de decisiones 
        self.lista = deque() ## lista que utiliza el algoritmo minimax para recorrer el arbol
        self.movimiento_seleccionado = None ## es el movimiento que devuelve la funcion minimax. Se selecciona cuando un nodo solucionado min, devuelve el nodo inicial
        self.deque_nodos = deque()        
    
    ##def padre(nodo): -> nodo
    def padre(self,nodo):
        id_padre = nodo.get_id_padre()
        return self.nodo_inicial.buscar_nodo(id_padre)

    def minimax_SSS_estrella(self):
        self.insertar_delante(self.nodo_inicial)
        self.minimax_SSS_estrella_aux()
        return self.movimiento_seleccionado

    def minimax_SSS_estrella_aux(self):
        
        while(True):
            nodo_actual = self.lista.popleft() ## Obtiene y elimina el primer elemento de la lista
            if not nodo_actual.id and nodo_actual.estado == Estado.SOLUCIONADO:
                return            
            if nodo_actual.estado == Estado.VIVO: ##esta vivo
                if not nodo_actual.es_terminal(): ## No es terminal
                    if nodo_actual.es_max(): ## es MAX
                        ## insertar todos los hijos del nodo en la cabeza de lista
                        nodo_actual.generar_todos_los_hijos()
                        for nodo_tmp in nodo_actual.hijos:
                            nodo_tmp.set_estado(Estado.VIVO)
                            self.insertar_delante(nodo_tmp)
                    elif nodo_actual.es_min(): ## es MIN
                        ## insertar el primer hijo del nodo en la cabeza de lista                         
                        nodo_tmp = nodo_actual.generar_hijo(0,nodo_actual.valor,nodo_actual.estado)
                        nodo_actual.hijos.append(nodo_tmp)
                        self.insertar_delante(nodo_tmp)

                else: ## Es terminal
                    ## insertar el mismo nodo con estado SOLUCIONADO y min(valor y f(nodo))
                    nodo_actual.actualizar_valor()
                    nodo_actual.solucionar_nodo()
                    self.insertar_delante_de_menores(nodo_actual)

            else: ##esta solucionado
                if nodo_actual.es_max(): ## es MAX
                    #nodo_actual.get_id_nodo().imprimir()
                    nodo_padre = self.padre(nodo_actual)
                    total_de_hijos = nodo_padre.cantidad_de_hijos_max()
                    hijo_actual = nodo_padre.buscar_nodo_hijo(nodo_actual.get_id_nodo())
                    if hijo_actual < total_de_hijos-1:  ## Si no es el ultimo hijo del padre, insertar el siguiente hermano en la cabeza de lista como VIVO con el valor del nodo
                        nodo_tmp = nodo_padre.generar_hijo(hijo_actual+1,nodo_actual.valor,Estado.VIVO)
                        nodo_padre.hijos.append(nodo_tmp)
                        nodo_tmp.set_valor(nodo_actual.valor)
                        self.insertar_delante(nodo_tmp)
                    else: ## Si es el ultimo hijo del padre, insertar el padre como SOLUCIONADO en la cabeza de la lista
                        nodo_padre.solucionar_nodo()
                        nodo_padre.set_valor(nodo_actual.valor)
                        self.insertar_delante(nodo_padre)               
                    
                elif nodo_actual.es_min():  ## es MIN
                    ## insertar padre como SOLUCIONADO con el valor del nodo en la cabeza de la lista
                    nodo_padre = self.padre(nodo_actual)
                    if not nodo_padre.id: ## Si el padre es [], actualizar movimiento seleccionado con el id del nodo
                        self.movimiento_seleccionado = nodo_actual.get_id_nodo()
                    nodo_padre.solucionar_nodo()
                    nodo_padre.set_valor(nodo_actual.valor)
                    self.eliminar_sucesores(nodo_padre.id)
                    self.insertar_delante(nodo_padre)
                    nodo_padre.eliminar_hijos()
                    ## Eliminar todos los sucesores de la lista
                    ## Eliminar todos los sucesores del arbol?
        
    def eliminar_sucesores(self,id):
        lista_index = self.get_indices_sucesores(id)
        self.eliminar_posiciones(lista_index)
    
    def get_indices_sucesores(self,id):
        index = 0
        lista_index = deque()
        for nodo in self.lista:
            if nodo.es_sucesor(id):
                lista_index.append(index)
            index += 1
        return lista_index

    ## elimina n elementos en los indices dados de un deque
    def eliminar_posiciones(self,indices_a_borrar):
        rotate = 0
        eliminados = 0 
        indice_inicial = 0
        
        for indice_a_borrar in indices_a_borrar:
            rotate = indice_a_borrar - indice_inicial - eliminados
            self.lista.rotate(-rotate)
            self.lista.popleft()
            indice_inicial = indice_inicial + rotate
            eliminados += 1
        
        self.lista.rotate(indice_inicial)

    def insertar_delante(self,nodo):
        self.lista.appendleft(nodo)
        
    
    def insertar_delante_de_menores(self,nodo):
        if not self.lista:
            self.lista.appendleft(nodo)
        else:
            index = 0
            for nodo_tmp in self.lista:
                if nodo_tmp.valor < nodo.valor:
                    break
                else:
                    index += 1
            self.insertar_en_index(nodo,index)

    def insertar_en_index(self,nodo,index):
        self.lista.rotate(-index)
        self.lista.appendleft(nodo)
        self.lista.rotate(index)

    ##def eliminar sucesores
    ##def #_hijos_nodo(nodo): int

    ##def #_de_hijo(nodo,padre): int

    ##def #_de_hijos_de