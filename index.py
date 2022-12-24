# crud realizado con tkinter para la interfaz y sqlite3 de base de datos y db browser para interfaz de base de datos

from tkinter import *
from tkinter import ttk

import sqlite3


class Product:

    db_nombre = 'database.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Aplicacion de productos')

        # frame container
        frame = LabelFrame(self.wind, text='Registra un nuevo producto')
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # input Nombre
        Label(frame, text='Nombre: ').grid(row=1, column=0)
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        # Input Precio
        Label(frame, text='Precio: ').grid(row=2, column=0)
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1)

        # boton agregar producto
        ttk.Button(frame, text='Guardar Producto', command=self.add_products).grid(
            row=3, columnspan=2, sticky=W + E)

        # boton eliminar producto
        ttk.Button(text='ELIMINAR', command=self.eliminar_producto).grid(
            row=5, column=0, sticky=W+E)
        # boton actualizar producto
        ttk.Button(text='EDITAR', command=self.actualizar_producto).grid(
            row=5, column=1, sticky=W+E)

        # mensaje de salida
        self.mensaje = Label(text='', fg='red')
        self.mensaje.grid(row=3, columnspan=2, sticky=W+E)
        # tabla
        self.tree = ttk.Treeview(height=10, columns=2, )
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text='Nombre', anchor=CENTER)
        self.tree.heading('#1', text='Precio', anchor=CENTER)

        # llena la tabla
        self.get_products()

    # acceso a la base de datos

    def run_query(self, query, params=()):
        with sqlite3.connect(self.db_nombre) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, params)
            conn.commit()
            return result

    def get_products(self):
        # limpia tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        # consulto datos
        query = 'SELECT * FROM producto ORDER BY nombre DESC'
        db_rows = self.run_query(query)
        # relleno datos
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=row[2])

    def validar(self):
        return len(self.nombre.get()) != 0 and len(self.precio.get()) != 0

    def add_products(self):
        if self.validar():
            query = 'INSERT INTO producto VALUES(NULL, ?, ?)'
            parametros = (self.nombre.get(), self.precio.get())
            self.run_query(query, parametros)
            self.mensaje['text'] = 'Producto: {} ha sido agregado satisfactoriamente'.format(
                self.nombre.get())
            self.nombre.delete(0, END)
            self.precio.delete(0, END)
        else:
            self.mensaje['text'] = 'el precio y el nombre son requeridos'
        self.get_products()

    def eliminar_producto(self):
        self.mensaje['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError:
            self.mensaje['text'] = 'Por favor selecciona un producto'
            return
        self.mensaje['text'] = ''
        query = 'DELETE FROM producto WHERE nombre = ?'
        name = self.tree.item(self.tree.selection())['text']
        self.run_query(query, (name, ))
        self.mensaje['text'] = '{} ha sido eliminado correctamente'.format(
            name)
        self.get_products()

    def actualizar_producto(self):
        self.mensaje['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError:
            self.mensaje['text'] = 'Por favor selecciona un producto'
            return
        self.mensaje['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar Producto'

        # viejo nombre
        Label(self.edit_wind, text='Nombre Viejo: ').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind,
              value=name), state='readonly').grid(row=0, column=2)

        # nuevo nombre
        Label(self.edit_wind, text='Nuevo nombre: ').grid(row=1, column=1)
        nuevo_nombre = Entry(self.edit_wind)
        nuevo_nombre.grid(row=1, column=2)

        # viejo precio
        Label(self.edit_wind, text='Precio Viejo: ').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind,
              value=old_price), state='readonly').grid(row=2, column=2)

        # nuevo precio
        Label(self.edit_wind, text='Nuevo Precio: ').grid(row=3, column=1)
        nuevo_precio = Entry(self.edit_wind)
        nuevo_precio.grid(row=3, column=2)

        # BOTON actualizar
        Button(self.edit_wind, text='Actualizar',
               command=lambda: self.editar_productos(nuevo_nombre.get(), name, nuevo_precio.get(), old_price)).grid(row=4, column=2, sticky=W)

    def editar_productos(self, nuevo_nombre, viejo_nombre, nuevo_precio, viejo_precio):
        query = 'UPDATE producto SET nombre = ?, precio = ? WHERE nombre = ? AND precio = ?'
        parametros = (nuevo_nombre, nuevo_precio, viejo_nombre, viejo_precio)
        self.run_query(query, parametros)
        self.edit_wind.destroy()
        self.mensaje['text'] = 'El producto: {} ahora es: {}'.format(
            viejo_nombre, nuevo_nombre)
        self.get_products()


if __name__ == '__main__':
    window = Tk()
    aplicacion = Product(window)
    window.mainloop()
