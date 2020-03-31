import copy
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
tablero = []

## Cada pieza se representa asi [ color, tipo, columna, fila ]
## Ejm. ['B','D','a',5]
piezas_iniciales = [ ['N','R','a',8], ['B','C','c',8], ['B','D','f',8],
                     ['B','P','a',7], ['N','T','g',6], ['B','A','a',4],
                     ['N','P','g',4], ['N','A','g',3], ['B','T','b',2],
                     ['B','R','b',1]]

####
##  Funciones de conversion entre el formato de entrada y el utilizado
####

## Genera un vector de 64 espacios vacios representados por 0
## Representa el tablero del juego
def generar_tablero_inicial_vacio(tablero):
    new_tablero = []
    for i in range(0,64):
        new_tablero.append(0)
    tablero = new_tablero
    return tablero

## Convierte una posicion real de ajedrez a la representacion del tablero
## Recibe una posicion real (columna, fila). Ejm (a, 4)
## Devuelve la representacion de la posicion (fila, columna). Ejm (4,0)
def convertir_posicion_real_a_representacion(posicion_real):
    posible_y = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
    representacion = [ 8 - posicion_real[1] , posible_y[ posicion_real[0] ] ]
    return representacion

## Convierte una representacion del tablero a la posicion real de ajedrez
## Recibe una representacion de la posicion (fila, columna). Ejm (4,0)
## Devuelve la posicion real (columna, fila). Ejm (a, 4)
def convertir_representacion_a_posicion_real(representacion):
    posible_y = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h'}
    posicion_real = [ posible_y[ representacion[0] ] , 8 - representacion[1] ]
    return posicion_real

## Convierte una pieza real en una pieza tablero
## Recibe una pieza real (color, tipo). Ejm (N,D)
## Devuelve la pieza tablero. Ejm -5
## P = 1
## C = 2
## A = 3
## T = 4
## D = 5
## R = 6
## Los numeros son positivos para las piezas blancas (B) y negativos para las negras (N)
def convertir_pieza_real_a_pieza_tablero(pieza_real):
    
    posible_pieza_tablero = {'P':1,'C':2,'A':3,'T':4,'D':5,'R':6}
    pieza_tablero = posible_pieza_tablero[pieza_real[1]]
    if pieza_real[0] == 'N':
        pieza_tablero *= -1
    return pieza_tablero

## Convierte una pieza real al valor correspondiente para el tablero
## Recibe una pieza tablero. Ejm -5
## Devuelve la pieza real (color, tipo). Ejm (N,D)
## 1 = P 
## 2 = C
## 3 = A
## 4 = T
## 5 = D
## 6 = R
## Los numeros son positivos para las piezas blancas (B) y negativos para las negras (N)
def convertir_pieza_tablero_a_pieza_real(pieza_tablero):
    pieza_real = []
    posible_pieza_real = {1:'P',2:'C',3:'A',4:'T',5:'D',6:'R'}
    
    if pieza_tablero < 0:
        pieza_tablero *= -1
        pieza_real = ['N',posible_pieza_real[pieza_tablero]]
    else:
        pieza_real = ['B',posible_pieza_real[pieza_tablero]]
        
    return pieza_real

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
def colocar_piezas_iniciales_en_tablero(tablero,piezas_iniciales):
    for i in range(0,len(piezas_iniciales)):
        pieza_real = [ piezas_iniciales[i][0], piezas_iniciales[i][1] ]
        posicion_real = [ piezas_iniciales[i][2], piezas_iniciales[i][3] ]
        posicion = convertir_posicion_real_a_representacion(posicion_real)
        pieza_tablero = convertir_pieza_real_a_pieza_tablero(pieza_real)
        tablero = colocar_pieza_en_casilla(tablero,pieza_tablero,posicion)
    return tablero

