import tkinter as tk

from Juego.Posicion import Posicion
from Juego.Movimiento import Movimiento

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
            #self.posicion_inicial = Posicion.Posicion(125,49.32)
        elif abs(self.pieza) == 2:
            self.path += color_de_pieza+'C'+tipo
            #self.posicion_inicial = Posicion.Posicion(126,50.4)
        elif abs(self.pieza) == 3:
            self.path += color_de_pieza+'A'+tipo
            #self.posicion_inicial = Posicion.Posicion(126,50.3)
        elif abs(self.pieza) == 4:
            self.path += color_de_pieza+'T'+tipo
            #self.posicion_inicial = Posicion.Posicion(126,50.3)
        elif abs(self.pieza) == 5:
            self.path += color_de_pieza+'D'+tipo
            #self.posicion_inicial = Posicion.Posicion(126,50.5)
        else:
            self.path += color_de_pieza+'R'+tipo
            #self.posicion_inicial = Posicion.Posicion(127,50.5)
        self.posicion_inicial = Posicion(100,100)
        self.imagen = tk.PhotoImage(file=self.path)
        #self.imagen = self.imagen.subsample(2,2)
    
    def calcular_posicion_en_tablero(self,posicion):
        self.posicion_en_tablero = Posicion(self.posicion_inicial.fila + (posicion.fila * 100),self.posicion_inicial.columna + (posicion.columna*100))

    def colocar_posicion_en_tablero(self,posicion):
        self.posicion_en_tablero = Posicion(posicion.fila,posicion.columna)
        
    def colocar_imagen_en_tablero(self):
        self.id_canvas = self.canvas.create_image(self.posicion_en_tablero.columna,self.posicion_en_tablero.fila,image = self.imagen)
        self.canvas.pack()
    
    def resize(self,escala_fila, escala_columna):
        self.imagen = self.imagen.subsample(escala_fila,escala_columna)

    def mover_pieza(self):
        self.canvas.coords(self.id_canvas,(self.posicion_en_tablero.columna,self.posicion_en_tablero.fila))
  
    def get_posicion_en_tablero(self):
        return self.posicion_en_tablero

    def mover_casilla_en_tablero(self,direccion_fila,direccion_columna):
        self.posicion_en_tablero = Posicion(self.posicion_en_tablero.fila+100*direccion_fila,self.posicion_en_tablero.columna+100*direccion_columna)
    
    def eliminar_pieza(self):
        self.canvas.delete(self.id_canvas)

    def get_focus(self):
        self.id_canvas.configure(takefocus=True)
    #movX = posXTablero + (col-1) * 48
    #movY = posYTablero + (fila-1) * 46        

