
from Juego import Nodo
from Juego import Estado
from Juego import Enrroque

def print_id(id):
    print("_id_init")
    if len(id) == 0:
        print("[]")
    else:
        for index in range(0,len(id)):
            id[index].imprimir()
    print("_id_end")

class ArbolDecision:

    def __init__(self,nodo):
        self.nodo_inicial = nodo ## nodo inicial del arbol de decisiones 
        self.lista = [] ## lista que utiliza el algoritmo minimax para recorrer el arbol
        self.movimiento_seleccionado = None ## es el movimiento que devuelve la funcion minimax. Se selecciona cuando un nodo solucionado min, devuelve el nodo inicial

    def buscar_nodo(self,nodo,id):
        #print("buscar nodo:")
        #print_id(id)
        if nodo.es_nodo(id):
            return nodo
        else:
            nodo_actual = nodo
            #print("nodo actual: ")
            #print_id(nodo_actual.id)
            cantidad_de_hijos = nodo_actual.cantidad_de_hijos()
            #print("cantidad de hijos: %d" % cantidad_de_hijos)
            
            for index in range(0,cantidad_de_hijos):
                nodo_tmp = nodo_actual.hijos[index]
                #print("nodo hijo:")
                #print_id(nodo_tmp.id)
                if nodo_tmp.es_nodo(id):
                    return nodo_tmp
                if nodo_actual.hijos[index].es_predecesor(id):
                    nodo_tmp = self.buscar_nodo(nodo_actual.hijos[index],id)
                    if nodo_tmp != None:
                        return nodo_tmp

            #print("No Ne")
            return None

    ##def padre(nodo): -> nodo
    def padre(self,nodo):
        id_padre = nodo.get_id_padre()
        return self.buscar_nodo(self.nodo_inicial,id_padre)

    def minimax_SSS_estrella(self):
        self.insertar_delante(self.nodo_inicial)
        self.minimax_SSS_estrella_aux()
        return self.movimiento_seleccionado

    def minimax_SSS_estrella_aux(self):
        
        while(True):
            # print("__")
            # print(len(self.lista))
            nodo_actual = self.lista.pop(0)
            # print("nodo actual: ")
            
            # id_print = nodo_actual.get_id_nodo()

            # if id_print == []:
            #     print("[]")                
            # else:
            #     print(id_print.imprimir())
            # print(nodo_actual.valor)
            # print(len(self.lista))
            if nodo_actual.id == [] and nodo_actual.estado == Estado.Estado.SOLUCIONADO:
                #print("finaliza")
                return
            
            if nodo_actual.estado == Estado.Estado.VIVO: ##esta vivo
                #print("vivo")
                #print(nodo_actual.es_terminal())

                if not nodo_actual.es_terminal(): ## No es terminal
                    if nodo_actual.es_max(): ## es MAX
                        ## insertar todos los hijos del nodo en la cabeza de lista
                        nodo_actual.generar_todos_los_hijos()
                        total_de_hijos = nodo_actual.cantidad_de_hijos_max()
                        for index in range(total_de_hijos-1,-1,-1):
                            nodo_tmp = nodo_actual.hijos[index]
                            #nodo_tmp.set_estado(Estado.Estado.VIVO)
                            self.insertar_delante(nodo_tmp)
                        
                    elif nodo_actual.es_min(): ## es MIN
                        ## insertar el primer hijo del nodo en la cabeza de lista                         
                        nodo_actual.generar_hijo(0,nodo_actual.valor,nodo_actual.estado)
                        nodo_tmp = nodo_actual.get_nodo_hijo(0)
                        self.insertar_delante(nodo_tmp)
                else: ## Es terminal
                    ## insertar el mismo nodo con estado SOLUCIONADO y min(valor y f(nodo))
                    nodo_actual.actualizar_valor()
                    nodo_actual.solucionar_nodo()
                    self.insertar_delante_de_menores(nodo_actual)

            else: ##esta solucionado
                #print("solucionado")
                if nodo_actual.es_max(): ## es MAX
                    #nodo_actual.get_id_nodo().imprimir()
                    nodo_padre = self.padre(nodo_actual)
                    total_de_hijos = nodo_padre.cantidad_de_hijos_max()
                    hijo_actual = nodo_padre.buscar_nodo_hijo(nodo_actual.get_id_nodo())
                    if hijo_actual != total_de_hijos-1:  ## Si no es el ultimo hijo del padre, insertar el siguiente hermano en la cabeza de lista como VIVO con el valor del nodo
                        nodo_padre.generar_hijo(hijo_actual+1,nodo_actual.valor,Estado.Estado.VIVO)
                        nodo_tmp = nodo_padre.get_nodo_hijo(hijo_actual+1)
                        nodo_tmp.set_valor(nodo_actual.valor)
                        self.insertar_delante(nodo_tmp)
                    else: ## Si es el ultimo hijo del padre, insertar el padre como SOLUCIONADO en la cabeza de la lista
                        nodo_padre.solucionar_nodo()
                        nodo_padre.set_valor(nodo_actual.valor)
                        self.insertar_delante(nodo_padre)               
                    
                elif nodo_actual.es_min():  ## es MIN
                    ## insertar padre como SOLUCIONADO con el valor del nodo en la cabeza de la lista
                    nodo_padre = self.padre(nodo_actual)
                    if nodo_padre.id == []: ## Si el padre es [], actualizar movimiento seleccionado con el id del nodo
                        self.movimiento_seleccionado = nodo_actual.get_id_nodo()
                    nodo_padre.solucionar_nodo()
                    nodo_padre.set_valor(nodo_actual.valor)
                    self.insertar_delante(nodo_padre)
                    self.eliminar_sucesores(nodo_padre.id)
                    #nodo_padre.eliminar_hijos()
                    ## Eliminar todos los sucesores de la lista
                    ## Eliminar todos los sucesores del arbol?
            #print(len(self.lista))
    
    def eliminar_sucesores(self,id):
        lista_index = self.get_indices_sucesores(id)
        for index in range(len(lista_index)-1,-1,-1):
            self.lista.pop(lista_index[index])

    
    def get_indices_sucesores(self,id):
        index = 0
        lista_index = []
        for nodo in self.lista:
            if nodo.es_sucesor(id):
                lista_index.append(index)
            index += 1
        return lista_index

    def insertar_delante(self,nodo):
        if self.lista == []:
            self.lista.append(nodo)
        else:
            self.lista.insert(0,nodo)

    def insertar_delante_de_menores(self,nodo):
        if self.lista == []:
            self.lista.append(nodo)
        else:
            index = 0
            for nodo_tmp in self.lista:
                if nodo_tmp.valor < nodo.valor:
                    break
                else:
                    index += 1
            self.lista.insert(index,nodo)


    ##def eliminar sucesores
    ##def #_hijos_nodo(nodo): int

    ##def #_de_hijo(nodo,padre): int

    ##def #_de_hijos_de