## Verifica que una posicion sea valida.
## Una posicion es valida si tiene el formato fila,columna. Ejm (2,1)
## y los valores se encuentran entre 0 y 7
## Devuelve True si la posicion es valida, False en caso contrario
def validar_posicion(posicion):
    return not (posicion[0] < 0 or posicion[0] > 7 or posicion[1] < 0 or posicion[1] > 7)

## Recibe un string de dos caracteres columna fila
## De la forma "a7", "d4"
def validar_posicion_real(posicion):
    columnas_validas = ['a','b','c','d','e','f','g','h']
    filas_validas = ['1','2','3','4','5','6','7','8']
    return posicion[0] in columnas_validas and posicion[1] in filas_validas

## Calcula el indice de una posicion del tablero
## Recibe una posicion (fila, columna)
## Devuelve un entero con el indice
def calcular_posicion_tablero(posicion):
    i = 8*posicion[0] + posicion[1]
    return i

## Recibe una posicion fila,columna Ejm.(2,1)
## Devuelve el valor en esa posicion del tablero
def obtener_pieza_de_casilla(tablero,posicion):
    return tablero[calcular_posicion_tablero(posicion)]

## Recibe el valor de una pieza (1,2,3,4,5,6) o negativos y una posicion fila,columna Ejm. (2,1)
## Devuelve el tablero con la pieza en esa casilla
def colocar_pieza_en_casilla(tablero,pieza,posicion):
    tablero[calcular_posicion_tablero(posicion)] = pieza
    return tablero

## imprime en consola el tablero con las piezas.
## metodo momentaneo, mientras realizamos la interfaz.
def imprimir_tablero(tablero):
    etiqueta_de_fila = ['8','7','6','5','4','3','2','1']
    etiqueta_de_columna = "     a    b    c    d    e    f    g    h"
    etiqueta_de_linea_inicial = "   _______________________________________ "
    etiqueta_de_linea = "  |____|____|____|____|____|____|____|____|"
    
    fila = 0
    print(etiqueta_de_linea_inicial)
    for fila in range(0,8):
        columna = 0
        fila_por_imprimir = ""
        fila_por_imprimir += etiqueta_de_fila[fila] + " | "
        for columna in range(0,8):
            posicion = [fila,columna]
            pieza_tablero = obtener_pieza_de_casilla(tablero,posicion)
            if pieza_tablero == 0:
                fila_por_imprimir += "__"
            else:
                pieza_real = convertir_pieza_tablero_a_pieza_real(pieza_tablero)
                fila_por_imprimir += pieza_real[0] + pieza_real[1]
            fila_por_imprimir += " | "
        print(fila_por_imprimir)
        print(etiqueta_de_linea)
    print(etiqueta_de_columna)
    return

## Recibe una posicion fila,columna de una pieza. Ejm (2,1)
## Devuelve 'B' si la pieza es blanca o 'N' si la pieza es negra
## En este caso las blancas se representan con numeros positivos del 1 al 6
## y las negras se representan con numeros negativos del 1 al 6
def obtener_color_de_pieza(tablero,posicion):
    pieza = obtener_pieza_de_casilla(tablero,posicion)
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
def mover_pieza(tablero,movimiento,pieza_de_coronamiento):
    posicion_inicial = movimiento[0]
    posicion_final = movimiento[1]
    pieza_a_mover = obtener_pieza_de_casilla(tablero,posicion_inicial)
    tablero = colocar_pieza_en_casilla(tablero,0,posicion_inicial)
    casilla_objetivo = obtener_pieza_de_casilla(tablero,posicion_final)
    if pieza_a_mover == 1 and posicion_final[0] == 0 and casilla_objetivo == 0:
        tablero = colocar_pieza_en_casilla(tablero,5,posicion_final)
    elif pieza_a_mover == -1 and posicion_final[0] == 6 and casilla_objetivo == 0:
        tablero = colocar_pieza_en_casilla(tablero,-5,posicion_final)
    else:
        tablero = colocar_pieza_en_casilla(tablero,pieza_a_mover,posicion_final)
    return tablero

