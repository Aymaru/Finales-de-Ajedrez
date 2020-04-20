import Posicion

## Cada pieza se representa asi [ color, tipo, columna, fila ]
## Ejm. ['B','D','a',5]

class Pieza:
    
    def __init__(self,color,pieza,columna,fila):
        self.color = color
        self.pieza = pieza
        self.posicion = Posicion.Posicion(fila,columna)

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
    def convertir_pieza_real_a_pieza_tablero(self):        
        posible_pieza_tablero = {'P':1,'C':2,'A':3,'T':4,'D':5,'R':6}
        pieza_tablero = posible_pieza_tablero[self.pieza]
        if self.color == 'N':
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
    # def convertir_pieza_tablero_a_pieza_real(self):
    #     pieza_real = []
    #     posible_pieza_real = {1:'P',2:'C',3:'A',4:'T',5:'D',6:'R'}
        
    #     if pieza_tablero < 0:
    #         pieza_tablero *= -1
    #         pieza_real = ['N',posible_pieza_real[pieza_tablero]]
    #     else:
    #         pieza_real = ['B',posible_pieza_real[pieza_tablero]]
            
    #     return pieza_real

