from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from time import *
import os

####Funciones Comunes####

def centrar(ventana):
    """Centra una ventana Tkinter
    """
    # Calculo del centro de la pantalla según el display.
    ventana.update_idletasks() # Actualiza desde el inicio en vez del update que lo hace despues del primer after
    # Dimension de la pantalla
    width = ventana.winfo_width()
    height = ventana.winfo_height()
    # Dimensiones de la ventana de inicio
    x = (ventana.winfo_screenwidth() // 2) - (width // 2)
    y = (ventana.winfo_screenheight() // 2) - (height // 2) -20
    ventana.geometry('{}x{}+{}+{}'.format(width, height, x, y)) # Ubico la pantalla
    return ventana


####Ventanas del Juego#####
    
class Inicio(Frame):
    """Crea la ventana de inicio con un progressbar.
    """
        ###Constructor de la clase###
    def __init__(self):
        """Crea una instancia de la clase Inicio
        """
        self.dimensiones()      # Crea una ventana inicio.
        centrar(self.inicio)    # Centra la pantalla.
        self.imagen()           # Agrega la imagen al fondo.
        self.progressBar()      # Configuracion del ProgressBar.
        self.leer_bytes()       # Aumenta los bytes del progressBar.
        
    ###Ajuste UI###
    def dimensiones(self):
        """Define los aspectos de la ventana inicio
        """
        self.inicio = Tk() 
        self.inicio.title('Instituto Tecnológico de Costa Rica')
        self.inicio.focus_set()           # Provoca que la ventana tome el focus.
        self.inicio.grab_set()            # Desabilita todas las otras ventanas hasta que esta ventana sea destruida.
        Frame.__init__(self, self.inicio) #
        self.inicio.geometry("800x600")   # Tamaño de la ventana de inicio.
        self.inicio.resizable(0,0)        # Bloquea que se cambien las dimensiones de la ventana inicio.

    def imagen(self):
        """Carga las imagenes a la ventana
        """
        self.fondo = PhotoImage(file="espera3.gif")  # Crea la imagen de fondo de la ventana inicio.
        self.lblFondo = Label(self.inicio, image=self.fondo, background='black') # Agrega la imagen en el fondo.

    ###SubComponentes de la Ventana###
    def progressBar(self):
        estiloBar = ttk.Style()
        estiloBar.theme_use('classic')
        estiloBar.configure("red.Horizontal.TProgressbar", foreground='black', background='black')
        self.progress = ttk.Progressbar(self.inicio, orient="horizontal", length=803, mode="determinate",style = "red.Horizontal.TProgressbar") # Crea una Progressbar
        self.lblFondo.grid(row=0, column=0)
        self.bytes = 0
        self.maxbytes = 1000
        self.progress["value"] = 0
        self.progress["maximum"] = 1000
        self.progress.place(x=-2, y=585) # Ubico el progressBar.

    ###Métodos especializados###
    def leer_bytes(self):
        """Lee los bytes para la Progressbar
        """
        self.bytes += 45                            # Incremeta el progressBar en 45.
        self.progress["value"] = self.bytes         # Actualizo el valor.
        if self.bytes < self.maxbytes:
            self.inicio.after(100, self.leer_bytes) #Cada 100 milisegundo realice la funcion.
        else:
            self.inicio.destroy()                   # Se destruye si el progressBar se lleno.
            Configuracion()                         # Comienza la configuración del juego.

class Configuracion(Frame):
    """Crea la ventana de configuracion de juego.
    """
    # Variables de clase
    # Cadenas de caracteres para la validación de piezas en los archivos de inicio.
    C   = "BN"
    P   = "RDTACP"
    Col = "ABCDEFGH"
    Fil = "87654321"

    ###Constructor de la clase###
    def __init__(self):
        """Crea una instancia de la clase Configuracion
        """
        self.inicioVacio = False    # El juego promociona que el/los jugador(es) carguen un archivo de inicio para mayor facilidad.  
        self.equipoJug1 = ""
        self.equipoJug2 = ""
        self.movIniciales = []
        self.configuracion = Tk()   # Crea una ventana donde estará la configuración básica de juego.
        self.dimensiones()          # Ajusta las dimensiones de la ventana.
        self.imagen()               # Agrega un fondo.
        self.botonBusqueda()        # Agrega los botones respectivos.
        self.botonesRadio()         #
        self.botonComenzar()        #
        self.botonFinalizar()       #
        self.botonEquipo()          # Color de las piezas del primer jugador(Negras/Blancas).
        centrar(self.configuracion) # Centra la pantalla.

    ###Ajuste UI###
    def dimensiones(self):
        """Define los aspectos de la ventana configuracion
        """
        self.configuracion.title('Configuración')
        self.configuracion.focus_set()           # Provoca que la ventana tome el focus
        self.configuracion.grab_set()            # Desabilita todas las otras ventanas hasta que esta ventana sea destruida
        Frame.__init__(self, self.configuracion)
        self.configuracion.geometry("400x400")   # Tamaño de la ventana de configuración.
        

    def imagen(self):
        """Carga las imagenes a la ventana
        """
        self.fondo = PhotoImage(file="fondoConfig.gif") # Crea la imagen de fondo de la ventana inicio.
        self.lblFondo = Label(self.configuracion, image=self.fondo, background='black')
        self.lblFondo.grid(row=0, column=0)

    ###SubComponentes de la Ventana###
    def botonBusqueda(self):
        """Boton que acciona la busqueda de un archivo.
        """
        self.boton = Button(self.configuracion,text = "Buscar",command= self.busquedaArchivo)
        self.boton.place(x=290,y=284)
        self.stringArchivo = StringVar()
        self.entradaArch = Entry(self.configuracion, textvariable=self.stringArchivo,width=13)
        self.entradaArch.place(x=155,y=280)

    def botonComenzar(self):
        """Boton que acciona la busqueda de un archivo.
        """
        self.boton = Button(self.configuracion,text = "Comenzar",command= self.comenzar)
        self.boton.place(x=95,y=352)

    def botonFinalizar(self):
        """Boton que acciona la busqueda de un archivo.
        """
        self.boton = Button(self.configuracion,text = "Finalizar",command= self.terminar)
        self.boton.place(x=248,y=352)

    def busquedaArchivo(self):
        """Buscar el archivo de arranca del juego.
        """
        self.archDialog = filedialog.askopenfilename(initialdir = "/", title = "Archivo de Inicio de Juego",defaultextension=".txt")
        self.stringArchivo.set(self.archDialog)

    def botonesRadio(self):
        self.valor = IntVar()
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('Wild.TRadiobutton', foreground='black')
        Radiobutton(self.configuracion, variable=self.valor, value=1,padx=0,pady=0).place(x=95,y=179)
        Radiobutton(self.configuracion, variable=self.valor, value=2,padx=0,pady=0).place(x=95,y=199)
        Radiobutton(self.configuracion, variable=self.valor, value=3,padx=0,pady=0).place(x=95,y=219)

    def botonEquipo(self):
        self.clicked = StringVar()
        self.clicked.set("Negras")
        self.equipo = OptionMenu(self.configuracion,self.clicked,"Negras","Blancas")
        self.equipo.place(x=225,y=253)
    
    ###Métodos especializados###   
    def terminar(self):
        """Finaliza el programa
        """
        self.configuracion.destroy()  # Fin del Juego.
        exit()

    def comenzar(self):
        """ Verificiamos que los paramtreos de inicio del juego esten completos y inicia 
        """
        # Verificamos los colores de los jugadores.
        if(self.clicked.get() == "Negras"):
            self.equipoJug1 = "Negras"
            self.equipoJug2 = "Blancas"
        else:
            self.equipoJug1 = "Blancas"
            self.equipoJug2 = "Negras"          
        empezar = False # El juego no comenzará hasta que cumpla con las validaciones mínimas.
        # Verificación 1: escogió un tipo de juego.
        if(self.valor.get() == 0):
            # No escogió nada.
            self.popUp(3,"[Error] ¡Debe escoger un tipo de juego!")
        else:
            # Si escogió un modo de juego.
            self.crearComponentes()     # Creación de las instancias de los objetos del juego [64 Piezas + 1 Tablero] + (AGREGAR COMPONENTE)
            # Verificamos si la caja de texto de archivo de inicio está vacía.
            if(self.stringArchivo.get() == ""):
                # No desea cargar un archivo de inicio. Estamos listos.
                #self.popUp(2,"[Aviso] ¡Deberá posicionar las fichas de\nambos jugadores antes de empezar el juego\ny luego darle el botón iniciar!")
                empezar = True
            else:
                bandera = self.cagarArchivo()
                # Si quiere cargar una partida.
                if(bandera == False):
                    # Hubo un error en el archivo.
                    self.popUp(3,"[Error] ¡Archivo Incorrecto!")
                    empezar = False
                else:
                    # Se cargará los movimientos inciales al tablero y empezar.
                    for mov in self.movIniciales:
                        self.cargarMovimientosTablero(mov)
                    empezar = True
        if(empezar == True):
            """self.componentes[0] = Piezas del Equipo 1 con su respectivo color.
               self.componentes[1] = Piezas del Equipo 2 con su respectivo color.
               self.componentes[2] = Tablero con los cuadros cargados.
               self.valor.get()    = Tipo de juego.
            """
            #self.printearTablero()
            Ajedrez(self.componentes[0],self.componentes[1],self.componentes[2],self.valor.get(),self.movIniciales)
            #Ajedrez(piezasJug1,piezasJug2,tablero,tipoJuego,movPreCargados):

    def popUp(self,tipo,mensaje):
        """Ventana que muestra un mensaje al usuario
        """
        self.pop = Toplevel()
        self.pop.focus_set()         # Provoca que la ventana tome el focus
        self.pop.grab_set()          # Desabilita todas las otras ventanas hasta que esta ventana sea destruida
        self.pop.geometry("412x138") # Tamaño de la ventana de inicio.
        if(tipo == 1):
            self.pop.title('Información')
            icono = PhotoImage(file="info.gif")           # Crea un icono de Informacion
        elif(tipo == 2):
            self.pop.title('Precaución')
            icono = PhotoImage(file="warning.gif")        # Crea un icono de Precaucion
        else:  
            self.pop.title('Error')
            icono = PhotoImage(file="error.gif")          # Crea un icono de Error
        lblIcono = Label(self.pop,image=icono, background='white')        # Agrega el icono en el fondo según el tipo de mensaje.
        boton = Button(self.pop,text = "Entendido",command = self.pop.destroy) # Opción de confirmación que entiende el mensaje. Se destruye la pantalla si se selecciona.
        boton.place(x=290,y=100)
        lblIcono.place(x=40,y=30)
        msg = Label(self.pop,text=mensaje, background='white') # Inserta el mensaje en la ventana pop.
        msg.place(x=110,y=32)
        centrar(self.pop)            # Centra la pantalla
        self.pop.wait_window()
        
    def printearTablero(self):
        tablero = self.componentes[2]
        for cuadros in tablero.cuadros:
            print(cuadros)

    def cagarArchivo(self):
        # Verifica si el cuadro de texto no es vacio.
        # Si escribió en el cuadro de texto.
        # Usabamos un try para verificar si realmente existe el documento.
        try:
            archivo = open(self.stringArchivo.get(), "r")  # Abre el archivo de inicio escrito o cargado por el jugador.
            datos = archivo.readlines()
            self.movIniciales = []
            for x in datos:
                for y in x.split():
                    if(len(y) == 5 and y[0] in Configuracion.C and
                       y[1] in Configuracion.P and y[2] in Configuracion.Fil and
                       y[3] in Configuracion.Col and y[4] in Configuracion.Fil):
                        self.movIniciales.append(y)
            self.movIniciales = list(dict.fromkeys(self.movIniciales)) # Elimino duplicados obteniendo los values del diccionario.
            if(self.movIniciales == []): # Verifica si el archivo no tenia movimientos en el formato correspondiente.
                # No ten[ia movimeintos.
                self.popUp(2,"[Error.B] ¡El archivo no posee movimientos iniciales!")
                int("AutoError")
            return True
        except:
            self.popUp(3,"Error, el archivo es incorrecto.")
            return False

    def convertirLetra(self,letra):
        """Conviertiendo la letra en el numero de columna
        """
        nueva = ''
        if(letra == 'A'):
            nueva = 1
        elif(letra == 'B'):
            nueva = 2
        elif(letra == 'C'):
            nueva = 3
        elif(letra == 'D'):
            nueva = 4
        elif(letra == 'E'):
            nueva = 5
        elif(letra == 'F'):
            nueva = 6
        elif(letra == 'G'):
            nueva = 7
        else:
            nueva = 8
        return nueva
        
    def cargarMovimientosTablero(self,mov):
        """
        """
        self.temporalC   = mov[0]           # C   = "NB"
        self.temporalP   = mov[1]           # P   = "RDTACP"
        self.temporalId  = int(mov[2])      # Id  = "12345678"
        self.temporalCol = mov[3]           # Col = "ABCDEFGH" -> "12345678"
        self.temporalFil = int(mov[4])      # Fil = "87654321"
        self.transformarInicalesAlTablero() # Procesa el movimiento

    def transformarInicalesAlTablero(self):
        """ Método que transforma la C-P-Id-Col-Fil al Tablero
        """
        # Recorremos los movimientos inciales por cada componentes para verificar cual hace match.
        if(self.temporalC == "N"):                 # Movimiento en las piezas Negras
            if(self.equipoJug1 == "Negras"):
                # Movimiento del Jugador 1
                for pieza in self.componentes[0]:  # Primero estan las Negras
                    self.agregarPieza(pieza)
            else:
                # Movimiento del Jugador 2
                for pieza in self.componentes[1]:  # Segundo estan las Blancas
                    self.agregarPieza(pieza)
        else:                                      # Movimiento en las piezas Blancas
            if(self.equipoJug1 == "Blancas"):
                # Movimiento del Jugador 1  
                for pieza in self.componentes[0]: # Primero estan las Blancas
                    self.agregarPieza(pieza)
            else:
                # Movimiento del Jugador 2
                for pieza in self.componentes[1]: # Segundo estan las Negras
                    self.agregarPieza(pieza)

    def agregarPieza(self,pieza):
        if(pieza.idChar == self.temporalP):  # Verifica la pieza
            if(pieza.id == self.temporalId): # Verifica el ID
                if(self.componentes[2].existePieza(self.temporalFil,self.convertirLetra(self.temporalCol)) == False):
                    self.componentes[2].agregarPieza(self.temporalFil,self.convertirLetra(self.temporalCol), pieza)
                else:                        # Existe una pieza previamente asignada
                    self.componentes[2].eliminarPieza(self.temporalFil,self.convertirLetra(self.temporalCol))
                    self.componentes[2].agregarPieza(self.temporalFil,self.convertirLetra(self.temporalCol), pieza)
            else:
                pass # Es la pieza, pero no con la identificación.
        else:
            pass # No es la pieza.
        
    def crearComponentes(self):
        """self.componentes = [fichasJug1 = [], fichasJug2 = [], tablero]
        """
        # Se crean/inicializan las piezas del juego de ambos jugadores.
        color = self.equipoJug1
        self.componentes = []
        fichas = []
        for jugador in [1,2]:
            fichas.append(Rey(jugador,color))
            fichas.append(Dama(jugador,color))
            for num in [1,2]:
                fichas.append(Caballo(num,jugador,color))
                fichas.append(Alfil(num,jugador,color))
                fichas.append(Torre(num,jugador,color))         
            for num in [1,2,3,4,5,6,7,8]:
                fichas.append(Peon(num,jugador,color))
            color = self.equipoJug2
            self.componentes.append(fichas)
            fichas = []  # Limpio la lista para cargar el conjunto de piezas del segundo jugador con su color respectivo
        # Se crea el tablero del juego
        self.componentes.append(Tablero(self.equipoJug1,self.equipoJug2))
        #self.printearComponentes()

    def printearComponentes(self):
        """Muestra los valores de los componentes.
        """
        for comp in range(0,3):
            print(self.componentes[comp])

class Ayuda(Frame):
    """Crea la ventana de inicio con un progressbar.
    """
        ###Constructor de la clase###
    def __init__(self):
        """Crea una instancia de la clase Inicio
        """
        self.dimensiones()      # Crea una ventana inicio.
        self.imagen()           # Agrega la imagen al fondo.'
        self.botonEntendido()
        centrar(self.ayuda)    # Centra la pantalla.
        
    ###Ajuste UI###
    def dimensiones(self):
        """Define los aspectos de la ventana inicio
        """
        self.ayuda = Toplevel() 
        self.ayuda.title('Ayuda')
        self.ayuda.focus_set()           # Provoca que la ventana tome el focus.
        Frame.__init__(self, self.ayuda) #
        self.ayuda.geometry("440x434")   # Tamaño de la ventana de inicio.
        self.ayuda.resizable(0,0)        # Bloquea que se cambien las dimensiones de la ventana inicio.

    def imagen(self):
        """Carga las imagenes a la ventana
        """
        self.fondo = PhotoImage(file="fondoAyuda.gif")  # Crea la imagen de fondo de la ventana inicio.
        self.lblFondo = Label(self.ayuda, image=self.fondo, background='black') # Agrega la imagen en el fondo.
        self.lblFondo.place(x=-1,y=-1)

    def botonEntendido(self):
        """Boton que acciona la busqueda de un archivo.
        """
        self.boton = Button(self.ayuda,text = "Entendido",command= self.ayuda.destroy)
        self.boton.place(x=64,y=395)

####Instancia Principal del Juego####         
class Ajedrez(Frame):
    """Crea la ventana de configuracion de juego.
    """

    ###Constructor de la clase###
    def __init__(self, piezasJug1,piezasJug2,tablero,tipoJuego,movPreCargados):
        """Crea una instancia de la clase Ajefrez
        """
        self.tablero = tablero           # Cuadricula con cuadros[wight,height,]
        self.piezasJug1 = piezasJug1  
        self.piezasJug2 = piezasJug2
        self.tipo = tipoJuego
        self.movPreCargados = movPreCargados
        self.principal = Toplevel()      # Crea una pantalla
        self.dimensiones()
        self.imagen()
        self.cajaResultados()
        self.botonIniciarJuego()
        self.botonRegresarCofiguracion()
        self.botonesRadio()
        self.botonAyuda()
        self.botonSiguienteJugador()
        self.entradaSiguienteMov()
        self.cargarPiezasPozo()
        self.cargarPiezasTablero()
        centrar(self.principal)
        self.principal.mainloop()
        

    ###Ajuste UI###
    def dimensiones(self):
        """Define los aspectos de la ventana principal
        """
        Frame.__init__(self, self.principal)
        self.principal.title("Instituto Tecnológico de Costa Rica")
        self.principal.geometry("801x601") # Tamaño de la ventana de inicio.
        self.canvas = Canvas(self.principal, height=601, width=801, bg = "black")
        self.canvas.pack()

    def imagen(self):
        """Carga las imagenes a la ventana
        """
        self.fondo = PhotoImage(file="Tablero.gif") # Crea la imagen de fondo de la ventana inicio.
        self.canvas.create_image(0, 0, anchor=NW, image=self.fondo)
        
    def cajaResultados(self):
        self.result = Listbox(self.principal, height=12, width=26,borderwidth=2.5,relief="raised", highlightthickness=1.5)
        self.canvas.create_window(545, 100, anchor=NW, window=self.result)
        self.result.insert(END,"            Historial de Movimientos")
        if(self.movPreCargados != []):
            self.result.insert(END,"Movimientos iniciales...")
            for i in self.movPreCargados:
                self.result.insert(END, "  "+i)
            self.result.insert(END,"Presione comenzar...")
        else:
            self.result.insert(END,"Sin movimientos inciales.")

    def botonIniciarJuego(self):
        """Boton que acciona la busqueda de un archivo.
        """
        self.boton = Button(self.principal,text = "Comenzar")
        self.canvas.create_window(566,547, anchor=NW, window=self.boton)

    def botonRegresarCofiguracion(self):
        """Boton que acciona la busqueda de un archivo.
        """
        self.boton = Button(self.principal,text = "Regresar",command= self.principal.destroy)
        self.canvas.create_window(695,547, anchor=NW, window=self.boton)

    def botonAyuda(self):
        """Boton que acciona la busqueda de un archivo.
        """
        self.boton = Button(self.principal,text = "Ayudar",command= self.mostrarAyuda)
        self.canvas.create_window(325,555, anchor=NW, window=self.boton)
    

    def botonesRadio(self):
        self.legales = IntVar()
        self.defensa = IntVar()
        self.contrataque = IntVar()
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('Wild.TRadiobutton', foreground='black')
        self.btncheck1 = Checkbutton(self.principal, variable=self.legales,padx=0,pady=0)
        self.btncheck2 = Checkbutton(self.principal, variable=self.defensa,padx=0,pady=0)
        self.btncheck3 = Checkbutton(self.principal, variable=self.contrataque,padx=0,pady=0)
        self.canvas.create_window(553,400, anchor=NW, window=self.btncheck1)
        self.canvas.create_window(553,437, anchor=NW, window=self.btncheck2)
        self.canvas.create_window(553,476, anchor=NW, window=self.btncheck3)
        
        
    def botonSiguienteJugador(self):
        self.turno = Canvas(self.principal, height=20, width=80,borderwidth=2.5,relief="sunken", highlightthickness=1.5)
        self.turnoText = "Jugador 1"
        label_resultados = self.turno.create_text(46, 15, text=self.turnoText, font="Arial 15")
        self.canvas.create_window(83,544, anchor=NW, window=self.turno)

    def entradaSiguienteMov(self):
        self.boton = Button(self.principal,text = "Aplicar")
        self.boton.place(x=350,y=548)
        self.movNuevo = StringVar()
        self.entradaArch = Entry(self.principal, textvariable=self.movNuevo,width=12)
        self.entradaArch.place(x=200,y=541)
        self.canvas.create_window(325,533, anchor=NW, window=self.boton)

    ###Métodos especializados######Métodos especializados###
    def mostrarAyuda(self):
        Ayuda()

    def cargarPiezasPozo(self):
        """ self.tablero = tablero 
            self.piezasJug1 = piezasJug1
            self.piezasJug2 = piezasJug2
            self.tipo = tipoJuego
        """
        self.imagenJ1 = []
        self.imagenJ2 = []
        acum = 0
        for pieza in self.piezasJug1:
            self.imagenJ1.append(PhotoImage(file=pieza.imagen))
            pieza.idCanvas = self.canvas.create_image(pieza.posiciones[0],pieza.posiciones[1],image=self.imagenJ1[acum])
            acum = acum + 1
        acum = 0
        for pieza in self.piezasJug2:
            self.imagenJ2.append(PhotoImage(file=pieza.imagen))
            pieza.idCanvas = self.canvas.create_image(pieza.posiciones[0],pieza.posiciones[1],image=self.imagenJ2[acum])
            acum = acum + 1
            
    def cargarPiezasTablero(self):
        for cuadro in self.tablero.cuadros:
            if(cuadro[2] != None):
                if(cuadro[2].jugador == 1):
                    for pieza in self.piezasJug1:
                        if(cuadro[2].id == pieza.id and cuadro[2].idChar == pieza.idChar):
                            print(cuadro)
                            fila = cuadro[4]
                            col = cuadro[5]
                            posXTablero = pieza.posiciones[2]
                            posYTablero = pieza.posiciones[3]
                            #print(col,posXTablero,fila,posYTablero) [posXPozo,posYPozo,posPivotXTablero,posPivotYTablero]
                            movX = posXTablero + (col-1) * 48
                            movY = posYTablero + (fila-1) * 46
                            #print(movX,movY)
                            self.canvas.coords(pieza.idCanvas,(movX,movY))
                if(cuadro[2].jugador == 2):
                    for pieza in self.piezasJug2:
                        if(cuadro[2].id == pieza.id and cuadro[2].idChar == pieza.idChar):
                            print(cuadro)
                            fila = cuadro[4]
                            col = cuadro[5]
                            posXTablero = pieza.posiciones[2]
                            posYTablero = pieza.posiciones[3]
                            #print(col,posXTablero,fila,posYTablero)
                            movX = posXTablero + (col-1) * 48
                            movY = posYTablero + (fila-1) * 46
                            #print(movX,movY)
                            self.canvas.coords(pieza.idCanvas,(movX,movY))
                        

    def calPixeles(self,puntoActual, puntoObjetivo):
        resultado = float(puntoObjetivo - puntoActual) 
        return str(resultado)


    ###SubComponentes de la Ventana###

    #Aqui botones....etc

    ###Métodos especializados###

    #Entra AYMA.
    

####Componentes#### 

class Tablero():
    """Crea una clase Tablero con los diferentes 
    """

    ###Constructor de la clase###
    def __init__(self,jugador1Equipo,jugador2Equipo):
        # Tamaño de UN cuadro.
        self.width = 64.0025    # Ancho de un cuadro.
        self.height = 61.814    # Alto de un cuadro.
        self.jugador1C = jugador1Equipo   # Color de las piezas del jugador 1 (Blancas/Negras)
        self.jugador2C = jugador2Equipo   # Color de las piezas del jugador 2 (Blancas/Negras)
        self.crearCuadros()       # Crear todos los cuadros.
        #self.printTablero()      # Mostrar.

    ###Métodos especializados###
    def crearCuadros(self):
        """ Un cuadro = [posX,poxY,pieza actual,historial,fila,columna]
        """
        self.cuadros = [] # Conjunto de cuadros del Tablero (x & y en la esquina superior).
        for fila in range (1,9):
            for columna in range (1,9):
                # Calculo de las equinas de los (64 en total)cuadros del juego.
                self.cuadros.append([17.65+((columna - 1) * 16.934),44.223 +((fila - 1) * 16.335),None,[],fila,columna])
            
    def agregarPieza(self,fila,columna,pieza):
        self.cuadros[((fila - 1)*8)+columna -1][2] = pieza
        self.cuadros[((fila - 1)*8)+columna-1][3].append(pieza)
        

    def eliminarPieza(self,fila,columna):
        self.cuadros[((fila - 1)*8)+columna-1][2] = None

    def existePieza(self,fila,columna):
        if(self.cuadros[((fila - 1)*8)+columna-1][2] == None):
            return False
        else:
            return True
    
    def printTablero(self):
        # Muestra los valores del tablero
        for x in self.cuadros:
            print(x)
        print("Total de Piezas:"+ str(len(self.cuadros)))
           
# filaY,columnaX Jug1
# ********** Peones **********
#           1                   2                    3                    4                  5                   6                7                       8
# [ [211.98 , 460.32] , [211.98 ,  485.32] , [211.98 , 510.32] , [241.38 , 460.32] , [241.38 , 485.32] , [241.38 , 510.32] , [271.02 , 475.32] , [271.02 , 495.32] ]
# ********** Caballos **********
#           1                   2
# [ [140 , 458.90] , [140 ,  511.32] ]
# ********** Alfiles **********
#           1                   2
# [ [181 , 473.32] , [181 ,  496.32] ]
# ********** Torres **********
#           1                   2
# [ [102.00 , 458.90] , [102.00 , 511.32] ]
# ********** Dama **********
#           1
# [ [140 , 485.32] ]

###########

# filaY,columnaX  ********** Jug2
# ********** Peones **********
#           1                   2                    3                    4                  5                   6                7                       8
# [ [499.98 , 460.32] , [499.98 ,  485.32] , [499.98 , 510.32] , [529.38 , 460.32] , [529.38 , 485.32] , [529.38 , 510.32] , [559.02 , 475.32] , [559.02 , 495.32] ]
# ********** Caballos **********
#           1                   2
# [ [425.90 , 458.90] , [425.90 ,  511.32] ]
# ********** Alfiles **********
#           1                   2
# [ [464.90 , 473.32] , [464.90 ,  496.32] ]
# ********** Torres **********
#           1                   2
# [ [387.90 , 458.90] , [387.90 ,  511.32] ]
# ********** Dama **********
#           1
# [ [425.9 , 485.32] ]


class Peon():
    """Crea la clase Peon para poder modificar los atributos
    """

    ###Constructor de la clase###
    def __init__(self,identificador,jugador=1,equipo="Negras"):
        self.idChar = 'P'
        self.posicionCuadro = (None,None) # Inicializa sin un cuadro
        self.jugador = jugador   # Jugador 1 or Jugador 2
        self.equipo = equipo     # Negras or Blancas
        self.id = identificador  # Peones [1,2,3,4,5,6,7,8]
        self.ponerImagen()       # Imagen del Peon
        self.posiciones = []     # [posXPozo,posYPozo,posPivotXTablero,posPivotYTablero]
        self.posicionarPozoX()   # Campo de inicio de la ficha en X
        self.posicionarPozoY()   # Campo de inicio de la ficha en Y
        self.posicionTablero()   # Posiciones en el Tablero de Inicio (se multiplica por la casilla que quiere llegar)
        self.movimientos = []    # Movimientos despues que salen del pozo hasta que los matan.
        self.idCanvas = 0        # Objeto en el Canvas que se va a mover 

    ###Ajuste UI###
    def posicionarPozoX(self):
        #Ambos jugadores
        if(self.id in [1,4]):
            self.posiciones.append(460.32)        # Peon 1 y 4 
        elif(self.id in [2,5]):
            self.posiciones.append(485.32)        # Peon 2 y 5
        elif(self.id  in [3,6]):
            self.posiciones.append(510.32)       # Peon 3 y 6
        elif(self.id == 7):
            self.posiciones.append(475.32)        # Peon 7
        else:
            self.posiciones.append(495.32)       # Peon 8


    def posicionarPozoY(self):
        # Jugador 1
        if(self.jugador == 1):
            if(1 <= self.id <= 3):
                self.posiciones.append(211.98)  # Peon 1 al 3
            elif(4 <= self.id <= 6):
                self.posiciones.append(241.38)   # Peon 4 al 6
            else:
                self.posiciones.append(271.02)  # Peon 7 y 8
        # Jugador 2
        else:
            if(1 <= self.id <= 3):
                self.posiciones.append(499.98) # Peon 1 al 3
            elif(4 <= self.id <= 6):
                self.posiciones.append(529.38) # Peon 4 al 6
            else:
                self.posiciones.append(559.02) # Peon 7 y 8
                
    def posicionTablero(self):
        self.posiciones.append(49.32) # Posicion en el eje X
        self.posiciones.append(125) # Posicion en el eje y     
            
    def ponerImagen(self):
        #Imagenes de las piezas.
        self.width =  18.57   # Ancho del Peon
        self.height = 29.14    # Alto del Peon
        if(self.equipo == "Negras"):
            self.imagen = "NP.gif"
        else:
            self.imagen = "BP.gif"

class Rey():
    """Crea la clase Rey para poder modificar los atributos
    """

    ###Constructor de la clase###
    def __init__(self,jugador=1,equipo="Negras"):
        self.idChar = 'R'
        self.jugador = jugador    # Jugador 1 o Jugador 2.
        self.equipo = equipo      # Negras o Blancas.
        self.id = 1               # Solo un Rey.
        self.ponerImagen()        # Imagen del Rey.
        self.posiciones = []      # [posXPozo,posYPozo,posPivotXTablero,posPivotYTablero]
        self.movimientos = []     # Movimientos despues que salen del pozo hasta que los matan.
        self.posicionarPozoX()    # Campo de inicio de la ficha en X.
        self.posicionarPozoY()    # Campo de inicio de la ficha en Y.
        self.posicionTablero()    # Posiciones en el Tablero de Inicio (se multiplica por la casilla que quiere llegar).
        self.idCanvas = 0         # Objeto en el Canvas que se va a mover

    ###Ajuste UI### 
    def posicionarPozoX(self):
        self.posiciones.append(485.32) 

    def posicionarPozoY(self):
        # Jugador 1.
        if(self.jugador == 1):
            self.posiciones.append(95.98)
        # Jugador 2.
        else:
            self.posiciones.append(382.32)
            
    def posicionTablero(self):
        self.posiciones.append(50.5) # Posicion en el eje X.
        self.posiciones.append(127) # Posicion en el eje Y.
            
    def ponerImagen(self):
        #Imagenes de las piezas.
        self.width =  23.84    # Ancho del Rey.
        self.height =  52.002  # Alto del Rey.
        if(self.equipo == "Negras"):
            self.imagen = "NR.gif"
        else:
            self.imagen = "BR.gif"

class Torre():
    """Crea la clase Torre para poder modificar los atributos
    """

    ###Constructor de la clase###
    def __init__(self,identificador,jugador=1,equipo="Negras"):
        self.idChar = 'T'
        self.jugador = jugador   # Jugador 1 o Jugador 2.
        self.equipo = equipo     # Negras o Blancas.
        self.id = identificador  # Torre [1,2].
        self.ponerImagen()       # Imagen del Torre.
        self.posiciones = []     # [posXPozo,posYPozo,posPivotXTablero,posPivotYTablero].
        self.posicionarPozoX()   # Campo de inicio de la ficha en X.
        self.posicionarPozoY()   # Campo de inicio de la ficha en Y.
        self.posicionTablero()   # Posiciones en el Tablero de Inicio (se multiplica por la casilla que quiere llegar).
        self.movimientos = []    # Movimientos despues que salen del pozo hasta que los matan.
        self.idCanvas = 0        # Objeto en el Canvas que se va a mover
        
    ###Ajuste UI###
    def posicionarPozoX(self):   # Se mantiene el eje X para ambos jugadores.
        if(self.id == 1):
            self.posiciones.append(458.9)  # Torre 1.
        else:
            self.posiciones.append(511.32)  # Torre 2.

    def posicionarPozoY(self):
        # Jugador 1.
        if(self.jugador == 1):
            self.posiciones.append(102)
        # Jugador 2.
        else:
            self.posiciones.append(387.9)

    def posicionTablero(self):
        self.posiciones.append(50.3) # Posicion en el eje X.
        self.posiciones.append(126) # Posicion en el eje Y.
            
    def ponerImagen(self):
        #Imagenes de las piezas.
        self.width =  23.516    # Ancho del Torre.
        self.height = 35.852    # Alto del Torre.
        if(self.equipo == "Negras"):
            self.imagen = "NT.gif"
        else:
            self.imagen = "BT.gif"

class Caballo():
    """Crea la clase Caballo para poder modificar los atributos
    """

    ###Constructor de la clase###
    def __init__(self,identificador,jugador=1,equipo="Negras"):
        self.idChar = 'C'
        self.jugador = jugador   # Jugador 1 or Jugador 2.
        self.equipo = equipo     # Negras or Blancas.
        self.id = identificador  # Caballo [1,2].
        self.ponerImagen()       # Imagen del Caballo.
        self.posiciones = []     # [posXPozo,posYPozo,posPivotXTablero,posPivotYTablero].
        self.posicionarPozoX()   # Campo de inicio de la ficha en X.
        self.posicionarPozoY()   # Campo de inicio de la ficha en Y.
        self.posicionTablero()   # Posiciones en el Tablero de Inicio (se multiplica por la casilla que quiere llegar).
        self.movimientos = []    # Movimientos despues que salen del pozo hasta que los matan.
        self.idCanvas = 0        # Objeto en el Canvas que se va a mover

    ###Ajuste UI###
    def posicionarPozoX(self):   # Se mantiene el eje X para ambos jugadores.
        if(self.id == 1):
            self.posiciones.append(458.9) # Caballo 1.
        else:
            self.posiciones.append(511.32) # Caballo 2.

    def posicionarPozoY(self):
        # Jugador 1.
        if(self.jugador == 1):
            self.posiciones.append(140)
        # Jugador 2.
        else:
            self.posiciones.append(425.9)

    def posicionTablero(self):
        self.posiciones.append(50.4) # Posicion en el eje X.
        self.posiciones.append(126) # Posicion en el eje Y.
            
    def ponerImagen(self):
        #Imagenes de las piezas.
        self.width = 26.46      # Ancho del Caballo.
        self.height = 43.079    # Alto del Caballo.
        if(self.equipo == "Negras"):
            self.imagen = "NC.gif"
        else:
            self.imagen = "BC.gif"

class Dama():
    """Crea la clase Dama para poder modificar los atributos
    """

    ###Constructor de la clase###
    def __init__(self,jugador=1,equipo="Negras"):
        self.idChar = 'D'
        self.jugador = jugador   # Jugador 1 o Jugador 2.
        self.equipo = equipo     # Negras o Blancas.
        self.id = 1              # Dama [1,2? si corona un PEON].
        self.ponerImagen()       # Imagen del Dama.
        self.posiciones = []     # [posXPozo,posYPozo,posPivotXTablero,posPivotYTablero].
        self.posicionarPozoX()   # Campo de inicio de la ficha en X.
        self.posicionarPozoY()   # Campo de inicio de la ficha en Y.
        self.posicionTablero()   # Posiciones en el Tablero de Inicio (se multiplica por la casilla que quiere llegar).
        self.movimientos = []    # Movimientos despues que salen del pozo hasta que los matan.
        self.idCanvas = 0        # Objeto en el Canvas que se va a mover

    ###Ajuste UI###
    def posicionarPozoX(self):   # Se mantiene el eje X para ambos jugadores.
         self.posiciones.append(485.32)

    def posicionarPozoY(self):
        # Jugador 1.
        if(self.jugador == 1):
            self.posiciones.append(140)
        # Jugador 2.
        else:
            self.posiciones.append(425.9)

    def posicionTablero(self):
        self.posiciones.append(50.5)  # Posicion en el eje X.
        self.posiciones.append(126)   # Posicion en el eje Y.
                        
    def ponerImagen(self):
        #Imagenes de las piezas.
        self.width = 26.46      # Ancho de la Dama.
        self.height = 43.08     # Alto de la Dama.
        if(self.equipo == "Negras"):
            self.imagen = "ND.gif"
        else:
            self.imagen = "BD.gif"
        
            
class Alfil():
    """Crea la clase Alfil para poder modificar los atributos
    """
    ###Constructor de la clase###
    def __init__(self,identificador,jugador=1,equipo="Negras"):
        self.idChar = 'A'
        self.jugador = jugador   # Jugador 1 or Jugador 2.
        self.equipo = equipo     # Negras or Blancas.
        self.id = identificador  # Alfil [1,2].
        self.ponerImagen()       # Imagen del Alfil.
        self.posiciones = []     # [posXPozo,posYPozo,posPivotXTablero,posPivotYTablero].
        self.posicionarPozoX()   # Campo de inicio de la ficha en X.
        self.posicionarPozoY()   # Campo de inicio de la ficha en Y.
        self.posicionTablero()   # Posiciones en el Tablero de Inicio (se multiplica por la casilla que quiere llegar).
        self.movimientos = []    # Movimientos despues que salen del pozo hasta que los matan.
        self.idCanvas = 0        # Objeto en el Canvas que se va a mover

    ###Ajuste UI###
    def posicionarPozoX(self):       # Se mantiene el eje X para ambos jugadores.
        if(self.id == 1):
            self.posiciones.append(473.32) # Alfil 1.

        else:
            self.posiciones.append(496.32) # Alfil 2.
            
    def posicionarPozoY(self):
        # Jugador 1.
        if(self.jugador == 1):
            self.posiciones.append(181) 
        # Jugador 2.
        else:
            self.posiciones.append(464.9)

    def posicionTablero(self):
        self.posiciones.append(50.3) # Posicion en el eje X.
        self.posiciones.append(126)  # Posicion en el eje Y.
            
    def ponerImagen(self):
        #Imagenes de las piezas.
        self.width =  23.61     # Ancho del Alfil.
        self.height = 48.40    # Alto del Alfil.
        if(self.equipo == "Negras"):
            self.imagen = "NA.gif"
        else:
            self.imagen = "BA.gif"

# Aquí inicia el programa.
Inicio()


##master = Tk()
##
##w = Canvas(master, width=300, height=200)
##w.pack()
##
##w.create_rectangle(0, 0,64.0025 , 64.0025, fill="blue")
##w.create_rectangle(64.0025, 0,128.005 ,64.0025 , fill="red")
##w.create_rectangle(64.0025, 0,128.005 ,64.0025 , fill="red")
##imagen = PhotoImage(file="NA.gif") # Crea la imagen de fondo de la ventana inicio.
##q = w.create_image(32, 32, image=imagen)
##i = w.create_image(32, 32, image=imagen)
##fila = 1
##columna = 2
##posInicial = 32
##w.coords(i,posInicial + (columna-1) * 64,32 + (fila-1) * 64)
##fila = 2
##w.coords(q,posInicial + (columna-1) * 64,32 + (fila-1) * 64)