## Funcion auxiliar, modifica fila,columna de una posicion a otra.
## Recibe una posicion (2,1), y dos enteros para aumentar cada uno respectivamente
## ejem avanzar_casilla((2,1),-1,+1) -> (1,2). El cual representa avanzar una casilla en la diagonal superior derecha
def avanzar_casilla(posicion,avanzar_fila,avanzar_columna):
    return [posicion[0] + avanzar_fila, posicion[1] + avanzar_columna]

## Funcion auxiliar que genera todos los posibles movimientos en una direccion.
## Las posibles direcciones son (izquierda, derecha, arriba, abajo,
## diagonal superior izquierda, diagonal superior derecha, diagonal inferior izquierda, diagonal inferior derecha).
## Evalua casilla por casilla hasta que la posicion se salga del tablero, se encuentre una pieza enemiga o una pieza propia
## Si la casilla esta vacia, agrega el posible movimiento y avanza
## Si se encuentra una pieza propia o una posicion fuera del tablero y termina
## Si se encuentra una pieza enemiga, agrega el posible movimiento y termina
## Recibe una posicion fila,columna Ejm (2,1). y dos enteros para utilizar la funcion 'avanzar_casilla(posicion,avanzar_fila,avanzar_columna)'
def posibles_movimientos_en_una_direccion(tablero,posicion,avanzar_fila,avanzar_columna):
    posibles_movimientos = []

    color_de_pieza = obtener_color_de_pieza(tablero,posicion)
    fila = posicion[0] + avanzar_fila
    columna = posicion[1] + avanzar_columna
    while True:
        if not validar_posicion([fila,columna]):
            break
        casilla_objetivo = obtener_pieza_de_casilla(tablero,[fila,columna])
        
        if casilla_objetivo != 0:
                color_casilla_objetivo = obtener_color_de_pieza(tablero,[fila,columna])
                if color_casilla_objetivo != color_de_pieza:
                    posibles_movimientos.append([posicion,[fila,columna]])
                    break
                else:
                    break
        else:
            posibles_movimientos.append([posicion,[fila,columna]])
            fila += avanzar_fila
            columna += avanzar_columna
    return posibles_movimientos
    
## Funcion que obtiene los posibles movimientos de un peon
## El peon puede moverse un campo para adelante a la vez.
## Si encuentra enemigos en las diagonales superiores o inferiores, dependiendo el color, puede realizar una captura
## Si el peon se encuentra en su posicion inicial de la partida, puede hacer una salida larga y avanzar dos espacios en vez de uno
## Recibe una posicion (2,1)
## Devuelve los posibles movimientos para el peon en esa posicion.
def posibles_movimientos_de_peon(tablero,posicion):
    posibles_movimientos = []
    
    color_de_pieza = obtener_color_de_pieza(tablero,posicion)
    if color_de_pieza == 'B':
        fila = posicion[0]-1
    else:
        fila = posicion[0]+1
        
    columna = posicion[1]

    for i in range(columna-1,columna+2):
        if not validar_posicion([fila,i]):
            continue
        casilla_objetivo = obtener_pieza_de_casilla(tablero,[fila,columna])
        if i == columna:
            if casilla_objetivo == 0:
                
                posibles_movimientos.append([posicion,[fila,columna]])
                if color_de_pieza == 'B':
                    fila_extra = fila - 1
                else:
                    fila_extra = fila + 1
                casilla_objetivo = obtener_pieza_de_casilla(tablero,[fila_extra,columna])
                
                if casilla_objetivo == 0:
                    posibles_movimientos.append([[posicion[0],columna],[fila_extra,columna]])
        else:
            if casilla_objetivo != 0:
                color_casilla_objetivo = obtener_color_de_pieza(tablero,[fila,i])
                if color_casilla_objetivo != color_de_pieza:
                    posibles_movimientos.append([posicion,[fila,i]])

    return posibles_movimientos
            
    
