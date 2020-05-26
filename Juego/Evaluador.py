from collections import deque

from Juego.Posicion import Posicion
from Juego.Tablero import Tablero
from Juego.Movimiento import Movimiento
from Juego.Tipos import Pieza
from Juego.Tipos import Casilla
from Juego.Tipos import Turno
from Juego.Tipos import TipoEvaluacion
from Juego.Tipos import EstructuraDePeon

class Evaluador(Tablero):

    def __init__(self,tablero):
        super(Evaluador, self).__init__(tablero)
        self.__piezas = {
            Turno.BLANCAS: {
                Pieza.PEON: {},
                Pieza.CABALLO: {},
                Pieza.ALFIL: {},
                Pieza.TORRE: {},
                Pieza.DAMA: {},
                Pieza.REY: {Casilla.ZONA_DEL_REY: []}
            }, 
            Turno.NEGRAS: {
                Pieza.PEON: {},
                Pieza.CABALLO: {},
                Pieza.ALFIL: {},
                Pieza.TORRE: {},
                Pieza.DAMA: {},
                Pieza.REY: {Casilla.ZONA_DEL_REY: []}
            }
        }

        self.__casillas_vacias = []

        # self.__movimientos_de_piezas = {
        #     Turno.BLANCAS: {
        #         Pieza.PEON: {Casilla.ATACADA: [],Casilla.DEFENDIDA: [],Casilla.AMENAZADA: []},
        #         Pieza.CABALLO: {Casilla.ATACADA: [],Casilla.DEFENDIDA: [],Casilla.AMENAZADA: []},
        #         Pieza.ALFIL: {Casilla.ATACADA: [],Casilla.DEFENDIDA: [],Casilla.AMENAZADA: []},
        #         Pieza.TORRE: {Casilla.ATACADA: [],Casilla.DEFENDIDA: [],Casilla.AMENAZADA: []},
        #         Pieza.DAMA: {Casilla.ATACADA: [],Casilla.DEFENDIDA: [],Casilla.AMENAZADA: []},
        #         Pieza.REY: {Casilla.ATACADA: [],Casilla.DEFENDIDA: [],Casilla.AMENAZADA: []}
        #     },
        #     Turno.NEGRAS: {
        #         Pieza.PEON: {Casilla.ATACADA: [], Casilla.DEFENDIDA: [], Casilla.AMENAZADA: []},
        #         Pieza.CABALLO: {Casilla.ATACADA: [], Casilla.DEFENDIDA: [], Casilla.AMENAZADA: []},
        #         Pieza.ALFIL: {Casilla.ATACADA: [], Casilla.DEFENDIDA: [], Casilla.AMENAZADA: []},
        #         Pieza.TORRE: {Casilla.ATACADA: [], Casilla.DEFENDIDA: [], Casilla.AMENAZADA: []},
        #         Pieza.DAMA: {Casilla.ATACADA: [], Casilla.DEFENDIDA: [], Casilla.AMENAZADA: []},
        #         Pieza.REY: {Casilla.ATACADA: [], Casilla.DEFENDIDA: [], Casilla.AMENAZADA: []}                
        #     }
        # }

        self.__posibles_movimientos = deque()

        # self.contador_de_piezas = [ [0,0,0,0,0,0], [0,0,0,0,0,0] ]
        # self.obtener_piezas()

        # self.piezas_blancas = contador_de_piezas[0]
        # self.piezas_negras = contador_de_piezas[1]
        
        ##valor material de las piezas en orden P, C, A, T, D, R
        self.__valor_de_piezas = [1,3,3,5,9,200]

        self.__valores_de_evaluacion = {
            TipoEvaluacion.MATERIAL: {
                Pieza.PEON: 1,
                Pieza.CABALLO: 3,
                Pieza.ALFIL: 3,
                Pieza.TORRE: 5,
                Pieza.DAMA: 9,
                Pieza.REY: 200
            },
            TipoEvaluacion.MOVILIDAD: 0.1,
            TipoEvaluacion.ESTRUCTURA_DE_PEONES: {
                EstructuraDePeon.AVANZADO: 1,
                EstructuraDePeon.ADELANTADO: 0.5,
                EstructuraDePeon.ATRASADO: -1,
                EstructuraDePeon.AISLADO: -1,
                EstructuraDePeon.DOBLADO: -0.5,
                EstructuraDePeon.PASADO: 1,
                EstructuraDePeon.ENCADENADO: 1,
                EstructuraDePeon.BLOQUEADO: -1,
            },
            TipoEvaluacion.ATAQUE_AL_REY: {
                1: 0.1,
                2: 5,
                3: 7.5,
                4: 8.8,
                5: 9.4,
                6: 9.7,
                7: 9.9
            }
        }
        ##Variables de la evaluacion
        self.__valor_material = 0 ##self.__evaluacion_material()
        self.__valor_de_movilidad = 0 ##self.__evaluacion_de_movilidad()
        self.__valor_de_ataque_al_rey = 0 ##self.__evaluacion_de_ataque_al_rey

    def evaluar_tablero(self,turno):
        self.__posibles_movimientos = self.generar_posibles_movimientos()
        self.__get_piezas()
        #self.print_piezas()
        self.__get_estados_de_piezas()
        self.__evaluacion_material()
        self.__evaluacion_de_movilidad()
        self.__evaluacion_de_ataque_al_rey()
        self.__evaluacion_de_estructura_de_peones()

        evaluacion = 0
        
        evaluacion += self.__valor_material 
        evaluacion += self.__valores_de_evaluacion[TipoEvaluacion.MOVILIDAD] * self.__valor_de_movilidad 
        evaluacion += 0.5 * self.__valor_de_ataque_al_rey
        evaluacion += self.__valor_de_estructura_de_peones
        
        if turno == Turno.NEGRAS:
            evaluacion *= -1
        return evaluacion

    def print_piezas(self):
        for color in self.__piezas.keys():
            print("Color: ", color)
            for pieza in self.__piezas[color].keys():
                print("pieza: " , pieza)

                for tmp_pieza in self.__piezas[color][pieza].keys():
                    if(type(tmp_pieza) == type(Posicion(0,0))):
                        obj_pieza = self.__get_pieza_t(color,pieza,tmp_pieza)
                        print("posicion: " , obj_pieza)
                        obj_pieza.imprimir()
           
        
        return

    ##Obtiene las posiciones del tablero por color y por pieza
    ##Devuelve un diccionario de las piezas. self.piezas[color][pieza] = posicion
    ##Ejm self.piezas[Turno.BLANCAS][Pieza.TORRE] = Posicion(2,3)
    ##Guarda la variable self.piezas
    def __get_piezas(self):
        for fila in range(0,8):
            for columna in range(0,8):
                posicion_tmp = Posicion(fila,columna)
                pieza = self.__get_pieza(posicion_tmp)
                color = self.__get_color_de_pieza(posicion_tmp)                
                if pieza == None:
                    self.__casillas_vacias.append(posicion_tmp)
                elif color == Turno.BLANCAS:
                    self.__piezas[color][pieza][posicion_tmp] = {Casilla.ATACA:[],
                                                                Casilla.DEFIENDE:[],
                                                                Casilla.AMENAZADA:[],
                                                                Casilla.ATACADA:[],
                                                                Casilla.DEFENDIDA:[]}
                else:
                    self.__piezas[color][pieza][posicion_tmp] = {Casilla.ATACA:[],
                                                                Casilla.DEFIENDE:[],
                                                                Casilla.AMENAZADA:[],
                                                                Casilla.ATACADA:[],
                                                                Casilla.DEFENDIDA:[]}
                
    
    def __contar_piezas(self,color,pieza):
        return len(self.__piezas[color][pieza])

    ##temp mientras actualizo los enums en el codigo
    def __get_color_de_pieza(self,posicion):
        pieza = self.obtener_pieza_de_casilla(posicion)
        if pieza == 0:
            return None
        elif pieza > 0:
            return Turno.BLANCAS
        elif pieza < 0:
            return Turno.NEGRAS
        else: 
            return None

    ##Recibe una posicion del tablero
    ##Devuelve el valor enum de tipo pieza del valor del tablero en la posicion dada
    ##Ejm asuma que la posicion "posicion" del tablero vale 4
    ##self.__get_pieza(posicion) -> Pieza.Torre
    def __get_pieza(self,posicion):
        pieza = abs(self.obtener_pieza_de_casilla(posicion))
        
        if pieza == 1:
            return Pieza.PEON
        elif pieza == 2:
            return Pieza.CABALLO
        elif pieza == 3:
            return Pieza.ALFIL
        elif pieza == 4:
            return Pieza.TORRE
        elif pieza == 5:
            return Pieza.DAMA
        elif pieza == 6:
            return Pieza.REY
        else:
            return None

    ##Recibe enum Turno, enum Pieza, Posicion
    ##Devuelve el objeto de la pieza en self.__piezas
    def __get_pieza_t(self,color,pieza,posicion):
        tmp_tipo_de_pieza = self.__get_pieza(posicion)
        if tmp_tipo_de_pieza == None:
            for casilla in self.__casillas_vacias:
                if casilla.equals(posicion):
                    return casilla
            return None
        else:
            for tmp_pieza in self.__piezas[color][pieza].keys():                
                if type(tmp_pieza) == type(Posicion(0,0)) and tmp_pieza.equals(posicion):
                    return tmp_pieza
            return None

    def __get_estados_de_piezas(self):

        for movimiento in self.__posibles_movimientos:
            ##pieza y color de casilla como llaves del dict piezas[color][pieza][tmp_pieza][estado]
            casilla_inicial_color = self.__get_color_de_pieza(movimiento.casilla_inicial)
            casilla_inicial_pieza = self.__get_pieza(movimiento.casilla_inicial)

            ##pieza y color de casilla como llaves del dict piezas[color][pieza][tmp_pieza][estado]
            casilla_objetivo_color = self.__get_color_de_pieza(movimiento.casilla_objetivo)
            casilla_objetivo_pieza = self.__get_pieza(movimiento.casilla_objetivo)

            ##tmp_pieza inicial como llave del dic
            tmp_ci_pieza = self.__get_pieza_t(casilla_inicial_color,casilla_inicial_pieza,movimiento.casilla_inicial) 
            if casilla_objetivo_pieza == None:
                ##AMENAZA
                tmp_co_pieza = self.__get_pieza_t(None,None,movimiento.casilla_objetivo)
                self.__piezas[casilla_inicial_color][casilla_inicial_pieza][tmp_ci_pieza][Casilla.AMENAZADA].append(tmp_co_pieza)
            else:                
                tmp_co_pieza = self.__get_pieza_t(casilla_objetivo_color,casilla_objetivo_pieza,movimiento.casilla_objetivo)
                if casilla_inicial_color == casilla_objetivo_color:
                    ##DEFIENDE Y DEFENDIDA
                    self.__piezas[casilla_inicial_color][casilla_inicial_pieza][tmp_ci_pieza][Casilla.DEFIENDE].append(tmp_co_pieza)
                    self.__piezas[casilla_objetivo_color][casilla_objetivo_pieza][tmp_co_pieza][Casilla.DEFENDIDA].append(tmp_ci_pieza)
                else:
                    ##ATACA Y ATACADA
                    self.__piezas[casilla_inicial_color][casilla_inicial_pieza][tmp_ci_pieza][Casilla.ATACA].append(tmp_co_pieza)
                    self.__piezas[casilla_objetivo_color][casilla_objetivo_pieza][tmp_co_pieza][Casilla.ATACADA].append(tmp_ci_pieza)

    def __get_rey(self,color):
        posicion_tmp = Posicion(0,0)
        for key in self.__piezas[color][Pieza.REY].keys():
            if type(key) == type(posicion_tmp):
                return key

    def __get_zona_del_rey(self,color):

        rey = self.__get_rey(color)
        if type(rey) == type(None):
            print("se cae por el rey")
            self.print_piezas()
        for fila in range(rey.fila-4,rey.fila+4):
            for columna in range(rey.columna-4,rey.columna+4):

                tmp_posicion = Posicion(fila,columna)
                if tmp_posicion.validar_posicion():
                    tmp_casilla_pieza = self.__get_pieza(tmp_posicion)
                    tmp_casilla_color = self.__get_color_de_pieza(tmp_posicion)
                    tmp_pieza = self.__get_pieza_t(tmp_casilla_color,tmp_casilla_pieza,tmp_posicion)
                    self.__piezas[color][Pieza.REY][Casilla.ZONA_DEL_REY].append(tmp_pieza)


    def __contar_movimientos_legales(self,color):
        
        contador_movimientos_legales = 0
        if color == Turno.BLANCAS:
            contador_movimientos_legales = len(self.obtener_movimientos_legales(self.__posibles_movimientos,'B'))
        else:
            contador_movimientos_legales = len(self.obtener_movimientos_legales(self.__posibles_movimientos,'N'))

        # for movimiento in self.__posibles_movimientos:
        #     casilla_inicial_color = self.__get_color_de_pieza(movimiento.casilla_inicial)
        #     if casilla_inicial_color == color:
        #         casilla_objetivo_color = self.__get_color_de_pieza(movimiento.casilla_objetivo)
        #         if casilla_objetivo_color != color:
        #             contador_movimientos_legales += 1
        
        return contador_movimientos_legales

    ##Evaluacion de material
    ##La sumatoria de la suma de la cantidad de piezas de las blancas menos las de las negras por el valor material de la pieza
    ##Deja el resultado en self.__valor_material
    def __evaluacion_material(self):
        valor_peon = self.__valor_de_piezas[0]
        valor_caballo = self.__valor_de_piezas[1]
        valor_alfil = self.__valor_de_piezas[2]
        valor_torre = self.__valor_de_piezas[3]
        valor_dama = self.__valor_de_piezas[4]
        valor_rey = self.__valor_de_piezas[5]

        valor_material = 0

        for pieza in self.__piezas[Turno.BLANCAS].keys():

            tmp =  len(self.__piezas[Turno.BLANCAS][pieza]) - len(self.__piezas[Turno.NEGRAS][pieza])
            
            tmp = tmp * self.__valores_de_evaluacion[TipoEvaluacion.MATERIAL][pieza]
            valor_material += tmp

        self.__valor_material = valor_material

    ##Evaluacion de movilidad
    ##Cantidad de movimientos legales de las blancas menos de las negras
    ##Deja el resultado en self.__valor_de_movilidad
    def __evaluacion_de_movilidad(self):        
        self.__valor_de_movilidad = self.__contar_movimientos_legales(Turno.BLANCAS) - self.__contar_movimientos_legales(Turno.NEGRAS)

    ##Evaluacion de ataque al rey   
    ##La zona del rey son las casillas a las que se podria mover el rey mas 3 casillas hacia el oponente
    ##Se cuentan las casillas de la zona del rey atacadas por piezas del oponente.
    ##Se suma la cantidad de casillas atacadas y se multiplica por una constante 20 en caso de caballo o alfil, 40 en caso de torre y 80 en caso de dama
    ##Se multiplica la cantidad de atacantes por el peso del ataque en self.__valores_de_evaluacion[TipoEvaluacion.ATAQUE_AL_REY][cantidad de atacantes]
    ##y se divide entre 100
    ## evaluacion de ataque de las blancas - ataque de las negras
    ##Dela el resultado en self.__valor_de_ataque_al_rey
    def __evaluacion_de_ataque_al_rey(self):
        self.__get_zona_del_rey(Turno.BLANCAS)
        self.__get_zona_del_rey(Turno.NEGRAS)
        valor_de_ataque_blancas = self.__evaluar_ataque_al_rey(Turno.NEGRAS)
        valor_de_ataque_negras = self.__evaluar_ataque_al_rey(Turno.BLANCAS)
        self.__valor_de_ataque_al_rey = valor_de_ataque_blancas - valor_de_ataque_negras

    ##Evaluacion de estructura de peones
    ##Los peones son las piezas mas abundantes, cada jugador tiene 8 peones ubicados en las filas 2 para las blancas y 7 para las negras,
    ##estos tienen poca movilidad, por lo que su estructura en el juego cambia lentamente y determina ciertas ventajas y debilidades en las posiciones de las piezas.
    ##Cada peon es evaluado y se asigna a una estructura.
    ##Las estructuras son: * peon aislado, * cadena de peones, * peon doblado, * peon atrasado, * peon pasado
    ##La evaluacion, toma para cada tipo de estructura, (la cantidad de peones blancos - la cantidad de peones negros ) * el valor de la estructura
    ##Deja el resultado en self.__valor_de_estructura_de_peones
    def __evaluacion_de_estructura_de_peones(self):
        self.__valor_de_estructura_de_peones = 0

        for estructura_de_peon in self.__valores_de_evaluacion[TipoEvaluacion.ESTRUCTURA_DE_PEONES].keys():
            evaluacion = self.__valores_de_evaluacion[TipoEvaluacion.ESTRUCTURA_DE_PEONES][estructura_de_peon] * (self.__evaluar_estructura_peones(Turno.BLANCAS,estructura_de_peon) - self.__evaluar_estructura_peones(Turno.NEGRAS,estructura_de_peon)) 
            self.__valor_de_estructura_de_peones += evaluacion


    def __evaluar_estructura_peones(self,color,estructura_de_peon):

        evaluacion = 0

        for tmp_peon in self.__piezas[color][Pieza.PEON].keys():
            
            if estructura_de_peon == EstructuraDePeon.ADELANTADO:
                if self.__evaluar_peon_es_adelantado(tmp_peon):
                    evaluacion += 1
                    continue   
            elif estructura_de_peon == EstructuraDePeon.AVANZADO:
                if self.__evaluar_peon_es_avanzado(tmp_peon):
                    evaluacion += 1
                    continue
            elif estructura_de_peon == EstructuraDePeon.AISLADO:
                if self.__evaluar_peon_es_aislado(tmp_peon):
                    evaluacion += 1
                    continue
            elif estructura_de_peon == EstructuraDePeon.ATRASADO:
                if self.__evaluar_peon_es_atrasado(tmp_peon):
                    evaluacion += 1
                    continue
            elif estructura_de_peon == EstructuraDePeon.DOBLADO:
                if self.__evaluar_peon_es_doblado(tmp_peon):
                    evaluacion += 1
                    continue
            elif estructura_de_peon == EstructuraDePeon.ENCADENADO:
                if self.__evaluar_peon_es_encadenado(tmp_peon):
                    evaluacion += 1
                    continue
            elif estructura_de_peon == EstructuraDePeon.PASADO:
                if self.__evaluar_peon_es_pasado(tmp_peon):
                    evaluacion += 1
                    continue
            elif estructura_de_peon == EstructuraDePeon.BLOQUEADO:
                if self.__evaluar_peon_es_bloqueado(tmp_peon):
                    evaluacion += 1
                    continue

        return evaluacion

    ##Funcion que evalua si un peon es bloqueado
    def __evaluar_peon_es_bloqueado(self,peon):
        color_peon = self.__get_color_de_pieza(peon)
        if color_peon == Turno.BLANCAS:
            tmp_posicion = Posicion(peon.fila,peon.columna-1)            
        elif color_peon == Turno.NEGRAS:
            tmp_posicion = Posicion(peon.fila,peon.columna+1)  

        tmp_color = self.__get_color_de_pieza(tmp_posicion)
        if tmp_color == None or tmp_color == color_peon:
            return False
        else:
            return True
    ##Funcion que evalua si un peon es doblado
    def __evaluar_peon_es_doblado(self,peon):
        color_peon = self.__get_color_de_pieza(peon)

        for tmp_peon in self.__piezas[color_peon][Pieza.PEON].keys():
            
            if tmp_peon.columna == peon.columna:
                if color_peon == Turno.BLANCAS:
                    if tmp_peon.fila < peon.fila:
                        return True
                elif color_peon == Turno.NEGRAS:
                    if tmp_peon.fila > peon.fila:
                        return True
        return False
    ##Funcion que evalua si un peon es avanzado
    def __evaluar_peon_es_avanzado(self,peon):
        color_peon = self.__get_color_de_pieza(peon)

        if color_peon == Turno.BLANCAS:
            if peon.fila <= 3 and len(self.__piezas[color_peon][Pieza.PEON][peon][Casilla.DEFENDIDA]) > 0:
                return True
            return
        elif color_peon == Turno.NEGRAS:
            if peon.fila >= 4 and len(self.__piezas[color_peon][Pieza.PEON][peon][Casilla.DEFENDIDA]) > 0:
                return True
            return
        return False
    ##Funcion que evalua si un peon es adelantado
    def __evaluar_peon_es_adelantado(self,peon):
        color_peon = self.__get_color_de_pieza(peon)
        
        if color_peon == Turno.BLANCAS:
            if peon.fila <= 3 and len(self.__piezas[color_peon][Pieza.PEON][peon][Casilla.DEFENDIDA]) == 0:
                return True
            return
        elif color_peon == Turno.NEGRAS:
            if peon.fila >= 4 and len(self.__piezas[color_peon][Pieza.PEON][peon][Casilla.DEFENDIDA]) == 0:
                return True
            return
        return False
    ##Funcion que evalua si un peon es encadenado
    def __evaluar_peon_es_encadenado(self,peon):
        color_peon = self.__get_color_de_pieza(peon)

        for fila in range(peon.fila-1,peon.fila+2):
            
            if fila == peon.fila:
                continue

            for columna in range(peon.columna-1,peon.columna+2):
                if columna == peon.columna:
                    continue
                tmp_posicion = Posicion(fila,columna)
                if tmp_posicion.validar_posicion():
                    tmp_pieza = self.__get_pieza_t(color_peon,Pieza.PEON,tmp_posicion)
                    if tmp_posicion == None:
                        continue
                    else:
                        return True
        return False
    ##Funcion que evalua si un peon es asilado
    def __evaluar_peon_es_aislado(self,peon):
        color_peon = self.__get_color_de_pieza(peon)

        for fila in range(peon.fila-1,peon.fila+2):
            for columna in range(peon.columna-1,peon.columna+2):

                if fila == peon.fila and columna == peon.columna:
                    continue
                tmp_posicion = Posicion(fila,columna)
                if tmp_posicion.validar_posicion():
                    tmp_color = self.__get_color_de_pieza(tmp_posicion)
                    if tmp_color == None:
                        continue
                    else:
                        return False

        return True
    ##Funcion que evalua si un peon es pasado
    def __evaluar_peon_es_pasado(self,peon):
        color_peon = self.__get_color_de_pieza(peon)
        
        if color_peon == Turno.BLANCAS:
            
            for fila in range(0,peon.fila):
                for columna in range(peon.columna-1,peon.columna+2):
                    tmp_posicion = Posicion(fila,columna)

                    if tmp_posicion.validar_posicion():
                        tmp_color = self.__get_color_de_pieza(tmp_posicion)
                        if tmp_color == None: 
                            continue
                        elif tmp_color == color_peon:
                            tmp_pieza = self.__get_pieza(tmp_posicion)
                            if tmp_pieza == Pieza.Peon:
                                return False
                        else:
                            tmp_pieza = self.__get_pieza(tmp_posicion)
                            if tmp_pieza == Pieza.Peon:
                                return False
                            else:
                                continue                        
                        return

        elif color_peon == Turno.NEGRAS:
            
            for fila in range(peon.fila+1,8):
                for columna in range(peon.columna-1,peon.columna+2):
                    tmp_posicion = Posicion(fila,columna)

                    if tmp_posicion.validar_posicion():
                        tmp_color = self.__get_color_de_pieza(tmp_posicion)
                        if tmp_color == None or tmp_color == color_peon: 
                            continue
                        else:
                            tmp_pieza = self.__get_pieza(tmp_posicion)
                            if tmp_pieza == Pieza.Peon:
                                return False
                            else:
                                continue                        
                        return
    ##Funcion que evalua si un peon es bloqueado
    def __evaluar_peon_es_atrasado(self,peon):
        color_peon = self.__get_color_de_pieza(peon)
        if not self.__evaluar_peon_es_encadenado(peon):
            return False
        if color_peon == Turno.BLANCAS:
           
            for fila in range(peon.fila-1,peon.fila+2):
                for columna in range(peon.columna-1,peon.columna+2):
                   
                    if fila == peon.fila and columna == peon.columna:
                        continue

                    tmp_posicion = Posicion(fila,columna)

                    if tmp_posicion.validar_posicion():
                        if fila == peon.fila+1:
                            tmp_color = self.__get_color_de_pieza(tmp_posicion)
                            
                            if tmp_color == None or tmp_color != color_peon:
                                continue
                            elif tmp_color == color_peon:
                                tmp_pieza = self.__get_pieza(tmp_posicion)
                                if tmp_pieza == Pieza.PEON:
                                    return False

                        elif fila == peon.fila:
                            tmp_color = self.__get_color_de_pieza(tmp_posicion)
                            
                            if tmp_color == None or tmp_color != color_peon:
                                continue
                            elif tmp_color == color_peon:
                                tmp_pieza = self.__get_pieza(tmp_posicion)
                                if tmp_pieza == Pieza.PEON:
                                    return False

        elif color_peon == Turno.NEGRAS:
            
            for fila in range(peon.fila-1,peon.fila+2):
                for columna in range(peon.columna-1,peon.columna+2):
                    
                    if fila == peon.fila and columna == peon.columna:
                        continue

                    tmp_posicion = Posicion(fila,columna)

                    if tmp_posicion.validar_posicion():
                        if fila == peon.fila - 1:
                            tmp_color = self.__get_color_de_pieza(tmp_posicion)
                            if tmp_color == None or tmp_color != color_peon:
                                continue
                            elif tmp_color == color_peon:
                                tmp_pieza = self.__get_pieza(tmp_posicion)
                                if tmp_pieza == Pieza.PEON:
                                    return False

                        elif fila == peon.fila:
                            tmp_color = self.__get_color_de_pieza(tmp_posicion)
                            if tmp_color == None or tmp_color != color_peon:
                                continue
                            elif tmp_color == color_peon:
                                tmp_pieza = self.__get_pieza(tmp_posicion)
                                if tmp_pieza == Pieza.PEON:
                                    return False
        
        if len(self.__piezas[color_peon][Pieza.PEON][peon][Casilla.DEFENDIDA]) == 0:
            return True
        else:
            return False
        
        

    def __evaluar_ataque_al_rey(self,color):
        
        cantidad_de_atacantes = 0
        valor_del_ataque = 0

        if color == Turno.BLANCAS:
            color_atacante = Turno.NEGRAS
        else:
            color_atacante = Turno.BLANCAS
        
        for pieza in self.__piezas[color_atacante].keys():
            if pieza == Pieza.PEON or pieza == Pieza.REY:
                continue
            
            for tmp_pieza in self.__piezas[color_atacante][pieza].keys():
                
                cantidad_de_objetivos = 0
                ataca = False
                for tmp_objetivo in self.__piezas[color_atacante][pieza][tmp_pieza][Casilla.ATACA]:

                    if tmp_objetivo in self.__piezas[color][Pieza.REY][Casilla.ZONA_DEL_REY]:
                        cantidad_de_objetivos += 1
                        ataca = True
                        
                if pieza == Pieza.CABALLO or pieza == Pieza.ALFIL:
                    potencia_de_ataque = 20
                elif pieza == Pieza.TORRE:
                    potencia_de_ataque = 40
                elif pieza == Pieza.DAMA:
                    potencia_de_ataque = 80

                valor_del_ataque += cantidad_de_objetivos * potencia_de_ataque

                if ataca:
                    cantidad_de_atacantes += 1
        if cantidad_de_atacantes == 0:
            return 0
        else:
            return valor_del_ataque * self.__valores_de_evaluacion[TipoEvaluacion.ATAQUE_AL_REY][cantidad_de_atacantes] / 100


    def __control_del_centro(self):

        return

    def evaluacion_del_juego(self):
        puntuacion = 0
        ## f(P)= 20000(K-K') + 900(Q-Q') + 500(R-R') + 330(B-B') + 320(N-N') + 100(P-P') - 50(D-D'+S-S'+I-I') + 10(M-M')
        ##
        for i in range(0,6):
            self.valor_material += self.valor_de_piezas[i] * ( self.piezas_blancas[i] - self.piezas_negras[i] )
        
        #posibles_movimientos = self.generar_posibles_movimientos()
        #valor_de_movilidad = 10 * (obtener_movimientos_legales(tablero,posibles_movimientos,'B') - obtener_movimientos_legales(tablero,posibles_movimientos,'N'))

        # estados_de_peon = self.obtener_estados_de_peon()
        # peones_blancos = estados_de_peon[0]
        # peones_negros = estados_de_peon[1]

        # valor_de_estados_de_peon = 0
        # for i in range(0,3):
        #     valor_de_estados_de_peon = -50 * ( peones_blancos[i] - peones_negros[i] )
        
        #puntuacion = valor_material + valor_de_estados_de_peon + valor_de_movilidad
        puntuacion = self.valor_material # + valor_de_estados_de_peon + valor_de_movilidad
        return puntuacion

    ## Devuelve la cantidad de piezas del tablero
    ## [ [0,0,0,0,0,0],[0,0,0,0,0,0] ]
    # def obtener_piezas(self):
    #     for fila in range(0,8):
    #         for columna in range(0,8):
    #             posicion_tmp = Posicion.Posicion(fila,columna)
    #             casilla_objetivo = self.obtener_pieza_de_casilla(posicion_tmp)
    #             if casilla_objetivo == 0:
    #                 continue
    #             elif casilla_objetivo > 0:
    #                 self.contador_de_piezas[0][casilla_objetivo-1] += 1
    #             else:
    #                 self.contador_de_piezas[1][abs(casilla_objetivo)-1] += 1

