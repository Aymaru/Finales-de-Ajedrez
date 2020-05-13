import copy
from Juego import Posicion
from Juego import Pieza
from Juego import Movimiento

## representacion del tablero

## filas
## 8 = 0
## 7 = 1
## 6 = 2
## 5 = 3
## 4 = 4
## 3 = 5
## 2 = 6
## 1 = 7

## columnas
##  a = 0  b = 1   c = 2   d = 3   e = 4   f = 5   g = 6   h = 7

#############################################################################
## 
class Tablero:

    def __init__(self):
        self.__generar_tablero_inicial_vacio()

    def __generar_tablero_inicial_vacio(self):
        self.tablero = []
        for i in range(0,64):
            
            self.tablero.append(0)

    ####
    ##  Funciones de que permiten ver las piezas y colocarlas en el tablero. Y otras funciones auxiliares
    ####

    ## Recibe la lista de piezas iniciales en el siguiente formato:
    ##      [<c><p><col><fil>
    ##  donde:
    ##      <c> ::= {B|N}
    ##      <p> ::= {R|D|T|A|C|P}
    ##      <col> ::= {a|b|c|d|e|f|g|h}
    ##      <fil> ::= {1|2|3|4|5|6|7|8}
    ## Ejemplo: piezas_iniciales = [    ['N','R','a',8], ['B','C','c',8], ['B','D','f',8],
    ##                                  ['B','P','a',7], ['N','T','g',6], ['B','A','a',4],
    ##                                  ['N','P','g',4], ['N','A','g',3], ['B','T','b',2],
    ##                                  ['B','R','b',1] ]
    ## Devuelve el tablero con las piezas
    def colocar_piezas_iniciales(self,piezas_iniciales):
        for i in range(0,len(piezas_iniciales)):
            pieza = Pieza.Pieza(piezas_iniciales[i][0],piezas_iniciales[i][1],piezas_iniciales[i][2],piezas_iniciales[i][3])
            pieza_tablero = pieza.convertir_pieza_real_a_pieza_tablero()
            
            if pieza.posicion.validar_posicion_real():
                pieza.posicion.convertir_posicion_real_a_representacion()
            
            self.colocar_pieza_en_casilla(pieza_tablero,pieza.posicion)

    ## Recibe una posicion fila,columna Ejm.(2,1)
    ## Devuelve el valor en esa posicion del tablero
    def obtener_pieza_de_casilla(self,posicion):
        return self.tablero[posicion.calcular_posicion_tablero()]

    ## Recibe el valor de una pieza (1,2,3,4,5,6) o negativos y una posicion fila,columna Ejm. (2,1)
    ## Devuelve el tablero con la pieza en esa casilla
    def colocar_pieza_en_casilla(self,pieza,posicion):
        self.tablero[posicion.calcular_posicion_tablero()] = pieza
        
    def imprimir_tablero(self):
        etiqueta_de_fila = ['8','7','6','5','4','3','2','1']
        etiqueta_de_columna = "     a    b    c    d    e    f    g    h"
        etiqueta_de_linea_inicial = "   _______________________________________"
        etiqueta_de_linea = "  |____|____|____|____|____|____|____|____|"
        
        print(etiqueta_de_linea_inicial)
        for fila in range(0,8):
            columna = 0
            fila_por_imprimir = ""
            fila_por_imprimir += etiqueta_de_fila[fila] + " | "
            for columna in range(0,8):
                posicion = Posicion.Posicion(fila,columna)
                pieza_tablero = self.obtener_pieza_de_casilla(posicion)
                if pieza_tablero == 0:
                    fila_por_imprimir += "__"
                else:
                    if pieza_tablero > 0:
                        fila_por_imprimir += " "+str(pieza_tablero)
                    else:
                        fila_por_imprimir += str(pieza_tablero)
                fila_por_imprimir += " | "
            print(fila_por_imprimir)
            print(etiqueta_de_linea)
        print(etiqueta_de_columna)

    ## Recibe una posicion fila,columna de una pieza. Ejm (2,1)
    ## Devuelve 'B' si la pieza es blanca o 'N' si la pieza es negra
    ## En este caso las blancas se representan con numeros positivos del 1 al 6
    ## y las negras se representan con numeros negativos del 1 al 6
    def obtener_color_de_pieza(self,posicion):
        pieza = self.obtener_pieza_de_casilla(posicion)
        if pieza > 0:
            return 'B'
        return 'N'

    ####
    ##  Funcionalidades que describen el juego, mover una pieza del tablero, generar los posibles movimientos en un turno, determinar jaque y jaque mate
    ####

    ## Realiza un movimiento legal de una pieza
    ## Recibe un movimiento legal y la una pieza en caso de coronamiento
    ## Devuelve el tablero con el movimiento realizado
    ## Un movimiento legal, son todos los posibles movimientos que la posicion inicial contenga una pieza del color del jugador,
    ## es decir, si el jugador esta jugando con las blancas, la pieza debe ser un numero positivo entre 1 y 6.
    ## Y si el jugador esta jugando con las negras, la pieza debe ser un numero negativo entre 1 y 6
    ## Y recibe una pieza de coronamiento. Generalmente es una reina, -5 para las negras y 5 para las blancas  
    def mover_pieza(self,movimiento):
        
        pieza_a_mover = self.obtener_pieza_de_casilla(movimiento.casilla_inicial)
        self.limpiar_casilla(movimiento.casilla_inicial)

        self.colocar_pieza_en_casilla(pieza_a_mover,movimiento.casilla_objetivo)
    
    def es_movimiento_enrroque(self,movimiento):
        filas = [0,7]
        columnas = [2,6]
        for fila in filas:
            casilla_inicial = Posicion.Posicion(fila,4)
            for columna in columnas:
                casilla_objetivo = Posicion.Posicion(fila,columna)
                mov_tmp = Movimiento.Movimiento(casilla_inicial,casilla_objetivo)
                if mov_tmp.equals(movimiento):
                    return True

    def es_movimiento_coronacion(self,movimiento):
        pieza_a_mover = self.obtener_pieza_de_casilla(movimiento.casilla_inicial)
        
        if pieza_a_mover == 1 and movimiento.casilla_objetivo.fila == 0:
            return True
        elif pieza_a_mover == -1 and movimiento.casilla_objetivo.fila == 7:
            return True
        else:
            return False

    def realizar_coronamiento(self,movimiento,pieza_de_coronamiento):
        pieza_a_mover = self.obtener_pieza_de_casilla(movimiento.casilla_inicial)
        self.limpiar_casilla(movimiento.casilla_inicial)

        
        if pieza_a_mover == 1:
            self.colocar_pieza_en_casilla(5,movimiento.casilla_objetivo)
        elif pieza_a_mover == -1:
            self.colocar_pieza_en_casilla(-5,movimiento.casilla_objetivo)

    def realizar_enrroque(self,movimiento):
        pieza_a_mover = self.obtener_pieza_de_casilla(movimiento.casilla_inicial)
        
        self.limpiar_casilla(movimiento.casilla_inicial)
        
        self.colocar_pieza_en_casilla(pieza_a_mover,movimiento.casilla_objetivo)

        if movimiento.casilla_objetivo.columna == 2:
            posicion_torre = Posicion.Posicion(movimiento.casilla_inicial.fila,0)
            pieza_torre = self.obtener_pieza_de_casilla(posicion_torre)
            self.limpiar_casilla(posicion_torre)
            posicion_torre.columna = 3
            self.colocar_pieza_en_casilla(pieza_torre,posicion_torre)
            ##enrroque largo

        elif movimiento.casilla_objetivo.columna == 6:
            posicion_torre = Posicion.Posicion(movimiento.casilla_inicial.fila,7)
            pieza_torre = self.obtener_pieza_de_casilla(posicion_torre)
            self.limpiar_casilla(posicion_torre)
            posicion_torre.columna = 5
            self.colocar_pieza_en_casilla(pieza_torre,posicion_torre)
            ##enrroque largo


    # def obtener_casillas_atacadas(self,posibles_movimientos,turno):
    #     casillas_atacadas = []
    #     self.obtener_color_de_pieza
    #     return

    # def obtener_casillas_defendidas(self,posibles_movimientos,turno):
    #     casillas_atacadas = []
    #     self.obtener_color_de_pieza
    #     return
    
    # def obtener_casillas_amenazadas(self,posibles_movimientos,turno):
    #     casillas_amenazadas = []
        
    #     for movimiento in posibles_movimientos:
    #         color_de_pieza = self.obtener_color_de_pieza(movimiento.casilla_inicial)
    #     return

    def posibles_movimientos_de_blancas(self,posibles_movimientos):
        posibles_movimientos_blancas = []
        for movimiento in posibles_movimientos:
            if self.obtener_color_de_pieza(movimiento.casilla_inicial) == 'B':
                posibles_movimientos_blancas.append(movimiento)

        return posibles_movimientos_blancas

    def posibles_movimientos_de_negras(self,posibles_movimientos):
        posibles_movimientos_negras = []
        for movimiento in posibles_movimientos:
            if self.obtener_color_de_pieza(movimiento.casilla_inicial) == 'N':
                posibles_movimientos_negras.append(movimiento)

        return posibles_movimientos_negras
        
    def limpiar_casilla(self,posicion):
        self.colocar_pieza_en_casilla(0,posicion)

    ## Funcion auxiliar que genera todos los posibles movimientos en una direccion.
    ## Las posibles direcciones son (izquierda, derecha, arriba, abajo,
    ## diagonal superior izquierda, diagonal superior derecha, diagonal inferior izquierda, diagonal inferior derecha).
    ## Evalua casilla por casilla hasta que la posicion se salga del tablero, se encuentre una pieza enemiga o una pieza propia
    ## Si la casilla esta vacia, agrega el posible movimiento y avanza
    ## Si se encuentra una pieza propia o una posicion fuera del tablero y termina
    ## Si se encuentra una pieza enemiga, agrega el posible movimiento y termina
    ## Recibe una posicion fila,columna Ejm (2,1). y dos enteros para utilizar la funcion 'avanzar_casilla(posicion,avanzar_fila,avanzar_columna)'
    def posibles_movimientos_en_una_direccion(self,casilla_inicial,avanzar_fila,avanzar_columna):
        posibles_movimientos = []

        color_de_pieza = self.obtener_color_de_pieza(casilla_inicial)

        casilla_objetivo = Posicion.Posicion(casilla_inicial.fila,casilla_inicial.columna)
        casilla_objetivo.avanzar_casilla(avanzar_fila,avanzar_columna)
        while True:
            if not casilla_objetivo.validar_posicion():
                break
            pieza_casilla_objetivo = self.obtener_pieza_de_casilla(casilla_objetivo)

            if pieza_casilla_objetivo != 0:
                    color_casilla_objetivo = self.obtener_color_de_pieza(casilla_objetivo)
                    if color_casilla_objetivo != color_de_pieza:
                        posible_movimiento = Movimiento.Movimiento(casilla_inicial,casilla_objetivo)
                        posibles_movimientos.append(posible_movimiento)
                    break                    
            else:
                posible_movimiento = Movimiento.Movimiento(casilla_inicial,casilla_objetivo)
                posibles_movimientos.append(posible_movimiento)
                casilla_objetivo = Posicion.Posicion(casilla_objetivo.fila+avanzar_fila,casilla_objetivo.columna+avanzar_columna)
                

        return posibles_movimientos    

    ## Funcion que obtiene los posibles movimientos de un peon
    ## El peon puede moverse un campo para adelante a la vez.
    ## Si encuentra enemigos en las diagonales superiores o inferiores, dependiendo el color, puede realizar una captura
    ## Si el peon se encuentra en su posicion inicial de la partida, puede hacer una salida larga y avanzar dos espacios en vez de uno
    ## Recibe una posicion (2,1)
    ## Devuelve los posibles movimientos para el peon en esa posicion.
    def posibles_movimientos_de_peon(self,casilla_inicial):
        #print("Revisando peon en fila:%d,columna:%d",(casilla_inicial.fila,casilla_inicial.columna))
        posibles_movimientos = []
        
        color_de_pieza = self.obtener_color_de_pieza(casilla_inicial)
        if color_de_pieza == 'B':
            casilla_objetivo = Posicion.Posicion(casilla_inicial.fila-1,casilla_inicial.columna)
        else:            
            casilla_objetivo = Posicion.Posicion(casilla_inicial.fila+1,casilla_inicial.columna)

        fila_actual = casilla_objetivo.fila
        for i in range(casilla_inicial.columna-1,casilla_inicial.columna+2):
            casilla_objetivo = Posicion.Posicion(fila_actual,i)
            if not casilla_objetivo.validar_posicion():
                continue

            pieza_casilla_objetivo = self.obtener_pieza_de_casilla(casilla_objetivo)
            if i == casilla_inicial.columna:
                if pieza_casilla_objetivo == 0:
                    posible_movimiento = Movimiento.Movimiento(casilla_inicial,casilla_objetivo)
                    posibles_movimientos.append(posible_movimiento)
                    
                    if color_de_pieza == 'B' and casilla_inicial.fila == 6:
                        fila_actual = casilla_objetivo.fila
                        #casilla_objetivo.fila -= 1
                        casilla_objetivo = Posicion.Posicion(casilla_objetivo.fila-1,i)#
                        pieza_casilla_objetivo = self.obtener_pieza_de_casilla(casilla_objetivo)
                        
                        if pieza_casilla_objetivo == 0:
                            posible_movimiento = Movimiento.Movimiento(casilla_inicial,casilla_objetivo)
                            posibles_movimientos.append(posible_movimiento)
                            #print("movimiento 2 B")
                        #casilla_objetivo.fila = fila_actual

                    elif color_de_pieza == 'N' and casilla_inicial.fila == 1:
                        fila_actual = casilla_objetivo.fila
                        #casilla_objetivo.fila += 1
                        casilla_objetivo = Posicion.Posicion(casilla_objetivo.fila+1,i)#
                        pieza_casilla_objetivo = self.obtener_pieza_de_casilla(casilla_objetivo)
                        
                        if pieza_casilla_objetivo == 0:
                            posible_movimiento = Movimiento.Movimiento(casilla_inicial,casilla_objetivo)
                            posibles_movimientos.append(posible_movimiento)
                            #print("movimiento 2 N")
                        #casilla_objetivo.fila = fila_actual
            else:
                if pieza_casilla_objetivo != 0:
                    color_casilla_objetivo = self.obtener_color_de_pieza(casilla_objetivo)
                    if color_casilla_objetivo != color_de_pieza:
                        posible_movimiento = Movimiento.Movimiento(casilla_inicial,casilla_objetivo)
                        posibles_movimientos.append(posible_movimiento)
                        #print("movimiento 1")

        return posibles_movimientos
                
        
    ## Funcion que obtiene los posibles movimientos que puede realizar un alfil
    ## El alfil puede recorrer todas las diagonales.
    ## Recibe una posicion (2,1)
    ## Devuelve los posibles movimientos para el alfil en esa posicion
    def posibles_movimientos_de_alfil(self,casilla_inicial):
        posibles_movimientos = self.posibles_movimientos_en_una_direccion(casilla_inicial,-1,-1) + self.posibles_movimientos_en_una_direccion(casilla_inicial,-1,1) + self.posibles_movimientos_en_una_direccion(casilla_inicial,1,-1) + self.posibles_movimientos_en_una_direccion(casilla_inicial,1,1)
        return posibles_movimientos

    ## Funcion que obtiene los posibles movimientos que puede realizar una torre
    ## La torre puede recorrer todos los espacios posibles hacia arriba, abajo, derecha e izquierda
    ## Recibe una posicion (2,1)
    ## Devuelve los posibles movimientos para la torre en esa posicion   
    def posibles_movimientos_de_torre(self,casilla_inicial):
        posibles_movimientos = self.posibles_movimientos_en_una_direccion(casilla_inicial,-1,0) + self.posibles_movimientos_en_una_direccion(casilla_inicial,1,0) + self.posibles_movimientos_en_una_direccion(casilla_inicial,0,-1) + self.posibles_movimientos_en_una_direccion(casilla_inicial,0,1)
        return posibles_movimientos

    ## Funcion que obtiene los posibles movimientos que puede realizar una Dama
    ## la dama puede recorrer todas las direcciones, que son una combinacion de los posibles movimientos de un alfil y de una torre
    ## Recibe una posicion (2,1)
    ## Devuelve los posibles movimientos para la dama en esa posicion  
    def posibles_movimientos_de_dama(self,casilla_inicial):
        posibles_movimientos = self.posibles_movimientos_de_alfil(casilla_inicial) + self.posibles_movimientos_de_torre(casilla_inicial)
        return posibles_movimientos

    ## Funcion que obtiene los posibles movimientos que puede realizar el caballo
    ## El caballo puede avanzar en una L a cualquier direccion.
    ## Recibe una posicion (2,1)
    ## Devuelve los posibles movimientos para el caballo en esa posicion 
    
    def posibles_movimientos_de_caballo(self,casilla_inicial):
        posibles_movimientos = []
        
        color_de_pieza = self.obtener_color_de_pieza(casilla_inicial)

        unos = [-1,1]
        dos = [-2,2]

        for i in unos:
            for j in dos:
                casilla_objetivo = Posicion.Posicion(casilla_inicial.fila+i,casilla_inicial.columna+j)                
                if casilla_objetivo.validar_posicion():
                    pieza_casilla_objetivo = self.obtener_pieza_de_casilla(casilla_objetivo)
            
                    if pieza_casilla_objetivo != 0:
                        color_casilla_objetivo = self.obtener_color_de_pieza(casilla_objetivo)
                        if color_casilla_objetivo != color_de_pieza:
                            posible_movimiento = Movimiento.Movimiento(casilla_inicial,casilla_objetivo)
                            posibles_movimientos.append(posible_movimiento)
                    else:
                        posible_movimiento = Movimiento.Movimiento(casilla_inicial,casilla_objetivo)
                        posibles_movimientos.append(posible_movimiento)

        for i in dos:
            for j in unos:
                casilla_objetivo = Posicion.Posicion(casilla_inicial.fila+i,casilla_inicial.columna+j)
                if casilla_objetivo.validar_posicion():
                    pieza_casilla_objetivo = self.obtener_pieza_de_casilla(casilla_objetivo)
            
                    if pieza_casilla_objetivo != 0:
                        color_casilla_objetivo = self.obtener_color_de_pieza(casilla_objetivo)
                        if color_casilla_objetivo != color_de_pieza:
                            posible_movimiento = Movimiento.Movimiento(casilla_inicial,casilla_objetivo)
                            posibles_movimientos.append(posible_movimiento)
                    else:
                        posible_movimiento = Movimiento.Movimiento(casilla_inicial,casilla_objetivo)
                        posibles_movimientos.append(posible_movimiento)
                        
        return posibles_movimientos

    ## Funcion que obtiene los posibles movimientos que puede realizar el rey
    ## El rey puede avanzar unicamente un espacio a cualquier direccion
    ## Recibe una posicion (2,1)
    ## Devuelve los posibles movimientos para el rey en esa posicion             
    def posibles_movimientos_de_rey(self,casilla_inicial):
        posibles_movimientos = []
        
        color_de_pieza = self.obtener_color_de_pieza(casilla_inicial)

        for fila in range(casilla_inicial.fila-1,casilla_inicial.fila+2):

            for columna in range(casilla_inicial.columna-1,casilla_inicial.columna+2):
                casilla_objetivo = Posicion.Posicion(fila,columna)
                if casilla_objetivo == casilla_inicial:
                    continue
                
                if casilla_objetivo.validar_posicion():
                    pieza_casilla_objetivo = self.obtener_pieza_de_casilla(casilla_objetivo)
                    if pieza_casilla_objetivo != 0:
                            color_casilla_objetivo = self.obtener_color_de_pieza(casilla_objetivo)
                            if color_casilla_objetivo != color_de_pieza:
                                posible_movimiento = Movimiento.Movimiento(casilla_inicial,casilla_objetivo)
                                posibles_movimientos.append(posible_movimiento)
                    else:
                        posible_movimiento = Movimiento.Movimiento(casilla_inicial,casilla_objetivo)
                        posibles_movimientos.append(posible_movimiento)

        return posibles_movimientos


    ## Genera todos los posibles movimientos, de todas las piezas en un tablero
    def generar_posibles_movimientos(self):
        posibles_movimientos = []
        
        for fila in range(0,8):
            for columna in range(0,8):
                casilla_inicial = Posicion.Posicion(fila,columna)
                pieza_casilla_inicial = abs(self.obtener_pieza_de_casilla(casilla_inicial))
            
                if pieza_casilla_inicial == 1:
                    posibles_movimientos += self.posibles_movimientos_de_peon(casilla_inicial)
                elif pieza_casilla_inicial == 2:
                    posibles_movimientos += self.posibles_movimientos_de_caballo(casilla_inicial)
                elif pieza_casilla_inicial == 3:
                    posibles_movimientos += self.posibles_movimientos_de_alfil(casilla_inicial)
                elif pieza_casilla_inicial == 4:
                    posibles_movimientos += self.posibles_movimientos_de_torre(casilla_inicial)
                elif pieza_casilla_inicial == 5:
                    posibles_movimientos += self.posibles_movimientos_de_dama(casilla_inicial)
                elif pieza_casilla_inicial == 6:
                    posibles_movimientos += self.posibles_movimientos_de_rey(casilla_inicial)
                else:
                    continue
                
        return posibles_movimientos

    def generar_enrroque_blancas_corto(self,casillas_atacadas):
        ##                  |    T   |   R   |  corto   |    T   |   R   | 
        ##                      7,7     7,4       ->        7,5     7,6
        posicion_rey = Posicion.Posicion(7,4)
        posicion_torre = Posicion.Posicion(7,7)
        posicion_rey_pieza = self.obtener_pieza_de_casilla(posicion_rey)
        posicion_torre_pieza = self.obtener_pieza_de_casilla(posicion_torre)
        #print("EBC")
        if posicion_rey_pieza == 6 and posicion_torre_pieza == 4:
            #print("EBC bien las piezas")
            fila = 7
            for columna in range(5,7):
                posicion = Posicion.Posicion(fila,columna)
                pieza_de_casilla = self.obtener_pieza_de_casilla(posicion)
                if pieza_de_casilla != 0 or self.es_casilla_atacada(posicion,casillas_atacadas):
                    #print("EBC se sale pieza != 0:%d o casilla atacada",(pieza_de_casilla))
                    return None
            casilla_objetivo = Posicion.Posicion(7,6)
            movimiento = Movimiento.Movimiento(posicion_rey,casilla_objetivo)
            #print("EBC devuelve movimiento")
            return movimiento
        else:
            #print("EBC mal las piezas")
            return None

    def generar_enrroque_blancas_largo(self,casillas_atacadas):
        ##                  |    T   |   R   |  corto   |    T   |   R   | 
        ##                      7,7     7,4       ->        7,5     7,6
        posicion_rey = Posicion.Posicion(7,4)
        posicion_torre = Posicion.Posicion(7,0)
        posicion_rey_pieza = self.obtener_pieza_de_casilla(posicion_rey)
        posicion_torre_pieza = self.obtener_pieza_de_casilla(posicion_torre)
        if posicion_rey_pieza == 6 and posicion_torre_pieza == 4:
            
            fila = 7
            for columna in range(2,4):
                posicion = Posicion.Posicion(fila,columna)
                pieza_de_casilla = self.obtener_pieza_de_casilla(posicion)
                if pieza_de_casilla != 0 or self.es_casilla_atacada(posicion,casillas_atacadas):
                    return None
            casilla_objetivo = Posicion.Posicion(7,2)
            movimiento = Movimiento.Movimiento(posicion_rey,casilla_objetivo)
            return movimiento
        else:
            return None

    
    def generar_enrroque_negras_corto(self,casillas_atacadas):
        ##                  |    T   |   R   |  corto   |    T   |   R   | 
        ##                      7,7     7,4       ->        7,5     7,6
        posicion_rey = Posicion.Posicion(0,4)
        posicion_torre = Posicion.Posicion(0,7)
        posicion_rey_pieza = self.obtener_pieza_de_casilla(posicion_rey)
        posicion_torre_pieza = self.obtener_pieza_de_casilla(posicion_torre)
        if posicion_rey_pieza == -6 and posicion_torre_pieza == -4:
            
            fila = 0
            for columna in range(5,7):
                posicion = Posicion.Posicion(fila,columna)
                pieza_de_casilla = self.obtener_pieza_de_casilla(posicion)
                if pieza_de_casilla != 0 or self.es_casilla_atacada(posicion,casillas_atacadas):
                    return None
            casilla_objetivo = Posicion.Posicion(0,6)
            movimiento = Movimiento.Movimiento(posicion_rey,casilla_objetivo)
            return movimiento
        else:
            return None

    def generar_enrroque_negras_largo(self,casillas_atacadas):
        ##                  |    T   |   R   |  corto   |    T   |   R   | 
        ##                      7,7     7,4       ->        7,5     7,6
        posicion_rey = Posicion.Posicion(0,4)
        posicion_torre = Posicion.Posicion(0,0)
        posicion_rey_pieza = self.obtener_pieza_de_casilla(posicion_rey)
        posicion_torre_pieza = self.obtener_pieza_de_casilla(posicion_torre)
        if posicion_rey_pieza == -6 and posicion_torre_pieza == -4:
            
            fila = 0
            for columna in range(2,4):
                posicion = Posicion.Posicion(fila,columna)
                pieza_de_casilla = self.obtener_pieza_de_casilla(posicion)
                if pieza_de_casilla != 0 or self.es_casilla_atacada(posicion,casillas_atacadas):
                    return None
            casilla_objetivo = Posicion.Posicion(0,2)
            movimiento = Movimiento.Movimiento(posicion_rey,casilla_objetivo)
            return movimiento
        else:
            return None

    def es_casilla_atacada(self,casilla,casillas_atacadas):
        
        for casilla_atacada in casillas_atacadas:
            if casilla.equals(casilla_atacada.casilla_objetivo):
                return True
            
        return False
    
    ## Verificar si un jugador se encuentra en jaque
    ## Recibe los posibles movimientos del tablero 'generar_posibles_movimientos(tablero)'
    ## y el turno del jugador 'B' o 'N', blanco o negro respectivamente
    ## Devuelve True si se encuentra en jaque o False en caso contrario
    def hay_jaque(self,posibles_movimientos,turno):
        for movimiento in posibles_movimientos:
            color_de_pieza = self.obtener_color_de_pieza(movimiento.casilla_inicial)
            if color_de_pieza != turno:
                casilla_objetivo = abs(self.obtener_pieza_de_casilla(movimiento.casilla_objetivo))
                if casilla_objetivo == 6:
                    return True            
        return False

    ## Verifica si un movimiento es un movimiento legal
    ## Un movimiento es legal, si se mueve una pieza del color que corresponda, si juegan las blancas solo los movimientos que toquen piezas blancas son legales.
    ## Ademas, no se puede quedar en estado de jaque despues de realizar el movimiento.
    ## Recibe un movimiento ([ posicion_inicial, [posicion_final] ])
    ## Las posiciones son pares fila,columna (2,1)
    ## y el turno del jugador 'B' o 'N', blanco o negro respectivamente
    ## Devuelve True si se encuentra en jaque o False en caso contrario
    def es_movimiento_legal(self,movimiento,turno):
        if turno == 'B':
            pieza_de_coronamiento = 5
        else:
            pieza_de_coronamiento = -5
            
        color_de_pieza = self.obtener_color_de_pieza(movimiento.casilla_inicial)
        if color_de_pieza == turno:
            tablero_despues_de_mover = copy.deepcopy(self)
            #tablero_despues_de_mover.mover_pieza(movimiento,pieza_de_coronamiento)
            if tablero_despues_de_mover.es_movimiento_enrroque(movimiento):
                tablero_despues_de_mover.realizar_enrroque(movimiento)
                
            elif tablero_despues_de_mover.es_movimiento_coronacion(movimiento):
                tablero_despues_de_mover.realizar_coronamiento(movimiento,pieza_de_coronamiento)
                
            else:
                tablero_despues_de_mover.mover_pieza(movimiento)

            posibles_movimientos_despues_de_mover = tablero_despues_de_mover.generar_posibles_movimientos()
            if tablero_despues_de_mover.hay_jaque(posibles_movimientos_despues_de_mover,turno):
                return False
            else:
                return True

        return False

    ## Funcion que obtiene todos los movimientos legales para un jugador 'B' o 'N', blanco o negro respectivamente
    ## Recibe todos los movimientos posibles y el turno del jugador
    ## Devuelve la lista de movimientos legales
    def obtener_movimientos_legales(self,posibles_movimientos,turno):
        movimientos_legales = []

        for movimiento in posibles_movimientos:
            if self.es_movimiento_legal(movimiento,turno):
                movimientos_legales.append(movimiento)
        return movimientos_legales

    ## Revisa si hay jaque mate
    def hay_jaque_mate(self,movimientos_legales):
        #movimientos_legales = self.obtener_movimientos_legales(posibles_movimientos,turno) 
        # ##Creo que es mejor pasarle la lista de movimientos legales, para no tener que volver a calcularlo aqui
        if len(movimientos_legales) == 0:
            return True
        return False  

    def evaluacion_del_juego(self):
        puntuacion = 0
        ## f(P)= 20000(K-K') + 900(Q-Q') + 500(R-R') + 330(B-B') + 320(N-N') + 100(P-P') - 50(D-D'+S-S'+I-I') + 10(M-M')
        ##
        piezas = self.obtener_todas_las_piezas()
        piezas_blancas = piezas[0]
        piezas_negras = piezas[1]
        valor_de_piezas = [100,320,330,500,900,20000]
        
        valor_material = 0
        for i in range(0,6):
            valor_material += valor_de_piezas[i] * ( piezas_blancas[i] - piezas_negras[i] )
        
        #posibles_movimientos = self.generar_posibles_movimientos()
        #valor_de_movilidad = 10 * (obtener_movimientos_legales(tablero,posibles_movimientos,'B') - obtener_movimientos_legales(tablero,posibles_movimientos,'N'))

        # estados_de_peon = self.obtener_estados_de_peon()
        # peones_blancos = estados_de_peon[0]
        # peones_negros = estados_de_peon[1]

        # valor_de_estados_de_peon = 0
        # for i in range(0,3):
        #     valor_de_estados_de_peon = -50 * ( peones_blancos[i] - peones_negros[i] )
        
        #puntuacion = valor_material + valor_de_estados_de_peon + valor_de_movilidad
        puntuacion = valor_material # + valor_de_estados_de_peon + valor_de_movilidad
        return puntuacion

    ## Devuelve la cantidad de piezas del tablero
    ## [ [0,0,0,0,0,0],[0,0,0,0,0,0] ]
    def obtener_todas_las_piezas(self):
        piezas = [ [0,0,0,0,0,0], [0,0,0,0,0,0] ]
        for fila in range(0,8):
            for columna in range(0,8):
                posicion_tmp = Posicion.Posicion(fila,columna)
                casilla_objetivo = self.obtener_pieza_de_casilla(posicion_tmp)
                if casilla_objetivo == 0:
                    continue
                elif casilla_objetivo > 0:
                    piezas[0][casilla_objetivo-1] += 1
                else:
                    piezas[1][abs(casilla_objetivo)-1] += 1
        return piezas

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