## Funcion que obtiene los posibles movimientos que puede realizar un alfil
## El alfil puede recorrer todas las diagonales.
## Recibe una posicion (2,1)
## Devuelve los posibles movimientos para el alfil en esa posicion
def posibles_movimientos_de_alfil(tablero,posicion):
    posibles_movimientos = posibles_movimientos_en_una_direccion(tablero,posicion,-1,-1) + posibles_movimientos_en_una_direccion(tablero,posicion,-1,1) + posibles_movimientos_en_una_direccion(tablero,posicion,1,-1) + posibles_movimientos_en_una_direccion(tablero,posicion,1,1)
    return posibles_movimientos

## Funcion que obtiene los posibles movimientos que puede realizar una torre
## La torre puede recorrer todos los espacios posibles hacia arriba, abajo, derecha e izquierda
## Recibe una posicion (2,1)
## Devuelve los posibles movimientos para la torre en esa posicion   
def posibles_movimientos_de_torre(tablero,posicion):
    posibles_movimientos = posibles_movimientos_en_una_direccion(tablero,posicion,-1,0) + posibles_movimientos_en_una_direccion(tablero,posicion,1,0) + posibles_movimientos_en_una_direccion(tablero,posicion,0,-1) + posibles_movimientos_en_una_direccion(tablero,posicion,0,1)
    return posibles_movimientos

## Funcion que obtiene los posibles movimientos que puede realizar una Dama
## la dama puede recorrer todas las direcciones, que son una combinacion de los posibles movimientos de un alfil y de una torre
## Recibe una posicion (2,1)
## Devuelve los posibles movimientos para la dama en esa posicion  
def posibles_movimientos_de_dama(tablero,posicion):
    posibles_movimientos = posibles_movimientos_de_alfil(tablero,posicion) + posibles_movimientos_de_torre(tablero,posicion)
    return posibles_movimientos

## Funcion que obtiene los posibles movimientos que puede realizar el caballo
## El caballo puede avanzar en una L a cualquier direccion.
## Recibe una posicion (2,1)
## Devuelve los posibles movimientos para el caballo en esa posicion 
 
def posibles_movimientos_de_caballo(tablero,posicion):
    posibles_movimientos = []
    
    color_de_pieza = obtener_color_de_pieza(tablero,posicion)

    unos = [-1,1]
    dos = [-2,2]

    for i in unos:
        for j in dos:
            fila = posicion[0]+i
            columna = posicion[1]+j
            if validar_posicion([fila,columna]):
                casilla_objetivo = obtener_pieza_de_casilla(tablero,[fila,columna])
        
                if casilla_objetivo != 0:
                    color_casilla_objetivo = obtener_color_de_pieza(tablero,[fila,columna])
                    if color_casilla_objetivo != color_de_pieza:
                        posibles_movimientos.append([posicion,[fila,columna]])
                else:
                    posibles_movimientos.append([posicion,[fila,columna]])

    for i in dos:
        for j in unos:
            fila = posicion[0]+i
            columna = posicion[1]+j
            if validar_posicion([fila,columna]):
                casilla_objetivo = obtener_pieza_de_casilla(tablero,[fila,columna])
        
                if casilla_objetivo != 0:
                    color_casilla_objetivo = obtener_color_de_pieza(tablero,[fila,columna])
                    if color_casilla_objetivo != color_de_pieza:
                        posibles_movimientos.append([posicion,[fila,columna]])
                else:
                    posibles_movimientos.append([posicion,[fila,columna]])
                    
    return posibles_movimientos