# def es_peon_aislado(tablero,posicion):
#     fila = posicion[0]
#     columna = posicion[1]

#     for i in range(fila-1,fila+2):
#         for j in range(columna-1,columna+2):

#             if validar_posicion([i,j]) and [i,j] != posicion:
#                 casilla_objetivo = obtener_pieza_de_casilla(tablero,[i,j])
#                 if casilla_objetivo != 0:
#                     return False
#     return True

# def es_peon_atrasado(tablero,posicion):
#     fila = posicion[0]
#     columna = posicion[1]
#     color_de_pieza = obtener_color_de_pieza(tablero,posicion)
#     atrasado = 0
    
#     for i in range(fila-1,fila+2):
#         for j in range(columna-1,columna+2):

#             if validar_posicion([i,j]) and [i,j] != posicion:
#                 casilla_objetivo = obtener_pieza_de_casilla(tablero,[i,j])   

#                 if color_de_pieza == 'B':
#                     if i == fila-1:

#                         if j == columna-1 or j == columna+1:
#                             if casilla_objetivo == 0:
#                                 continue
#                             elif casilla_objetivo == 1:
#                                 atrasado += 1
#                             else:
#                                 return False
#                         else:
#                             if casilla_objetivo != 0:
#                                 return False
#                     else:
#                         if casilla_objetivo != 0:
#                             return False
#                 else:
#                     if i == fila+1:

