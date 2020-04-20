
# tableros_para_jugar.txt
##[ ['N','R','a',8], ['B','C','c',8], ['B','D','f',8],
##                     ['B','P','a',7], ['N','T','g',6], ['B','A','a',4],
##                     ['N','P','g',4], ['N','A','g',3], ['B','T','b',2],
##                     ['B','R','b',1]]

import os.path as path
import Pieza

#Agrega la representacion de una tablero al archivo de tableros
def escribir_linea(file,texto):
    f = open(file,"a+")
    f.write(texto+"\n")
    f.close()
    
# devuelve un arreglo de partidas
def leer_partidas(file):
    
    f = open(file,"r+")
    fl = f.read()
    f.close()
    partidas = fl.strip().split("\n")
    return partidas

def convertir_partida_en_piezas_iniciales(partida):
    piezas = partida.split(",")
    
    
    
        
game1 = "NRa8,BCc8,BDf8,BPa7,NTg6,BAa4,NPg4,NAg3,BTb2,BRb1"
inicial_game = "NTa8,NCb8,NAc8,NDd8,NRe8,NAf8,NCg8,NTh8,NPa7,NPb7,NPc7,NPd7,NPe7,NPf7,NPg7,NPh7,BTa1,BCb1,BAc1,BDd1,BRe1,BAf1,BCg1,BTh1,BPa1,BPb2,BPc2,BPd2,BPe2,BPf2,BPg2,BPh2"
file = "tableros_para_jugar.txt" 
#print(str(path.exists(file)))