## Funcion que obtiene los posibles movimientos que puede realizar el rey
## El rey puede avanzar unicamente un espacio a cualquier direccion
## Recibe una posicion (2,1)
## Devuelve los posibles movimientos para el rey en esa posicion             
def posibles_movimientos_de_rey(tablero,posicion):
    posibles_movimientos = []
    
    color_de_pieza = obtener_color_de_pieza(tablero,posicion)

    for i in range(posicion[0]-1,posicion[0]+2):

        for j in range(posicion[1]-1,posicion[1]+2):
            if [i,j] == posicion:
                continue
            
            if validar_posicion([i,j]):
                casilla_objetivo = obtener_pieza_de_casilla(tablero,[i,j])
                if casilla_objetivo != 0:
                        color_casilla_objetivo = obtener_color_de_pieza(tablero,[i,j])
                        if color_casilla_objetivo != color_de_pieza:
                            posibles_movimientos.append([posicion,[i,j]])
                else:
                    posibles_movimientos.append([posicion,[i,j]])

    return posibles_movimientos


## Genera todos los posibles movimientos, de todas las piezas en un tablero
def generar_posibles_movimientos(tablero):
    posibles_movimientos = []
    
    for fila in range(0,8):
        for columna in range(0,8):
            casilla_objetivo = abs(obtener_pieza_de_casilla(tablero,[fila,columna]))
        
            if casilla_objetivo == 1:
                posibles_movimientos += posibles_movimientos_de_peon(tablero,[fila,columna])
            elif casilla_objetivo == 2:
                posibles_movimientos += posibles_movimientos_de_caballo(tablero,[fila,columna])
            elif casilla_objetivo == 3:
                posibles_movimientos += posibles_movimientos_de_alfil(tablero,[fila,columna])
            elif casilla_objetivo == 4:
                posibles_movimientos += posibles_movimientos_de_torre(tablero,[fila,columna])
            elif casilla_objetivo == 5:
                posibles_movimientos += posibles_movimientos_de_dama(tablero,[fila,columna])
            elif casilla_objetivo == 6:
                posibles_movimientos += posibles_movimientos_de_rey(tablero,[fila,columna])
            else:
                continue
            
    return posibles_movimientos



## Verificar si un jugador se encuentra en jaque
## Recibe los posibles movimientos del tablero 'generar_posibles_movimientos(tablero)'
## y el turno del jugador 'B' o 'N', blanco o negro respectivamente
## Devuelve True si se encuentra en jaque o False en caso contrario
def hay_jaque(tablero,posibles_movimientos,turno):

    for movimiento in posibles_movimientos:
        color_de_pieza = obtener_color_de_pieza(tablero,movimiento[0])
        if color_de_pieza != turno:
            casilla_objetivo = abs(obtener_pieza_de_casilla(tablero,movimiento[1]))
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
def es_movimiento_legal(tablero,movimiento,turno):

    if turno == 'B':
        pieza_de_coronamiento = 6
    else:
        pieza_de_coronamiento = -6
        
    color_de_pieza = obtener_color_de_pieza(tablero,movimiento[0])
    if color_de_pieza == turno:
        tablero_despues_de_movimiento = copy.deepcopy(tablero)
        tablero_despues_de_movimiento = mover_pieza(tablero_despues_de_movimiento,movimiento,pieza_de_coronamiento)
        posibles_movimientos = generar_posibles_movimientos(tablero_despues_de_movimiento)
        if hay_jaque(tablero_despues_de_movimiento,posibles_movimientos,turno):
            return False
        else:
            return True

    return False

## Funcion que obtiene todos los movimientos legales para un jugador 'B' o 'N', blanco o negro respectivamente
## Recibe todos los movimientos posibles y el turno del jugador
## Devuelve la lista de movimientos legales
def obtener_movimientos_legales(tablero,posibles_movimientos,turno):
    movimientos_legales = []

    for movimiento in posibles_movimientos:
        if es_movimiento_legal(tablero,movimiento,turno):
            movimientos_legales.append(movimiento)
    return movimientos_legales

## Revisa si hay jaque mate
def hay_jaque_mate(tablero,posibles_movimientos,turno):
    movimientos_legales = obtener_movimientos_legales(tablero,posibles_movimientos,turno)
    if len(movimientos_legales) == 0:
        return True
    return False