#                         if j == columna-1 or j == columna+1:
#                             if casilla_objetivo == 0:
#                                 continue
#                             elif casilla_objetivo == -1:
#                                 atrasado += 1
#                             else:
#                                 return False
#                         else:
#                             if casilla_objetivo != 0:
#                                 return False
#                     else:
#                         if casilla_objetivo != 0:
#                             return False
#     if atrasado > 0:
#         return True
#     return False


# def es_peon_doble(tablero,posicion):
#     fila = posicion[0]
#     columna = posicion[1]
#     color_de_pieza = obtener_color_de_pieza(tablero,posicion)
#     doble = 0
    
#     for i in range(fila-1,fila+2):
#         for j in range(columna-1,columna+2):

#             if validar_posicion([i,j]) and [i,j] != posicion:
#                 casilla_objetivo = obtener_pieza_de_casilla(tablero,[i,j])   

#                 if color_de_pieza == 'B':
#                     if i == fila-1:

#                         if j == columna:
#                             if casilla_objetivo == 0:
#                                 return False
#                             elif casilla_objetivo == 1:
#                                 doble += 1
#                             else:
#                                 return False
#                         else:
#                             if casilla_objetivo != 0:
#                                 return False
#                     else:
#                         if casilla_objetivo != 0:
#                             return False
#                 else:
#                     if i == fila+1:

