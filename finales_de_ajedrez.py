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

tablero = []

## Cada pieza se representa asi [ color, tipo, columna, fila ]
## Ejm. ['B','D','a',5]
piezas_iniciales = [ ['N','R','a',8], ['B','C','c',8], ['B','D','f',8],
                     ['B','P','a',7], ['N','T','g',6], ['B','A','a',4],
                     ['N','P','g',4], ['N','A','g',3], ['B','T','b',2],
                     ['B','R','b',1]]

## Genera un vector de 64 espacios vacios representados por 0
## Representa el tablero del juego
def generar_tablero_inicial_vacio():
    global tablero
    for i in range(0,64):
        tablero.append(0)
    return

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
    posicion_real = [ 8 - representacion[1] , posible_y[ representacion[0] ] ]
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

def validar_posicion(posicion):
    return not (posicion[0] < 0 or posicion[0] > 7 or posicion[1] < 0 or posicion[1] > 7)

## Calcula el indice de una posicion del tablero
## Recibe una posicion (fila, columna)
## Devuelve un entero con el indice
def calcular_posicion_tablero(posicion):
    #print(posicion[0])
    #print(posicion[1])
    i = 8*posicion[0] + posicion[1]
    #print(i)
    return i

def obtener_pieza_de_casilla(tablero,posicion):
    return tablero[calcular_posicion_tablero(posicion)]

def colocar_pieza_en_casilla(tablero,pieza,posicion):
    tablero[calcular_posicion_tablero(posicion)] = pieza
    return tablero

def imprimir_tablero():
    global tablero
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

def colocar_piezas_iniciales_en_tablero():
    global tablero, piezas_iniciales
    tablero_con_piezas = tablero
    for i in range(0,len(piezas_iniciales)):
        pieza_real = [ piezas_iniciales[i][0], piezas_iniciales[i][1] ]
        posicion_real = [ piezas_iniciales[i][2], piezas_iniciales[i][3] ]
        posicion = convertir_posicion_real_a_representacion(posicion_real)
        pieza_tablero = convertir_pieza_real_a_pieza_tablero(pieza_real)
        colocar_pieza_en_casilla(tablero_con_piezas,pieza_tablero,posicion)
    tablero = tablero_con_piezas
    return


def obtener_color_de_pieza(tablero,posicion):
    pieza = obtener_pieza_de_casilla(tablero,posicion)
    if pieza > 0:
        return 'B'
    else:
        return 'N'
    

## Funcionalidades que describen el juego
def mover_pieza(tablero,posicion_inicial,posicion_final,pieza_de_coronamiento):
    pieza_a_mover = obtener_pieza_de_casilla(tablero,posicion_inicial)
    tablero = colocar_pieza_en_casilla(tablero,0,posicion_inicial)
    casilla_objetivo = obtener_pieza_de_casilla(tablero,posicion_final)
    if pieza_a_mover == 1 and posicion_final[0] == 0 and casilla_objetivo == 0:
        tablero = colocar_pieza_en_casilla(tablero,6,posicion_final)
    elif pieza_a_mover == -1 and posicion_final[0] == 6 and casilla_objetivo == 0:
        tablero = colocar_pieza_en_casilla(tablero,-6,posicion_final)
    else:
        tablero = colocar_pieza_en_casilla(tablero,pieza_a_mover,posicion_final)
    return tablero

def avanzar_casilla(posicion,avanzar_fila,avanzar_columna):
    return [posicion[0] + avanzar_fila, posicion[1] + avanzar_columna]

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
    

def posibles_movimientos_de_alfil(tablero,posicion):
    posibles_movimientos = posibles_movimientos_en_una_direccion(tablero,posicion,-1,-1) + posibles_movimientos_en_una_direccion(tablero,posicion,-1,1) + posibles_movimientos_en_una_direccion(tablero,posicion,1,-1) + posibles_movimientos_en_una_direccion(tablero,posicion,1,1)
    return posibles_movimientos
    
def posibles_movimientos_de_torre(tablero,posicion):
    posibles_movimientos = posibles_movimientos_en_una_direccion(tablero,posicion,-1,0) + posibles_movimientos_en_una_direccion(tablero,posicion,1,0) + posibles_movimientos_en_una_direccion(tablero,posicion,0,-1) + posibles_movimientos_en_una_direccion(tablero,posicion,0,1)
    return posibles_movimientos

def posibles_movimientos_de_dama(tablero,posicion):
    posibles_movimientos = posibles_movimientos_de_alfil(tablero,posicion) + posibles_movimientos_de_torre(tablero,posicion)
    return posibles_movimientos


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



## Verificar jaque
## verificar mov legal
## verificar movimientos legales

def hay_jaque(tablero,posibles_movimientos,turno):

    for movimiento in posibles_movimientos:
        color_de_pieza = obtener_color_de_pieza(tablero,movimiento[0])
        if color_de_pieza != turno:
            casilla_objetivo = abs(obtener_pieza_de_casilla(tablero,movimiento[1]))
            if casilla_objetivo == 6:
                return True
            

    return False

def es_movimiento_legal(tablero,movimiento,turno):

    if turno == 'B':
        pieza_de_coronamiento = 6
    else:
        pieza_de_coronamiento = -6
        
    color_de_pieza = obtener_color_de_pieza(tablero,movimiento[0])
    if color_de_pieza == turno:
        tablero_despues_de_movimiento = copy.deepcopy(tablero)
        tablero_despues_de_movimiento = mover_pieza(tablero_despues_de_movimiento,movimiento[0],movimiento[1],pieza_de_coronamiento)
        posibles_movimientos = generar_posibles_movimientos(tablero_despues_de_movimiento)
        if hay_jaque(tablero_despues_de_movimiento,posibles_movimientos,turno):
            return False
        else:
            return True
    else:
        return False

def obtener_movimientos_legales(tablero,posibles_movimientos,turno):
    movimientos_legales = []

    for movimiento in posibles_movimientos:
        if es_movimiento_legal(tablero,movimiento,turno):
            movimientos_legales.append(movimiento)
    return movimientos_legales

def hay_jaque_mate(tablero,posibles_movimientos,turno):
    movimientos_legales = obtener_movimientos_legales(tablero,posibles_movimientos,turno)
    if len(movimientos_legales) == 0:
        return True
    return False
        










    
    












        



