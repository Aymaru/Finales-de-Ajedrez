
class Posicion:

    def __init__(self,fila,columna):
        self.fila = fila
        self.columna = columna

   ## Convierte una posicion real de ajedrez a la representacion del tablero
    ## Recibe una posicion real (columna, fila). Ejm (a, 4)
    ## Devuelve la representacion de la posicion (fila, columna). Ejm (4,0)
    def convertir_posicion_real_a_representacion(self):
        posible_y = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
        col = posible_y[ self.columna ]
        self.fila = (8 - int(self.fila))
        self.columna = col

    ## Convierte una representacion del tablero a la posicion real de ajedrez
    ## Recibe una representacion de la posicion (fila, columna). Ejm (4,0)
    ## Devuelve la posicion real (columna, fila). Ejm (a, 4)
    # def convertir_representacion_a_posicion_real(self):
    #     posible_y = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h'}
    #     self.fila = 8 - self.columna
    #     self.columna = posible_y[self.columna]


    ## Verifica que una posicion sea valida.
    ## Una posicion es valida si tiene el formato fila,columna. Ejm (2,1)
    ## y los valores se encuentran entre 0 y 7
    ## Devuelve True si la posicion es valida, False en caso contrario
    def validar_posicion(self):
        return not (self.fila < 0 or self.fila > 7 or self.columna < 0 or self.columna > 7)

    ## Recibe un string de dos caracteres columna fila
    ## De la forma "a7", "d4"
    def validar_posicion_real(self):
        columnas_validas = ['a','b','c','d','e','f','g','h']
        filas_validas = ['1','2','3','4','5','6','7','8']
        return self.columna in columnas_validas and self.fila in filas_validas

    ## Calcula el indice de una posicion del tablero
    ## Recibe una posicion (fila, columna)
    ## Devuelve un entero con el indice
    def calcular_posicion_tablero(self):
        return  8 * self.fila + self.columna    

    ## Funcion auxiliar, modifica fila,columna de una posicion a otra.
    ## Recibe una posicion (2,1), y dos enteros para aumentar cada uno respectivamente
    ## ejem avanzar_casilla((2,1),-1,+1) -> (1,2). El cual representa avanzar una casilla en la diagonal superior derecha
    def avanzar_casilla(self,avanzar_fila,avanzar_columna):
        self.fila += avanzar_fila
        self.columna += avanzar_columna

    def equals(self,posicion):
        return (self.fila == posicion.fila and self.columna == posicion.columna )
    
    def imprimir(self):
        print("fila: %s, columna: %s" % (str(self.fila), str(self.columna)))
        