#                         if j == columna:
#                             if casilla_objetivo == 0:
#                                 return False
#                             elif casilla_objetivo == -1:
#                                 doble += 1
#                             else:
#                                 return False
#                         else:
#                             if casilla_objetivo != 0:
#                                 return False
#                     else:
#                         if casilla_objetivo != 0:
#                             return False
#     if doble > 0:
#         return True
#     return False

# ## Devuelve la cantidad de estados especiales de peon
# ## Revisa peones dobles, peones atrasados y peones aislados respectivamente para blancas y negras
# ## [ [0,0,0],[0,0,0]]
# def obtener_estados_de_peon(tablero):

#     estados_de_peon = [ [0,0,0] , [0,0,0] ]
#     for fila in range(0,8):
#         for columna in range(0,8):
#             casilla_objetivo = obtener_pieza_de_casilla(tablero,[fila,columna])
            
#             if casilla_objetivo == 1:
#                 if es_peon_doble(tablero,[fila,columna]):
#                     estados_de_peon[0][0] += 1
#                 elif es_peon_atrasado(tablero,[fila,columna]):
#                     estados_de_peon[0][1] += 1
#                 elif es_peon_aislado(tablero,[fila,columna]):
#                     estados_de_peon[0][2] += 1

#             elif casilla_objetivo == -1:
#                 if es_peon_doble(tablero,[fila,columna]):
#                     estados_de_peon[1][0] += 1
#                 elif es_peon_atrasado(tablero,[fila,columna]):
#                     estados_de_peon[1][1] += 1
#                 elif es_peon_aislado(tablero,[fila,columna]):
#                     estados_de_peon[1][2] += 1

#     return estados_de_peon