def iniciar_juego(tablero,turno,J1,J2):

    ##Pendiente el log en archivo log_partida = [log_de_tablero_inicial,log_de_movimientos]
    log_de_tablero_inicial = copy.deepcopy(tablero)
    log_de_movimientos = []

    while True:
        posibles_movimientos = generar_posibles_movimientos(tablero)
        movimientos_legales = obtener_movimientos_legales(tablero,posibles_movimientos,turno)
        if len(movimientos_legales) == 0:
            break

        jaque = hay_jaque(tablero,posibles_movimientos,turno)
        
        if turno == 'B':
            pieza_de_coronamiento = 5
        else:
            pieza_de_coronamiento = -5

        if turno == J1: ## Turno del jugador, espera que el jugador ingrese el movimiento
            print("Ingrese la casilla a mover y la casilla donde se mueve, con formato: \ncolumna fila. Ejm (a7)")
            posicion_inicial = input("Ingrese la casilla inicial: ")
            posicion_destino = input("Ingrese la casilla destino: ")
            if not(validar_posicion_real(posicion_inicial) and validar_posicion_real(posicion_destino)):
                print("Error en las posiciones ingresadas")
                continue
            
            posicion_inicial = convertir_posicion_real_a_representacion([posicion_inicial[0],posicion_inicial[1]])
            posicion_destino = convertir_posicion_real_a_representacion([posicion_destino[0],posicion_destino[1]])
            movimiento = [posicion_inicial,posicion_destino]

            tablero = mover_pieza(tablero,movimiento,pieza_de_coronamiento)
            turno = J2
        else:
            movimiento = [] ## Obtener movimiento usando minimax
            tablero = mover_pieza(tablero,movimiento,pieza_de_coronamiento)
            turno = J1

def evaluacion_del_juego(tablero,turno):
    puntuacion = 0
    ## f(P)= 20000(K-K') + 900(Q-Q') + 500(R-R') + 330(B-B') + 320(N-N') + 100(P-P') - 50(D-D'+S-S'+I-I') + 10(M-M')
    ##
    piezas = obtener_todas_las_piezas(tablero)
    piezas_blancas = piezas[0]
    piezas_negras = piezas[1]
    valor_de_piezas = [100,320,330,500,900,20000]
    
    valor_material = 0
    for i in range(0,7):
        valor_material += valor_de_piezas[i] * ( piezas_blancas[i] - piezas_negras[i] )
    
    posibles_movimientos = generar_posibles_movimientos(tablero)
    valor_de_movilidad = 10 * (obtener_movimientos_legales(tablero,posibles_movimientos,'B') - obtener_movimientos_legales(tablero,posibles_movimientos,'N'))

    estados_de_peon = obtener_estados_de_peon(tablero)
    peones_blancos = estados_de_peon[0]
    peones_negros = estados_de_peon[1]

    valor_de_estados_de_peon = 0
    for i in range(0,3):
        valor_de_estados_de_peon = -50 * ( peones_blancos[i] - peones_negros[i] )
    
    puntuacion = valor_material - valor_de_estados_de_peon + valor_de_movilidad
    return puntuacion

def es_peon_aislado(tablero,posicion):
    fila = posicion[0]
    columna = posicion[1]

    for i in range(fila-1,fila+2):
        for j in range(columna-1,columna+2):

            if validar_posicion([i,j]) and [i,j] != posicion:
                casilla_objetivo = obtener_pieza_de_casilla(tablero,[i,j])
                if casilla_objetivo != 0:
                    return False
    return True

