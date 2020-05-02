import tkinter as tk

from Juego import Posicion

class Pieza():

    def __init__(self,canvas,pieza):
        self.canvas = canvas
        self.pieza = pieza
        self.cargar_imagen()

    ##Crea el path para la imagen de la pieza y carga la imagen
    def cargar_imagen(self):
        self.path = './Imagenes/'
        tipo = '.gif'
        if self.pieza > 0:
            color_de_pieza = 'B'
        else:
            color_de_pieza = 'N'

        if abs(self.pieza) == 1:
            self.path += color_de_pieza+'P'+tipo
            self.posicion_inicial = Posicion.Posicion(125,49.32)
        elif abs(self.pieza) == 2:
            self.path += color_de_pieza+'C'+tipo
            self.posicion_inicial = Posicion.Posicion(126,50.4)
        elif abs(self.pieza) == 3:
            self.path += color_de_pieza+'A'+tipo
            self.posicion_inicial = Posicion.Posicion(126,50.3)
        elif abs(self.pieza) == 4:
            self.path += color_de_pieza+'T'+tipo
            self.posicion_inicial = Posicion.Posicion(126,50.3)
        elif abs(self.pieza) == 5:
            self.path += color_de_pieza+'D'+tipo
            self.posicion_inicial = Posicion.Posicion(126,50.5)
        else:
            self.path += color_de_pieza+'R'+tipo
            self.posicion_inicial = Posicion.Posicion(127,50.5)
        
        self.imagen = tk.PhotoImage(file=self.path)
    
    def calcular_posicion_en_tablero(self,posicion):
        self.posicion_en_tablero = Posicion.Posicion(self.posicion_inicial.fila + (posicion.fila * 46),self.posicion_inicial.columna + (posicion.columna*48))

    def colocar_posicion_en_tablero(self,posicion):
        self.posicion_en_tablero = Posicion.Posicion(posicion.fila,posicion.columna)
        
    def colocar_imagen_en_tablero(self):
        self.id_canvas = self.canvas.create_image(self.posicion_en_tablero.columna,self.posicion_en_tablero.fila,image = self.imagen)
        self.canvas.pack()

    def mover_pieza(self):
        self.canvas.coords(self.id_canvas,(self.posicion_en_tablero.columna,self.posicion_en_tablero.fila))

    #movX = posXTablero + (col-1) * 48
    #movY = posYTablero + (fila-1) * 46        

