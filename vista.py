# En este modulo se configura la interfaz de la app.
import tkinter
import modelo
from tkinter import ttk, messagebox, Frame, LabelFrame, Button, BOTH, NO, CENTER, W
import re
# Defino una clase para la interfaz de la aplicacion


class VistaApp():
    """
    Clase destinada a la creacion de la interfaz grafica de la aplicacion. Posee multiples atributos destinados
    a la construccion de la interfaz, y varios metodos que permiten llevar adelante las operaciones ABMC. 
    Se comunica con el modulo "modelo" para realizar querys a la base de datos.
    """
    # Defino el constructor, tiene un atributo que será la ventana donde se ejecute.

    def __init__(self, ventana):
        self.root = ventana
        self.root.geometry("600x400")
        self.root.title("CRUD")
        # Agrego un notebook para separar cada funcion del CRUD
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack()
        # -----------------LISTAR--------------
        # Agrego un frame para el index del notebook
        frame_listar = Frame(self.notebook, width=50, height=50)
        frame_listar.pack()
        self.notebook.add(frame_listar, text="Listar clientes")
        # Agrego frame de listar
        frame1 = tkinter.LabelFrame(frame_listar, text="Listar clientes")
        frame1.grid(columnspan=1, padx=10, pady=6)
        # Agrego un treeview para mostrar los clientes dentro del frame_listar.
        self.tree = ttk.Treeview(frame1)
        self.tree["columns"] = ("Id", "Nombre", "Apellido")
        # Doy formato a las columnas
        self.tree.column("#0", stretch=NO, width=0)
        self.tree.column("Id", anchor=CENTER, width=80)
        self.tree.column("Nombre", anchor=W, width=120)
        self.tree.column("Apellido", anchor=W, width=120)
        # Agrego los headings
        self.tree.heading("#0")
        self.tree.heading("Id", text="Id", anchor=CENTER)
        self.tree.heading("Nombre", text="Nombre", anchor=W)
        self.tree.heading("Apellido", text="Apellido", anchor=W)
        self.tree.grid(rowspan=3, columnspan=2)
        Button(frame1, text="Listar/actualizar clientes", command=lambda: self.para_listar()
               ).grid(row=3, column=0)

        #  ----------AGREGAR---------
        # Agrego un frame para el index del notebook.
        frame_agregar = Frame(self.notebook, width=500, height=500)
        frame_agregar.pack(pady=10, padx=20)
        self.notebook.add(frame_agregar, text="Agregar clientes")
        # Agrego frame de añadir
        frame2 = tkinter.LabelFrame(frame_agregar, text="Agregar cliente")
        frame2.grid(columnspan=1, pady=6, padx=10)
        # Entrys
        self.entry_nombre = tkinter.Entry(frame2)
        self.entry_nombre.grid(row=2, column=1)
        self.entry_apellido = tkinter.Entry(frame2)
        self.entry_apellido.grid(row=3, column=1)
        # Labels
        tkinter.Label(frame2, text="Ingresa el nombre:").grid(
            row=2, column=0)
        tkinter.Label(frame2, text="Ingresa el apellido:").grid(
            row=3, column=0)
        # Boton
        boton_agregar = tkinter.Button(
            frame2, text="Agregar cliente", command=lambda: self.para_agregar(self.entry_nombre, self.entry_apellido))
        boton_agregar.grid(row=4, column=3)
        tkinter.Label(
            frame2, text="Para ver los cambios actualiza la lista de clientes.").grid(row=4, column=0)
        ############################
        # ---------ELIMINAR---------
        ############################
        # Agrego un frame para el index del notebook
        frame_eliminar = Frame(self.notebook, width=500, height=500)
        frame_eliminar.pack()
        self.notebook.add(frame_eliminar, text="Eliminar clientes")
        # Agrego frame de eliminar
        frame3 = LabelFrame(frame_eliminar, text="Eliminar un cliente")
        frame3.grid(row=2, column=0, columnspan=1, pady=6, padx=10)
        id = tkinter.StringVar()

        # Entrys
        self.entry_eliminar = tkinter.Entry(frame3, textvariable=id)
        self.entry_eliminar.grid(row=4, column=1)
        # Labels
        tkinter.Label(frame3, text="Ingresa el id del cliente que deseas eliminar:").grid(
            row=4, column=0)
        # Boton
        boton_eliminar = tkinter.Button(
            frame3, text="Eliminar cliente", command=lambda: self.para_borrar(self.entry_eliminar))
        boton_eliminar.grid(row=5, column=1)
        boton_eliminar_todos = tkinter.Button(
            frame3, text="Vaciar tabla", command=self.eliminar_todos)
        boton_eliminar_todos.grid(row=6, column=1)
        tkinter.Label(frame3, text="Para ver los cambios actualiza la lista de clientes.").grid(
            row=6, column=0)
        #################################
        # ---------MODIFICAR-------------
        #################################
        # Agrego un frame para el index del notebook
        frame_modificar = Frame(self.notebook, width=500, height=500)
        frame_modificar.pack(fill=BOTH)
        self.notebook.add(frame_modificar, text="Modificar clientes")
        # Agrego frame de modificar
        frame4 = LabelFrame(frame_modificar, text="Modificar cliente")
        frame4.grid(column=5, row=0, columnspan=1)

        id_modificar = tkinter.StringVar()
        nombre_modificar = tkinter.StringVar()
        apellido_modificar = tkinter.StringVar()
        # Entrys

        self.entry_id_modificar = tkinter.Entry(
            frame4, textvariable=id_modificar)
        self.entry_id_modificar.grid(column=1, row=1)
        self.entry_nombre_modificar = tkinter.Entry(
            frame4, textvariable=nombre_modificar)
        self.entry_nombre_modificar.grid(row=2, column=1)
        self.entry_apellido_modificar = tkinter.Entry(
            frame4, textvariable=apellido_modificar)
        self.entry_apellido_modificar.grid(row=3, column=1)
        # Labels
        tkinter.Label(
            frame4, text="Ingresa el id del cliente que queres modificar y rellena los datos.").grid(row=0, column=0)
        tkinter.Label(frame4, text="Id: ",).grid(row=1, column=0)
        tkinter.Label(frame4, text="Nombre:").grid(row=2, column=0)
        tkinter.Label(frame4, text="Apellido: ").grid(row=3, column=0)
        # Boton
        boton_modificar = tkinter.Button(frame4, text="Modificar cliente", command=lambda: self.para_modificar(
            self.entry_id_modificar, self.entry_nombre_modificar, self.entry_apellido_modificar))
        boton_modificar.grid(row=4, column=2)

        tkinter.Label(frame4, text="Para ver los cambios actualiza la lista de clientes.").grid(
            row=4, column=0)
        # Esto es un atributo de la clase VistaApp?
        self.modelo = modelo.Abmc()

    # Creo un metodo de VistaAPP para limpiar los entrys cada vez que se pulsa el boton correspondiente
    def borrar_entry(self, entry):
        """
        Metodo utilizado para borrar lo que escriba el usuario en los entrys al realizar una funcionalidad.
        Recibe el entry del que se toman datos y procede a dejarlo vacio.
        """
        entry.delete(0, "end")
    # Creo un metodo de VistApp para "actualizar" el treeview con los clientes

    def actualizar_tree(self):
        """
        Metodo que borra cualquier registro que se encuentre a la vista en el treeview del objeto.
        Sera utilizado para "limpiar" registros de modo que no se muestren mas de una vez al listar registros.
        """
        for i in self.tree.get_children():
            self.tree.delete(i)
    # Creo un metodo de VistaApp para usar el metodo eliminar_cliente de la clase Crud.
    # Va a tomar el input que ponga el usuario en el entry_eliminar y luego ejecuta la query de eliminar.

    def para_borrar(self, parametro):
        """
        Metodo destinado a borrar registros de la base de datos. Se ejecuta al presionar en el boton que le corresponde.
        Utiliza un objeto de la clase Abmc, el cual toma el parametro necesario (un id) para borrar un registro.
        Finalmente utiliza el metodo borrar_entry para limpiar.
        """
        self.modelo.eliminar_clientes(parametro.get())
        self.borrar_entry(self.entry_eliminar)

    def eliminar_todos(self):
        """
        Metodo utilizado para eliminar todos los registros de la tabla.
        Utiliza objeto de la clase Abmc para llevar adelante la query.
        """
        self.modelo.borrar_todos()
    # Creo un metodo de VistaApp para usar el metodo agregar_clientes de la clase Crud.
    # Va a tomar el nombre y apellido que ingrese el usuario dentro del entry respectivo. Luego borra.

    def para_agregar(self, nombre, apellido):
        """
            Metodo para agregar clientes dentro de la base de datos. Se ejecuta al presionar el boton que le corresponde.
            Recibe dos strs que deben coincidir con el patron de regex definido para luego agregar un registro a la tabla.
            Utiliza un objeto de la clase Abmc, el cual toma los parametros necesarios (nombre y apellido) para agregar un registro. 
        """
        if nombre.get() != "" and apellido.get() != "":
            self.modelo.agregar_clientes(nombre.get(), apellido.get())
            self.borrar_entry(self.entry_nombre)
            self.borrar_entry(self.entry_apellido)
        else:
            messagebox.showerror(
                title="Erorr", message="Por favor introduci un formato correcto.")
            self.borrar_entry(self.entry_nombre)
            self.borrar_entry(self.entry_apellido)
    # Creo un metodo de VistaApp para usar el metodo modificar_clientes de la clase Crud.
    # Va a tomar el id del cliente que quiera modificar y los nuevos nombres y apellidos que ingrese.

    def para_modificar(self, id, nombre, apellido):
        """
        Metodo destinado a modificar registros de la base de datos. Se ejecuta al presionar el boton que le corresponde.
        Recibe, a lo sumo, tres parametros. Estos deben coincidir con su respectiva regex. 
        """
        self.modelo.modificar_clientes(id.get(), nombre.get(), apellido.get())
        # Me aseguro que me pase un id y al menos cambie un campo para dar notificacion.
        if id.get() != "" and (nombre.get() != "" or apellido.get() != ""):
            messagebox.showinfo(
                message="Cliente modificado.", title="Aviso")
        # Limpio los entrys.
        self.borrar_entry(self.entry_apellido_modificar)
        self.borrar_entry(self.entry_id_modificar)
        self.borrar_entry(self.entry_nombre_modificar)

    def para_listar(self):
        """
        Metodo destinado a listar registros de la tabla. 
        Usa el metodo actualizar_tree para limpiar los registros del treeview y luego utiliza un objeto de la clase Abmc
        para proceder a listar los registros.
        """
        self.actualizar_tree()
        self.modelo.listar_clientes(self.tree)