def es_peon_atrasado(tablero,posicion):
    fila = posicion[0]
    columna = posicion[1]
    color_de_pieza = obtener_color_de_pieza(tablero,posicion)
    atrasado = 0
    
    for i in range(fila-1,fila+2):
        for j in range(columna-1,columna+2):

            if validar_posicion([i,j]) and [i,j] != posicion:
                casilla_objetivo = obtener_pieza_de_casilla(tablero,[i,j])   

                if color_de_pieza == 'B':
                    if i == fila-1:

                        if j == columna-1 or j == columna+1:
                            if casilla_objetivo == 0:
                                continue
                            elif casilla_objetivo == 1:
                                atrasado += 1
                            else:
                                return False
                        else:
                            if casilla_objetivo != 0:
                                return False
                    else:
                        if casilla_objetivo != 0:
                            return False
                else:
                    if i == fila+1:

                        if j == columna-1 or j == columna+1:
                            if casilla_objetivo == 0:
                                continue
                            elif casilla_objetivo == -1:
                                atrasado += 1
                            else:
                                return False
                        else:
                            if casilla_objetivo != 0:
                                return False
                    else:
                        if casilla_objetivo != 0:
                            return False
    if atrasado > 0:
        return True
    return False


def es_peon_doble(tablero,posicion):
    fila = posicion[0]
    columna = posicion[1]
    color_de_pieza = obtener_color_de_pieza(tablero,posicion)
    doble = 0
    
    for i in range(fila-1,fila+2):
        for j in range(columna-1,columna+2):

            if validar_posicion([i,j]) and [i,j] != posicion:
                casilla_objetivo = obtener_pieza_de_casilla(tablero,[i,j])   

                if color_de_pieza == 'B':
                    if i == fila-1:

                        if j == columna:
                            if casilla_objetivo == 0:
                                return False
                            elif casilla_objetivo == 1:
                                doble += 1
                            else:
                                return False
                        else:
                            if casilla_objetivo != 0:
                                return False
                    else:
                        if casilla_objetivo != 0:
                            return False
                else:
                    if i == fila+1:

                        if j == columna:
                            if casilla_objetivo == 0:
                                return False
                            elif casilla_objetivo == -1:
                                doble += 1
                            else:
                                return False
                        else:
                            if casilla_objetivo != 0:
                                return False
                    else:
                        if casilla_objetivo != 0:
                            return False
    if doble > 0:
        return True
    return False

## Devuelve la cantidad de estados especiales de peon
## Revisa peones dobles, peones atrasados y peones aislados respectivamente para blancas y negras
## [ [0,0,0],[0,0,0]]
def obtener_estados_de_peon(tablero):

    estados_de_peon = [ [0,0,0] , [0,0,0] ]
    for fila in range(0,8):
        for columna in range(0,8):
            casilla_objetivo = obtener_pieza_de_casilla(tablero,[fila,columna])
            
            if casilla_objetivo == 1:
                if es_peon_doble(tablero,[fila,columna]):
                    estados_de_peon[0][0] += 1
                elif es_peon_atrasado(tablero,[fila,columna]):
                    estados_de_peon[0][1] += 1
                elif es_peon_aislado(tablero,[fila,columna]):
                    estados_de_peon[0][2] += 1

            elif casilla_objetivo == -1:
                if es_peon_doble(tablero,[fila,columna]):
                    estados_de_peon[1][0] += 1
                elif es_peon_atrasado(tablero,[fila,columna]):
                    estados_de_peon[1][1] += 1
                elif es_peon_aislado(tablero,[fila,columna]):
                    estados_de_peon[1][2] += 1

    return estados_de_peon



## Devuelve la cantidad de piezas del tablero
## [ [0,0,0,0,0,0],[0,0,0,0,0,0] ]
def obtener_todas_las_piezas(tablero):
    piezas = [ [0,0,0,0,0,0], [0,0,0,0,0,0] ]
    for fila in range(0,8):
        for columna in range(0,8):
            casilla_objetivo = obtener_pieza_de_casilla(tablero,[fila,columna])
            if casilla_objetivo == 0:
                continue
            elif casilla_objetivo > 0:
                piezas[0][casilla_objetivo] += 1
            else:
                piezas[1][abs(casilla_objetivo)] += 1
    return piezas












    
    












        



