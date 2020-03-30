import math

#Segemento de Datos
dim = 8   #Dimension del tablero
pieza = ["P","T","C","A","D","R"] #P - Peon / T - Torre / C - Caballo / A - Alfil / D - Dama / R - Rey
dirr = ["DLU","DLD","DRU","DRD","U","D","L","R"]
#DLU - Diagonal Left Up / DLD - Diagonal Left Down / DRU - Diagonal Right Up / DRD - Diagonal Right Down
#U - Up / D - Down / R - Right / L - Left
mov = [[0,2,4],[4,5,6,7],[4,5,6,7],[0,1,2,3],[0,1,2,3,4,5,6,7],[0,1,2,3,4,5,6,7]] #Lista de mov disponible
#Estado del juego
tablero = [0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0]


# Retorna la posicion en el tablero (fila,columna)
def getPos(num):
    if(num%8 == 0): #LLega al final de las columnas
        return (math.ceil(num/8),8)
    else:
        return (math.ceil(num/8),num%8)

#Retorna los posibles mov (lista) en el tablero segun la pieza (todos los posibles)
def getMovs(punto,pieza):
    if (pieza == "P"):
        return getMovsPeon(punto)
    elif (pieza == "T"):
        return getMovsTorre(punto)
    elif (pieza == "C"):
        return getMovsCaballo(punto)
    elif (pieza == "A"):
        return getMovsAlfil(punto)
    elif (pieza == "D"):
        return getMovsDama(punto)
    else: #  "R"
        return getMovsRey(punto)


def getMovsPeon(punto):
    for n in range(0,len(mov[0])):
        pass

def getMovsTorre(punto):
    for n in range(0,len(mov[1])):
        pass

def getMovsCaballo(punto):
    for n in range(0,len(mov[2])):
        pass

def getMovsAlfil(punto):
    for n in range(0,len(mov[3])):
        pass

def getMovsDama(punto):
    for n in range(0,len(mov[4])):
        pass

def getMovsRey(punto):
    for n in range(0,len(mov[5])):
        pass

def getNumMovDLU(row,col): # row:++  col: --
    pass

def getNumMovDLD(row,col): # row:--  col: --
    pass

def getNumMovDRU(row,col): # row:++  col:++
    pass

def getNumMovDRD(row,col): # row:--  col:++
    pass

def getNumMovU(row,col): # row:++  col:NA
    pass

def getNumMovD(row,col): # row:--  col:NA
    pass

def getNumMovL(row,col): # row:NA  col:--
    pass

def getNumMovR(row,col): # row:NA  col:++
    pass
    

#Printea la lista de tableros 
def printTablero():
    char = " \t A \t B \t C \t D \t E \t F \t G \t H \n1"
    row = 1
    for n in range(0,len(tablero)):
        if((n+1)%8 == 0):
            row += 1
            if(len(tablero) -1 == n):
                char += "\t "+str(tablero[n])
            else:
                char += "\t "+str(tablero[n])+"\n"+str(row)
        else:
            char += "\t "+str(tablero[n])
    print(char)

#printTablero()
print(getPos(9))
