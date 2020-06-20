import copy
from collections import deque

from Juego.Posicion import Posicion
from Juego.Tablero import Tablero
from Juego.Movimiento import Movimiento
from Juego.Tipos import Pieza
from Juego.Tipos import Casilla
from Juego.Tipos import Turno
from Juego.Tipos import TipoEvaluacion
from Juego.Tipos import EstructuraDePeon
from Juego.Tipos import FaseDeJuego

class Evaluador(Tablero):

    def __init__(self,tablero):
        super(Evaluador, self).__init__(tablero) ## Inicializa la clase madre

        ## self.__piezas y self.__casillas_vacias, en conjunto representan todas las casillas del tablero.
        ## Estructura de diccionario que guarda la informacion de las piezas del tablero
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

        ## Lista que guarda la informacion de las casillas vacias del tablero
        self.__casillas_vacias = []

        ## Deque que guarda todos los posibles movimientos del tablero
        self.__posibles_movimientos = deque()

        ## Estructura de diccionario que guarda los valores utilizados en cada evaluacion del estado del tablero
        self.__valores_de_evaluacion = {
            TipoEvaluacion.MATERIAL: {
                Pieza.PEON: 100,
                Pieza.CABALLO: 300,
                Pieza.ALFIL: 310,
                Pieza.TORRE: 500,
                Pieza.DAMA: 900,
                Pieza.REY: 20000
            },
            TipoEvaluacion.MOVILIDAD: 10,
            TipoEvaluacion.ESTRUCTURA_DE_PEONES: {
                EstructuraDePeon.AVANZADO: 10,
                EstructuraDePeon.ADELANTADO: 5,
                EstructuraDePeon.ATRASADO: -10,
                EstructuraDePeon.AISLADO: -10,
                EstructuraDePeon.DOBLADO: -5,
                EstructuraDePeon.PASADO: 10,
                EstructuraDePeon.ENCADENADO: 10,
                EstructuraDePeon.BLOQUEADO: -10,
            },
            TipoEvaluacion.CONTROL_DEL_CENTRO: {
                Pieza.PEON: 100,
                Pieza.CABALLO: 200,
                Pieza.ALFIL: 200,
                Pieza.TORRE: 400,
                Pieza.DAMA: 800,
                Pieza.REY: 50
            },
            TipoEvaluacion.ATAQUE_AL_REY: {
                1: 0.01,
                2: 0.5,
                3: 0.75,
                4: 0.88,
                5: 0.94,
                6: 0.97,
                7: 0.99
            },
            TipoEvaluacion.POSICIONAMIENTO: {
                ## Guarda la evaluacion de la posicion de una pieza en el tablero
                ## Para cada pieza en cada fase del juego hay una lista del tamaño del tablero 8x8 (64)
                ## Cada espacio de la lista representa la misma posicion del tablero 8*fila+columna
                ## El valor de posicionamiento de una pieza se obtiene con self.__get_valor_de_evaluacion_de_posicionamiento_de_pieza(fase_de_juego,posicion)
                FaseDeJuego.APERTURA: { ##Valores [50,25,10,0,-10,-25,-50]
                    Pieza.PEON: [ 0,   0,   0,   0,   0,   0,   0,   0,
                                 25,  10,  10,   0,   0,  10,  10,  25,
                                -10, -10,   0,  25,  25,   0, -10, -10,
                                -10, -10,  10,  25,  25,  10, -10, -10,
                                 10,  10,  25,  50,  50,  25,  10,  10,
                                 25,  25,  50,  50,  50,  50,  25,  25,
                                 10,  10,  10,  10,  10,  10,  10,  50,
                                 10,  10,  10,  10,  10,  10,  10,  50],
                    Pieza.CABALLO: [ -50,   0,   0,  10,  10,   0,   0, -50,
                                -50,  10,  10,   0,   0,  10,  10, -50,
                                  0,  10,   0,  25,  25,   0,  10,   0,
                                  0,  10,  50,  25,  25,  50,  10,   0,
                                 10,  10,  25,  50,  50,  25,  25,  10,
                                 25,  25,  50,  50,  50,  50,  25,  25,
                                -50, -50,  25,   0,   0,  25, -50, -50,
                                -50, -50,  25,   0,   0,  25, -50, -50],
                    Pieza.ALFIL:[   -50, -50,   0, -50, -50,   0, -50, -50,
                                    -25,   0, -10,   0,   0, -10,   0, -25,
                                     10,  10,   0,  10,  10,  25, -10,  10,
                                      0,  10,  50,  25,  25,  50, -10, -10,
                                     10,  10,  25,  50,  50,  25,  25,  10,
                                     25,  25,  50,  50,  50,  50,  25,  25,
                                    -50, -50, -50, -50, -50, -50, -50, -50,
                                    -50, -50, -50, -50, -50, -50, -50, -50],
                    Pieza.TORRE: [  -50,   0,   0,  10,  10,   0,   0, -50,
                                    -50,  10,  10,   0,   0,  10,  10, -50,
                                      0,  10,   0,  25,  25,  25, -10,  10,
                                      0,  10,  50,  25,  25,  50, -10, -10,
                                     10,  10,  25,  50,  50,  25,  25,  10,
                                     25,  25,  50,  50,  50,  50,  25,  25,
                                    -50, -50,  25,   0,   0,  25, -50, -50,
                                    -50, -50,  25,   0,   0,  25, -50, -50],
                    Pieza.DAMA: [   -50,   0,   0,  10,  10,   0,   0, -50,
                                    -50,  10,  10,   0,   0,  10,  10, -50,
                                      0,  10,   0,  25,  25,  25, -10,  10,
                                      0,  10,  50,  25,  25,  50, -10, -10,
                                     10,  10,  25,  50,  50,  25,  25,  10,
                                     25,  25,  50,  50,  50,  50,  25,  25,
                                    -50, -50,  25,   0,   0,  25, -50, -50,
                                    -50, -50,  25,   0,   0,  25, -50, -50],
                    Pieza.REY: [    -50,   0,   0,  10,  10,   0,   0, -50,
                                    -50,  10,  10,   0,   0,  10,  10, -50,
                                      0,  10,   0,  25,  25,  25, -10,  10,
                                      0,  10,  50,  25,  25,  50, -10, -10,
                                     10,  10,  25,  50,  50,  25,  25,  10,
                                     25,  25,  50,  50,  50,  50,  25,  25,
                                    -50, -50,  25,   0,   0,  25, -50, -50,
                                    -50, -50,  25,   0,   0,  25, -50, -50],
                },
                FaseDeJuego.DESARROLLO: {
                    Pieza.PEON: [0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0],
                    Pieza.CABALLO: [0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0],
                    Pieza.ALFIL: [0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0],
                    Pieza.TORRE: [0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0],
                    Pieza.DAMA: [0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0],
                    Pieza.REY: [0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0]
                },
                FaseDeJuego.FINAL: {
                    Pieza.PEON: [0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0],
                    Pieza.CABALLO: [0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0],
                    Pieza.ALFIL: [0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0],
                    Pieza.TORRE: [0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0],
                    Pieza.DAMA: [0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0],
                    Pieza.REY: [0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0]
                }
            }
        }

        ##Variables de la evaluacion del estado del tablero
        self.__valor_material = 0 ##self.__evaluacion_material()
        self.__valor_de_movilidad = 0 ##self.__evaluacion_de_movilidad()
        self.__valor_de_ataque_al_rey = 0 ##self.__evaluacion_de_ataque_al_rey
        self.__valor_de_estructura_de_peones = 0 ##self.__evaluacion_de_estructura_de_peones()
        self.__valor_de_posicionamiento = 0 ##self.__evaluacion_de_posicionamiento()
        self.__valor_de_iniciativa = 0 ##self.__evaluacion_de_iniciativa()
        self.__valor_de_control_del_centro = 0 ##self.__evaluacion_de_control_del_centro()
        
    ## **************************************************************************************************************************************************************
    ## FUNCION PRINCIPAL QUE EVALUA EL TABLERO
    ## ES LA UNICA FUNCION PUBLICA DE LA CLASE
    ## RECIBE EL TURNO DE LAS PIEZAS A EVALUAR
    ## DEVUELVE EL VALOR DE LA EVALUACION DEL ESTADO DEL TABLERO PARA LAS PIEZAS DADAS.
    ## **************************************************************************************************************************************************************

    def evaluar_tablero(self,turno):
        self.__posibles_movimientos = self.generar_posibles_movimientos()
        self.__get_piezas()
        #self.print_piezas()
        self.__get_estados_de_piezas()
        self.__evaluacion_material()
        self.__evaluacion_de_movilidad()
        self.__evaluacion_de_ataque_al_rey()
        self.__evaluacion_de_estructura_de_peones()
        self.__evaluacion_de_control_del_centro()
        #self.__evaluacion_de_posicionamiento(fase_del_juego)
        self.__evaluacion_de_iniciativa()

        fase_del_juego = self.__get_fase_del_juego()
        jaque = self.__es_jaque(self.__posibles_movimientos,turno)
        jaque_mate = self.__es_jaque_mate(jaque,turno)
        tablas = self.__es_tablas(jaque,turno)
        evaluacion = 0

        if jaque:
            evaluacion = 5000
            if turno == Turno.BLANCAS:
                evaluacion *= -1
        
        if jaque_mate:
            evaluacion = 20000
            if turno == Turno.BLANCAS:
                evaluacion *= -1 
            return evaluacion
        
        if tablas:
            evaluacion = 0
            return evaluacion

        if fase_del_juego == FaseDeJuego.APERTURA:
            self.__evaluacion_de_posicionamiento(fase_del_juego)
            self.__valor_de_ataque_al_rey = 0
            self.__valor_de_ataque_al_rey = 0.1 * self.__valor_de_control_del_centro            
            self.__valor_de_iniciativa = 0

        elif fase_del_juego == FaseDeJuego.DESARROLLO:
            self.__evaluacion_de_posicionamiento(fase_del_juego)
            self.__valor_de_ataque_al_rey = 0.3 * self.__valor_de_ataque_al_rey
            self.__valor_de_ataque_al_rey = 0.7 * self.__valor_de_control_del_centro
            self.__valor_de_iniciativa = self.__valor_de_iniciativa
            
        elif fase_del_juego == FaseDeJuego.FINAL:
            self.__evaluacion_de_posicionamiento(fase_del_juego)
            self.__valor_de_ataque_al_rey = 0.7 * self.__valor_de_ataque_al_rey
            self.__valor_de_ataque_al_rey = 0.5 * self.__valor_de_control_del_centro
            self.__valor_de_iniciativa = self.__valor_de_iniciativa
            
        else:
            return None
        
        evaluacion += self.__valor_material 
        evaluacion += self.__valores_de_evaluacion[TipoEvaluacion.MOVILIDAD] * self.__valor_de_movilidad 
        evaluacion += self.__valor_de_estructura_de_peones
        #evaluacion += self.__valor_de_posicionamiento
        evaluacion += self.__valor_de_iniciativa

        #self.print_piezas()
        # print("fase :"+str(fase_del_juego))
        # print("mat: %f" % self.__valor_material)
        # print("mov: %f" % self.__valor_de_movilidad)
        # print("ar: %f" % self.__valor_de_ataque_al_rey)
        # print("ep: %f" % self.__valor_de_estructura_de_peones)
        # #print("pos: %f" % self.__valor_de_posicionamiento)
        # print("ini: %f" % self.__valor_de_iniciativa)
        # print("cc: %f" % self.__valor_de_control_del_centro)
        # print("eval: %f" % evaluacion)
        return evaluacion

    def __es_jaque(self,posibles_movimientos,turno):
        tmp_turno = ''
        if turno == Turno.BLANCAS:
            tmp_turno = 'B'
        elif turno == Turno.NEGRAS:
            tmp_turno = 'N'        
        return self.hay_jaque(posibles_movimientos,tmp_turno)

    def __es_jaque_mate(self,jaque,turno):
        cant_movimientos_legales = self.__contar_movimientos_legales(turno)
        if jaque and cant_movimientos_legales == 0:
            return True
        else:
            return False

    def __es_tablas(self,jaque,turno):
        cant_movimientos_legales = self.__contar_movimientos_legales(turno)
        if not jaque and cant_movimientos_legales == 0:
            return True
        else:
            return False
    
    ## **************************************************************************************************************************************************************
    ## FUNCION PARA IMPRIMIR LA ESTRUCTURA DE LAS PIEZAS
    ## USADA PARA DEBUGGEAR
    ## **************************************************************************************************************************************************************
    def print_piezas(self):
        total_piezas = 0
        for color in self.__piezas.keys():
            print("Color: ", color)
            for pieza in self.__piezas[color].keys():
                print("pieza: " , pieza)

                for tmp_pieza in self.__piezas[color][pieza].keys():
                    if(type(tmp_pieza) == type(Posicion(0,0))):
                        obj_pieza = self.__get_pieza_t(color,pieza,tmp_pieza)
                        print("posicion: " , obj_pieza)
                        obj_pieza.imprimir()
                        total_piezas += 1
                        #self.print_estados_de_piezas(color,pieza,tmp_pieza)
        print("Total de piezas: %d" % total_piezas)
           
        
        return

    def print_estados_de_piezas(self,color,pieza,posicion):
        for estado in self.__piezas[color][pieza][posicion].keys():
            print("Estado : ", estado)
            for tmp_objetivo in self.__piezas[color][pieza][posicion][estado]:
                print("posicion: " , tmp_objetivo)
                tmp_objetivo.imprimir()
        return
    ## **************************************************************************************************************************************************************
    ## FUNCIONES AUXILIARES PARA LA EVALUACION DEL ESTADO DEL TABLERO
    ## **************************************************************************************************************************************************************

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
                    self.__piezas[color][pieza][posicion_tmp] = {Casilla.ATACA: [],
                                                                Casilla.DEFIENDE: [],
                                                                Casilla.AMENAZADA: [],
                                                                Casilla.ATACADA: [],
                                                                Casilla.DEFENDIDA: []}
                else:
                    self.__piezas[color][pieza][posicion_tmp] = {Casilla.ATACA: [],
                                                                Casilla.DEFIENDE: [],
                                                                Casilla.AMENAZADA: [],
                                                                Casilla.ATACADA: [],
                                                                Casilla.DEFENDIDA: []}
                
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
        if pieza == None:
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
        for rey in self.__piezas[color][Pieza.REY].keys():
            if type(rey) == type(Posicion(0,0)):
                return rey

    def __get_zona_del_rey(self,color):

        rey = self.__get_rey(color)
        if type(rey) == type(None):
            return None
        for fila in range(rey.fila-3,rey.fila+3):
            for columna in range(rey.columna-3,rey.columna+3):

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

        return contador_movimientos_legales
    
    ##Devuelve el valor de posicionamiento de una pieza en self.__valores_de_evaluacion[TipoDeEvaluacion.POSICIONAMIENTO][FaseDeJuego.?][Pieza.?][posicion]
    ##Recibe la fase del juego FaseDeJuego.INICIO / FaseDeJuego.DESARROLLO / FaseDeJuego.FINAL
    ##Y la posicion de la pieza (Debe ser una posicion de una pieza, es decir que sea una key en self.__piezas[color][pieza])
    def __get_valor_de_evaluacion_de_posicionamiento_de_pieza(self,fase_de_juego,color,pieza,posicion):
        index_posiciones = posicion.calcular_posicion_tablero()

        if color == Turno.BLANCAS:
            return self.__valores_de_evaluacion[TipoEvaluacion.POSICIONAMIENTO][fase_de_juego][pieza][index_posiciones]

        elif color == Turno.NEGRAS:
            valores_de_posicionamiento_invertida = self.__invertir_valores_de_posicionamiento_del_tablero(self.__valores_de_evaluacion[TipoEvaluacion.POSICIONAMIENTO][fase_de_juego][pieza])
            return valores_de_posicionamiento_invertida[index_posiciones]

    def __invertir_valores_de_posicionamiento_del_tablero(self,tabla):
        tabla_invertida = []
        largo_tabla = len(tabla)
        tabla_tmp = copy.deepcopy(tabla)
        for index in range(largo_tabla):
            tabla_invertida.append(tabla_tmp.pop())
        return tabla_invertida

    ##Determina la fase del juego en la que se encuentra el tablero, entre apertura, desarrollo y final
    ##Devuelve el valor del enum FaseDeJuego correspondiente.
    ##Los valores que devuelve son FaseDeJuego.APERTURA, FaseDeJuego.DESARROLLO, FaseDeJuego.FINAL
    def __get_fase_del_juego(self):
        contador_de_piezas = {}
        cantidad_de_piezas_menores_blancas = 0
        cantidad_de_piezas_menores_negras = 0

        for color in self.__piezas.keys():
            contador_de_piezas[color] = {}
            for pieza in self.__piezas[color].keys():
                contador_de_piezas[color][pieza] = len(self.__piezas[color][pieza].keys())

        cantidad_de_piezas_menores_blancas = contador_de_piezas[Turno.BLANCAS][Pieza.CABALLO] + contador_de_piezas[Turno.BLANCAS][Pieza.ALFIL] + contador_de_piezas[Turno.BLANCAS][Pieza.TORRE]
        cantidad_de_piezas_menores_negras = contador_de_piezas[Turno.NEGRAS][Pieza.CABALLO] + contador_de_piezas[Turno.NEGRAS][Pieza.ALFIL] + contador_de_piezas[Turno.NEGRAS][Pieza.TORRE]

        # print("cant dama N: %d" % contador_de_piezas[Turno.NEGRAS][Pieza.DAMA])
        if (    self.__evaluar_fase_del_juego_es_apertura( contador_de_piezas[Turno.BLANCAS][Pieza.DAMA], cantidad_de_piezas_menores_blancas, contador_de_piezas[Turno.BLANCAS][Pieza.PEON] ) and 
                self.__evaluar_fase_del_juego_es_apertura( contador_de_piezas[Turno.NEGRAS][Pieza.DAMA], cantidad_de_piezas_menores_negras, contador_de_piezas[Turno.NEGRAS][Pieza.PEON] ) ):
            return FaseDeJuego.APERTURA
        elif (  self.__evaluar_fase_del_juego_es_final( contador_de_piezas[Turno.BLANCAS][Pieza.DAMA], cantidad_de_piezas_menores_blancas ) or 
                self.__evaluar_fase_del_juego_es_final( contador_de_piezas[Turno.NEGRAS][Pieza.DAMA], cantidad_de_piezas_menores_negras ) ):
        ##Si alguno de los esta en fase final, ambos estan en fase final (EXPERIMENTAR CON AMBOS EN FASE FINAL PARA PASAR A FASE FINAL) NOTA: A la inversa con apertura
            return FaseDeJuego.FINAL
        ## Si no se encuentran en apertura ni final, es el desarrollo
        else:
            return FaseDeJuego.DESARROLLO
    
    ## **************************************************************************************************************************************************************
    ## FUNCIONES DE EVALUACION DEL ESTADO DEL TABLERO
    ## TODAS LAS FUNCIONES DE EVALUACION DE LOS DIFERENTES ANALISIS DEL TABLERO
    ## INCLUYE EVALUACION DEL MATERIAL, EVALUACION DE LA ESTRUCTURA DE LOS PEONES, EVALUACION DE OFENSIVA AL REY, EVALUACION DE MOVILIDAD,
    ## CONTROL DEL CENTRO, DOBLE ALFIL, EVALUACION DE LA POSICION DE LAS PIEZAS EN EL TABLERO SEGUN LA FASE DEL JUEGO.
    ## EL JUEGO SE DIVIDE EN TRES FASES Y LA EVALUACION CAMBIA PARA CADA FASE
    ## LAS FASES DEL JUEGO SON EL INICIO, EL DESARROLLO y EL FINAL.
    ## **************************************************************************************************************************************************************

    ##Evaluacion de material
    ##La sumatoria de la suma de la cantidad de piezas de las blancas menos las de las negras por el valor material de la pieza
    ##Deja el resultado en self.__valor_material
    def __evaluacion_material(self):

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
        
        for estructura_de_peon in self.__valores_de_evaluacion[TipoEvaluacion.ESTRUCTURA_DE_PEONES].keys():
            evaluacion = self.__valores_de_evaluacion[TipoEvaluacion.ESTRUCTURA_DE_PEONES][estructura_de_peon] * (self.__evaluar_estructura_peones(Turno.BLANCAS,estructura_de_peon) - self.__evaluar_estructura_peones(Turno.NEGRAS,estructura_de_peon)) 
            self.__valor_de_estructura_de_peones += evaluacion

    ##Evaluacion del posicionamiento de las piezas
    ##Deja el resultado en self.__valor_de_posicionamiento
    def __evaluacion_de_posicionamiento(self,fase_de_juego):
        valor_de_posicionamiento = { Turno.BLANCAS: 0 , Turno.NEGRAS: 0 }

        for color in self.__piezas.keys():
            for pieza in self.__piezas[color].keys():

                for tmp_posicion in self.__piezas[color][pieza].keys():
                    if type(tmp_posicion) != type(Posicion(0,0)):
                        continue
                    valor_de_posicionamiento[color] += self.__get_valor_de_evaluacion_de_posicionamiento_de_pieza(fase_de_juego,color,pieza,tmp_posicion)
        
        self.__valor_de_posicionamiento = valor_de_posicionamiento[Turno.BLANCAS] - valor_de_posicionamiento[Turno.NEGRAS]
        
    ##Evaluacion de la iniciativa de las piezas
    ##Para ATACA, DEFIENDE, AMENAZADA promedio
    ##Para ATACADA, DEFENDIDA el promedio del peso
    ##Deja el resultado en self.__valor_de_iniciativa
    def __evaluacion_de_iniciativa(self):   
        
        valor_de_iniciativa = { 
            Turno.BLANCAS: {
                Casilla.AMENAZADA: 0,
                Casilla.ATACA: 0,
                Casilla.DEFIENDE: 0,
                Casilla.ATACADA: 0,
                Casilla.DEFENDIDA: 0
            }, 
            Turno.NEGRAS: {
                Casilla.AMENAZADA: 0,
                Casilla.ATACA: 0,
                Casilla.DEFIENDE: 0,
                Casilla.ATACADA: 0,
                Casilla.DEFENDIDA: 0
            } 
        }
        total_de_piezas = { Turno.BLANCAS: 0, Turno.NEGRAS: 0 }
        valor = { Turno.BLANCAS: 0, Turno.NEGRAS: 0 }

        for color in self.__piezas.keys():
            for pieza in self.__piezas[color].keys():
                for tmp_pieza in self.__piezas[color][pieza].keys():
                    if type(tmp_pieza) != type(Posicion(0,0)):
                        continue
                    total_de_piezas[color] += 1

                    valor_de_iniciativa[color][Casilla.AMENAZADA] += len( self.__piezas[color][pieza][tmp_pieza][Casilla.AMENAZADA] )
                    valor_de_iniciativa[color][Casilla.ATACA] += len( self.__piezas[color][pieza][tmp_pieza][Casilla.ATACA] )
                    valor_de_iniciativa[color][Casilla.DEFIENDE] += len( self.__piezas[color][pieza][tmp_pieza][Casilla.DEFIENDE] )
                    valor_de_iniciativa[color][Casilla.ATACADA] -= len( self.__piezas[color][pieza][tmp_pieza][Casilla.ATACADA]) * (self.__valores_de_evaluacion[TipoEvaluacion.MATERIAL][pieza] / 100)
                    valor_de_iniciativa[color][Casilla.DEFENDIDA] += len( self.__piezas[color][pieza][tmp_pieza][Casilla.DEFENDIDA]) * (self.__valores_de_evaluacion[TipoEvaluacion.MATERIAL][pieza] / 100)
        
        for color in valor_de_iniciativa.keys():
            for tipo in valor_de_iniciativa[color].keys():
                if valor_de_iniciativa[color][tipo] == 0:
                    continue
                valor[color] += valor_de_iniciativa[color][tipo] #/ total_de_piezas[color]

        # print("\n*** Evaluacion de iniciativa debug ***\n")
        # print("Total de piezas blancas: %d, total de piezas negras: %d" % ( total_de_piezas[Turno.BLANCAS], total_de_piezas[Turno.NEGRAS] ) )
        # print("Valores blancas\nAMENAZADA: %d, ATACA: %d, DEFIENDE: %d, DEFENDIDA: %d, ATACADA: %d" % ( valor_de_iniciativa[Turno.BLANCAS][Casilla.AMENAZADA], valor_de_iniciativa[Turno.BLANCAS][Casilla.ATACA], valor_de_iniciativa[Turno.BLANCAS][Casilla.DEFIENDE], valor_de_iniciativa[Turno.BLANCAS][Casilla.DEFENDIDA], valor_de_iniciativa[Turno.BLANCAS][Casilla.ATACADA]))
        # print("Valores negras\nAMENAZADA: %d, ATACA: %d, DEFIENDE: %d, DEFENDIDA: %d, ATACADA: %d" % ( valor_de_iniciativa[Turno.NEGRAS][Casilla.AMENAZADA], valor_de_iniciativa[Turno.NEGRAS][Casilla.ATACA], valor_de_iniciativa[Turno.NEGRAS][Casilla.DEFIENDE], valor_de_iniciativa[Turno.NEGRAS][Casilla.DEFENDIDA], valor_de_iniciativa[Turno.NEGRAS][Casilla.ATACADA]))
        # print("Valor de piezas blancas: %f, valor de piezas negras: %f" % ( valor[Turno.BLANCAS], valor[Turno.NEGRAS] ) )
        self.__valor_de_iniciativa = valor[Turno.BLANCAS] - valor[Turno.NEGRAS]
    
    ##Evaluacion del control del centro
    ##El control del centro del tablero es muy importante en el juego
    ##El centro del tablero es el cuadrado que se forma con las casillas en las posiciones con fila,columna 2,3,4 y 5 
    ##Las esquinas del centro son las posiciones fila,columna (2,2),(2,5),(5,2),(5,5)
    ##La evaluacion para un color de piezas es la cantidad de piezas que tenga en el centro * el peso de la pieza
    ##La evaluacion del centro seria: evaluacion de blancas - evaluacion de negras
    ##Deja el resultado en self.__valor_de_control_del_centro
    def __evaluacion_de_control_del_centro(self):

        valor_de_control_del_centro = { Turno.BLANCAS: 0 , Turno.NEGRAS: 0 }

        for fila in range(2,6):
            for columna in range(2,6):
                tmp_posicion = Posicion(fila,columna)
                tmp_pieza = self.__get_pieza(tmp_posicion)
                if tmp_pieza == None:
                    continue
                else:
                    tmp_color = self.__get_color_de_pieza(tmp_posicion)
                    valor_de_control_del_centro[tmp_color] += self.__valores_de_evaluacion[TipoEvaluacion.CONTROL_DEL_CENTRO][tmp_pieza]
        
        self.__valor_de_control_del_centro = valor_de_control_del_centro[Turno.BLANCAS] - valor_de_control_del_centro[Turno.NEGRAS]

    ##Bonos
    ## bono por doble alfil
    ## bono de dama
    ## bono de torres conectadas
    
    ## **************************************************************************************************************************************************************
    ## FUNCIONES AUXILIARES DE EVALUACION DEL ESTADO DEL TABLERO
    ## **************************************************************************************************************************************************************


    def __evaluar_estructura_peones(self,color,estructura_de_peon):

        evaluacion = 0

        for tmp_peon in self.__piezas[color][Pieza.PEON].keys():
            
            if estructura_de_peon == EstructuraDePeon.ADELANTADO:
                if self.__evaluar_peon_es_adelantado(tmp_peon):
                    evaluacion += 1
                    continue   
            elif estructura_de_peon == EstructuraDePeon.AVANZADO:
                if self.__evaluar_peon_es_avanzado(tmp_peon):
                    evaluacion += 1.5
                    continue
            elif estructura_de_peon == EstructuraDePeon.AISLADO:
                if self.__evaluar_peon_es_aislado(tmp_peon):
                    evaluacion -= 1
                    continue
            elif estructura_de_peon == EstructuraDePeon.ATRASADO:
                if self.__evaluar_peon_es_atrasado(tmp_peon):
                    evaluacion -= 1
                    continue
            elif estructura_de_peon == EstructuraDePeon.DOBLADO:
                if self.__evaluar_peon_es_doblado(tmp_peon):
                    evaluacion -= 1
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
                    evaluacion -= 0.5
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
                            if tmp_pieza == Pieza.PEON:
                                return False
                        else:
                            tmp_pieza = self.__get_pieza(tmp_posicion)
                            if tmp_pieza == Pieza.PEON:
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
                        if tmp_color == None: 
                            continue
                        elif tmp_color == color_peon:
                            tmp_pieza = self.__get_pieza(tmp_posicion)
                            if tmp_pieza == Pieza.PEON:
                                return False
                        else:
                            tmp_pieza = self.__get_pieza(tmp_posicion)
                            if tmp_pieza == Pieza.PEON:
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
            
            for tmp_pieza in self.__piezas[color_atacante][pieza].keys():
                if type(tmp_pieza) != type(Posicion(0,0)):
                    continue

                cantidad_de_objetivos = 0
                ataca = False
                for tmp_objetivo in self.__piezas[color_atacante][pieza][tmp_pieza][Casilla.AMENAZADA]:
                    if tmp_objetivo in self.__piezas[color][Pieza.REY][Casilla.ZONA_DEL_REY]:
                        cantidad_de_objetivos += 1
                        ataca = True

                for tmp_objetivo in self.__piezas[color_atacante][pieza][tmp_pieza][Casilla.ATACA]:
                    if tmp_objetivo in self.__piezas[color][Pieza.REY][Casilla.ZONA_DEL_REY]:
                        cantidad_de_objetivos += 1
                        ataca = True
                
                if pieza == Pieza.PEON or pieza == Pieza.REY:
                    potencia_de_ataque = 5
                elif pieza == Pieza.CABALLO or pieza == Pieza.ALFIL:
                    potencia_de_ataque = 20
                elif pieza == Pieza.TORRE:
                    potencia_de_ataque = 40
                elif pieza == Pieza.DAMA:
                    potencia_de_ataque = 80

                valor_del_ataque += cantidad_de_objetivos * potencia_de_ataque

                if ataca or (tmp_pieza in self.__piezas[color][Pieza.REY][Casilla.ZONA_DEL_REY]):
                    cantidad_de_atacantes += 1
        if cantidad_de_atacantes == 0:
            return 0
        
        else:
            return valor_del_ataque * self.__valores_de_evaluacion[TipoEvaluacion.ATAQUE_AL_REY][cantidad_de_atacantes] / 100

    ##Evalua si la fase del juego para un jugador es apertura
    ##Es apertura si el jugador tiene una dama y
    ##tiene 6 piezas menores y 5 o mas peones
    ##o tiene 5 piezas menores y 6 o mas peones
    ##si tiene 4 o menos piezas menores o si tiene 4 peones o menos ya no es apertura
    ##Devuelve True o False, si es apertura o no respectivamente
    def __evaluar_fase_del_juego_es_apertura(self,cantidad_dama,cantidad_piezas_menores,cantidad_peones):
        if cantidad_dama == 1:
            if cantidad_piezas_menores == 6:
                if cantidad_peones >= 5:
                    return True
                else:
                    return False
            elif cantidad_piezas_menores == 5:
                if cantidad_peones >= 6:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    ##Evalua si la fase del juego para un jugador es final
    ##Es final si el jugador tiene una dama y tiene dos o menos piezas menores
    ##o si el jugador no tiene dama y tiene tres o menos piezas menores
    ##si no, no es final
    ##Devuelve True o False, si es final o no respectivamente
    def __evaluar_fase_del_juego_es_final(self,cantidad_dama,cantidad_piezas_menores):
        if cantidad_dama == 1:
            if cantidad_piezas_menores <= 2:
                return True
            else:
                return False
        else:
            if cantidad_piezas_menores <= 3:
                return True
            else:
                return False
        

