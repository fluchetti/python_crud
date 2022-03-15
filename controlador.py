# En este modulo se ejecuta la app.
import tkinter
import modelo
import vista
from tkinter import Tk

# Creo db y tabla con un objeto de la clase Abmc. Agrego ejemplos sencillos.
modelo = modelo.Abmc()
modelo.conexion_db()
modelo.crear_tabla()
modelo.agregar_ejemplos("Juan", "Gomez")
modelo.agregar_ejemplos("Faustino", "Luchetti")
modelo.agregar_ejemplos("Ariel", "Rodriguez")
modelo.agregar_ejemplos("Joaquin", "Arregui")
modelo.agregar_ejemplos("Lionel", "Fernandez")

# Defino una clase desde donde se lanza la aplicacion, tiene como atributo una ventana (tkinter.Tk())


class MiAplicacion:
    """
    Clase destinada a ejecutar la interfaz grafica de la aplicacion. 
    Su metodo constructor tiene un atributo, el cual es una ventana de la libreria tkinter.
    """

    def __init__(self, ventana):
        self.root = ventana
        vista.VistaApp(self.root)


# Lanzo la aplicacion
if __name__ == "__main__":
    ventana = tkinter.Tk()
    app = vista.VistaApp(ventana)
    ventana.mainloop()
