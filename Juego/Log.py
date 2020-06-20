import datetime

from Juego.LogMov import LogMov
from Juego.Tipos import TipoDeJuego
from Juego.Tipos import Turno
from Juego.Tipos import Pieza
from Juego.Tipos import EstadosLog

class Log:

    def __init__(self,tablero,piezas_iniciales,tipo_de_juego,J1,J2,turno_inicial):

        ##Configuracion de archivo
        self.path = "./Logs/"
        self.ext = ".log"
        ##Configuracion del log
        self.tablero = tablero
        self.generar_nombre_log()
        self.piezas_iniciales = piezas_iniciales
        self.tipo_de_juego = tipo_de_juego
        self.J1 = J1
        self.J2 = J2
        self.turno_inicial = turno_inicial

        ##Historial
        self.historial_de_movimientos = []

        ##Resultados
        self.juego_finalizado = False
        self.resultado = ""       
        self.time_stamp = ""

    def set_estado_a_log(self,estado):
        if estado != None:
            tmp_log = self.historial_de_movimientos.pop()
            tmp_log.escribir_estado(estado)
            self.historial_de_movimientos.append(tmp_log)

    def finalizar_juego(self):
        self.juego_finalizado = True

    def generar_nombre_log(self):
        date = datetime.datetime.now().isoformat()
        date = date.replace(".","%")
        date = date.replace(":","%")
        print(date)
        self.file_name = self.path+date+self.ext
    

    def agregar_log(self,tablero,movimiento):
        new_log_mov = LogMov(movimiento)
        new_log_mov.escribir_movimiento(tablero)
        self.historial_de_movimientos.append(new_log_mov)

    ##Ejemplo de log
    ##timestamp: datetime.datetime().isoformat()
    ##tipo de juego: self.tipo de juego
    ##J1 v J2: Blancas v Negras
    ##mueven: Blancas
    ##resultado: Ganan Blancas/Ganan Negras/Tablas
    ##tablero inicial: NDd8,NRe8,NTh8,NPd7,NPe7,NPf7,NPg7,BAc6,NAb5,BPh5,NPa4,BPe4,NCh3,BPa2,BPb2,BPd2,BPf2,BPg2,BCb1,BRe1,BAf1,BCg1
    ##historial de movimientos:
    ##1. mov
    ##2. mov
    ##...
    ##n. mov
   
    def registrar_log(self):
        endline = "\n"
        tipo_de_juego = self.tipo_de_juego_toString()
        blancas = self.jugador_blancas_toString()
        negras = self.jugador_negras_toString()
        mueven = self.turno_inicial_toString()
        resultado = self.resultado_toString()
        piezas_iniciales = self.piezas_iniciales_toString()
        contador_de_movimientos = 1
        print(self.file_name)
        file = open(self.file_name,"w+")
        file.write("timestamp: " + datetime.datetime.now().isoformat() + endline)
        file.write("tipo de juego: " + tipo_de_juego + endline)
        file.write("blancas: " + blancas + endline)
        file.write("negras: " + negras + endline)
        file.write("mueven: " + mueven + endline)
        file.write("resultado: " + resultado + endline)
        file.write("tablero inicial: " + piezas_iniciales + endline)
        file.write("historial de movimientos: " + endline)

        for log_mov in self.historial_de_movimientos:
            file.write(str(contador_de_movimientos) + ". " + log_mov.log_movimiento + endline)
            contador_de_movimientos += 1                 
        
        file.close()
        return 
 
    def tipo_de_juego_toString(self):
        if self.tipo_de_juego == 1:
            return "Jugador vs Jugador"
        elif self.tipo_de_juego == 2:
            return "Jugador vs PC"
        elif self.tipo_de_juego == 3:
            return "PC vs PC"
    
    def jugador_blancas_toString(self):
        if self.J1 == "B":
            if self.tipo_de_juego == 1:
                return "Jugador1"
            elif self.tipo_de_juego == 2:
                return "Jugador"
            elif self.tipo_de_juego == 3:
                return "PC1"
        else:
            if self.tipo_de_juego == 1:
                return "Jugador2"
            elif self.tipo_de_juego == 2:
                return "PC"
            elif self.tipo_de_juego == 3:
                return "PC2"
            
    def jugador_negras_toString(self):
        if self.J1 == "N":
            if self.tipo_de_juego == 1:
                return "Jugador1"
            elif self.tipo_de_juego == 2:
                return "Jugador"
            elif self.tipo_de_juego == 3:
                return "PC1"
        else:
            if self.tipo_de_juego == 1:
                return "Jugador2"
            elif self.tipo_de_juego == 2:
                return "PC"
            elif self.tipo_de_juego == 3:
                return "PC2"

    def turno_inicial_toString(self):
        if self.turno_inicial == "B":
            return "Blancas"
        else:
            return "Negras"

    def resultado_toString(self):
        resultado_str = ""
        if self.juego_finalizado:
            if self.resultado == None:
                resultado_str = "Tablas"
                return resultado_str 
            elif self.resultado == Turno.BLANCAS:
                resultado_str = "Ganan las Blancas"
                return resultado_str
            elif self.resultado == Turno.NEGRAS:
                resultado_str = "Ganan las Negras"
                return resultado_str
        else:
            resultado_str = "Juego Incompleto"
            return resultado_str

    def piezas_iniciales_toString(self):
        ## Ejm. ['B','D','a',5]
        piezas_iniciales_str = ""
        for tmp_pieza in self.piezas_iniciales:
            for index in range(0,len(tmp_pieza)):
                piezas_iniciales_str = piezas_iniciales_str + tmp_pieza[index]
            piezas_iniciales_str = piezas_iniciales_str + " "
        return piezas_iniciales_str

