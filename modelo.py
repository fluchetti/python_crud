# En este modulo se ejecutan las funciones de la app.
from os import curdir
from typing import Text
from peewee import with_metaclass
from regex import match
import sqlite3
from tkinter import messagebox

# Creo una clase Abmc


class Abmc:
    """
    Clase destinada a ejecutar funcionalidades relacionadas con la base de datos.
    """
    # Defino el constructor de la clase, este tiene como fin inicializar los objetos de la clase

    def __init__(self):
        """
        Constructor de la clase, define dos atributos que seran utilizados para validar los inputs.
        """
        self.patron_nombre = "^[A-ZÑ][a-záéíóúñ]+( [A-ZÑ][a-záéíóúñ]+)*$"
        self.patron_numero = "^[0-9]+$"

    # En todos los metodos que siguen el parametro self hace referencia al objeto de la clase Abmc que lo utiliza.

    # Defino el metodo para conectarme a la base (si no existe, la crea). Retorna la conexion a dicha base.
    def conexion_db(self):
        """
        Metodo utilizado para conectarse a la base de datos, en caso de que esta no exista, se crea.
        Este metodo sera utilizado por otros para acceder a la base y realizar distintas querys.
        Retorna la conexion a la base.
        """
        conexion = sqlite3.connect("clientes.db")
        return conexion

    # Defino el metodo para crear una tabla dentro de la base a la que me conecto.
    def crear_tabla(self):
        """
        Metodo utilizado para crear una tabla dentro de la base de datos.
        Crea 3 columnas, nombre y apellido son de tipo CHAR y deben completarse a la hora de agregar un registro.
        id es de tipo INTEGER, es PRIMARY KEY (por lo cual no puede ser NULL) y AUTOINCREMENTAL
        (no es necesario especificar su valor a la hora de cargar registros)
        """
        conexion = self.conexion_db()
        cursor = conexion.cursor()
        try:
            sql = """CREATE TABLE  IF NOT EXISTS clientes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre CHAR(20) NOT NULL,
                apellido CHAR(20) NOT NULL
            )"""
            cursor.execute(sql)
            conexion.commit()
            conexion.close()
        except Exception as e:
            print("Ocurrio un error: {e}")
    # Defino el metodo para listar clientes dentro de la base a la que me conecto.

    def listar_clientes(self, tree):
        """
        Metodo utilizado para listar los registros que contiene la base de datos.
        Toma un parametro "tree", el cual hace referencia al treeview de la interfaz grafica, donde se mostraran los posibles registros.
        """
        conexion = self.conexion_db()
        cursor = conexion.cursor()
        try:
            sql = "SELECT * FROM clientes"
            cursor.execute(sql)
            clientes = cursor.fetchall()
            if len(clientes) != 0:
                for i in clientes:
                    tree.insert(parent="", index=i[0], values=(
                        i[0], i[1], i[2]))
        # Si la lista esta vacia mando una notificacion.
            else:
                messagebox.showinfo(
                    message="No hay clientes en la lista.", title="Aviso")

            conexion.close()
        except Exception as e:
            print(f"Ocurrio un error: {e}")

    # Defino el metodo para agregar clientes dentro de la base a la que me conecto.

    def agregar_clientes(self, nombre, apellido):
        """
        Metodo utilizado para agregar registros dentro de la tabla "clientes".
        Toma dos parametros, nombre y apellido los cuales seran obtenidos de la interfaz grafica.
        Se valida mediante regex que el usuario ingrese un formato correcto ( Nombre Apellido ) dentro de los entrys.
        Dependiendo el caso, lanzara una notificacion acorde al insertarse registros.
        """
        datos = (nombre, apellido)
        if match(self.patron_nombre, datos[0]) and match(self.patron_nombre, datos[1]):
            conexion = self.conexion_db()
            cursor = conexion.cursor()
            try:
                sql = "SELECT * FROM clientes WHERE Nombre = ? AND Apellido = ?"
                cursor.execute(sql, (datos[0], datos[1]))
                lista_clientes = cursor.fetchall()
                # Me aseguro que llene los campos.
                if datos[0] != "" and datos[1] != "":
                    # Me aseguro que el cliente no este en la lista
                    if len(lista_clientes) != 0:
                        messagebox.showerror(
                            "Aviso", "Ya esta registrado el cliente.")
                    else:
                        cursor.execute(
                            "INSERT INTO clientes (Nombre,Apellido) VALUES (?,?)", (datos[0], datos[1]))
                        messagebox.showinfo("Aviso", "Cliente añadido")
                else:

                    messagebox.showerror(
                        message="Completa los campos.", title="Error")
                conexion.commit()
                conexion.close()
            except Exception as e:
                print(f"Ocurrio un error: {e}")
        else:
            messagebox.showerror("Error", "Formato erroneo.")
    # Defino el metodo para eliminar clientes dentro de la base a la que me conecto.

    def borrar_todos(self):
        """
        Metodo utilizado para eliminar todos los registros de la tabla.
        """
        conexion = self.conexion_db()
        cursor = conexion.cursor()
        confirmar = messagebox.askyesno("Aviso", "Borrar todos los clientes?")
        if confirmar == True:
            cursor.execute("DELETE FROM clientes")
            conexion.commit()
            conexion.close()
        else:
            pass

    def eliminar_clientes(self, id):
        """
        Metodo utilizado para eliminar registros de la tabla de forma individual.
        Toma un parametro id, el cual debe ser un numero y sera utilizado como referencia para eliminar un registro.
        """
        if match(self.patron_numero, id):
            conexion = self.conexion_db()
            cursor = conexion.cursor()
            try:
                datos = (id,)
                sql = "SELECT * FROM clientes WHERE id = ?"
                cursor.execute(sql, datos)
                resultado = cursor.fetchall()
                if len(resultado) != 0:
                    confirmar = messagebox.askyesno(
                        title="Aviso", message="Eliminar cliente?")
                    if confirmar == True:
                        sql = "DELETE FROM clientes WHERE id = ?"
                        cursor.execute(sql, (datos))
                    else:
                        pass
                    conexion.commit()
                    conexion.close()
                else:
                    messagebox.showwarning(
                        "Atencion", f"No existe cliente con id {id}.")
            except Exception as e:
                print(f"Ocurrio un error: {e}")
        else:
            messagebox.showerror("Error", "Erro de formato.")
    # Defino el metodo para modificar clientes dentro de la base a la que me conecto.

    def modificar_clientes(self, id, nombre, apellido):
        """
        Metodo utilizado para modificar registros de la tabla. 
        Toma, a lo sumo, tres parametros. Se requiere de un id y un nombre/apellido para ejecutar una acutalizacion de registro.
        Se verifica que cada parametro concuerde con lo esperado utilizando regex.
        """
        if match(self.patron_numero, id):
            conexion = self.conexion_db()
            cursor = conexion.cursor()
            datos_nombre = (nombre, id)
            datos_apellido = (apellido, id)
            try:
                # Si deja un campo vacio no lo modifico.
                if nombre != "" and match(self.patron_nombre, nombre):
                    sql = "UPDATE clientes SET nombre = ? WHERE id = ?"
                    cursor.execute(sql, (datos_nombre))
                if apellido != "" and match(self.patron_nombre, apellido):
                    sql = "UPDATE clientes SET apellido = ? WHERE id = ?"
                    cursor.execute(sql, (datos_apellido))
                conexion.commit()
                # Si no modificó al menos uno de los dos campos notifico el error.
                if nombre != "" or apellido != "":
                    pass
                else:
                    messagebox.showerror(title="Error",
                                         message="Completa al menos un campo para modificar.")
                conexion.close()
            except Exception as e:
                print("Ocurrio un error: {e}")
        else:
            messagebox.showerror(
                "Error", "Error de formato al ingresar datos.")

    def agregar_ejemplos(self, nombre, apellido):
        """
        Metodo para agregar ejemplos rapido y asi facilitar la interaccion con las diversas funciones. No verifica existencia previa.
        """
        conexion = self.conexion_db()
        cursor = conexion.cursor()
        sql = "INSERT INTO clientes (Nombre,Apellido) VALUES (?,?)"
        datos = (nombre, apellido)
        cursor.execute(sql, datos)
        conexion.commit()
        conexion.close()
