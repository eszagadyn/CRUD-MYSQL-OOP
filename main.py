#Curso: Python 3 - Nivel Intermedio
#Alumno: Eduardo Luis Szagadyn
#Ejercicio de la unidad 3

import tkinter
import tkinter.messagebox
import tkinter.ttk
import mysql.connector
import modulovalidacion

class Producto:

    def __init__(self, window):
        
        self.master = window
        self.master.title("Tarea POO")
        self.master.geometry("515x300")
        self.master.resizable(True, True)

        Etiqueta1 = tkinter.Label(self.master, text= "Ingrese sus datos", bg = "purple", fg = "white", width=70, justify=tkinter.LEFT)
        Etiqueta1.grid(row=0, column=0, columnspan=3, sticky=tkinter.EW)
        Etiqueta1bis = tkinter.Label(self.master, text= "", bg = "purple", fg = "white", width=1, justify=tkinter.LEFT)
        Etiqueta1bis.grid(row=0, column=4, sticky=tkinter.EW) #Rellena interfaz

        self.Etiqueta_Titulo = tkinter.Label(self.master, text="Título")
        self.Etiqueta_Titulo.grid(row=1, column=0, sticky=tkinter.W)

        Etiqueta_Descripcion = tkinter.Label(self.master,text="Descripción")
        Etiqueta_Descripcion.grid(row=2, column=0, sticky=tkinter.W)

        self.val_titulo = tkinter.StringVar()
        self.entrada_titulo = tkinter.Entry(self.master, textvariable=self.val_titulo, width=40)
        self.entrada_titulo.grid(row=1, column=1, sticky=tkinter.EW, padx=10)

        self.val_descripcion = tkinter.StringVar()
        self.entrada_descripcion = tkinter.Entry(self.master, textvariable=self.val_descripcion, width=40)
        self.entrada_descripcion.grid(row=2, column=1, sticky=tkinter.EW, padx=10)

        Etiqueta2 = tkinter.Label(self.master, text= "Mostrar registros existentes", bg = "light grey", fg = "black", width=70, justify=tkinter.LEFT)
        Etiqueta2.grid(row=3, column=0, columnspan=3, sticky=tkinter.EW)
        Etiqueta2bis = tkinter.Label(self.master, text= "", bg = "light grey", fg = "black", width=1, justify=tkinter.LEFT)
        Etiqueta2bis.grid(row=3, column=4, sticky=tkinter.EW) #Rellena interfaz

        self.vista_arbol = tkinter.ttk.Treeview(self.master, columns=(1,2,3), show="headings", height="5", selectmode ="browse")
        self.vista_arbol.heading(1, text="ID")
        self.vista_arbol.heading(2, text="Título")
        self.vista_arbol.heading(3, text="Descripción")
        self.vista_arbol.column(1, width=150, minwidth=150, stretch=tkinter.YES)
        self.vista_arbol.column(2, width=150, minwidth=150, stretch=tkinter.YES)
        self.vista_arbol.column(3, width=150, minwidth=150, stretch=tkinter.YES)
        self.scroll_arbol = tkinter.ttk.Scrollbar(self.master, orient ="vertical", command = self.vista_arbol.yview)
        self.vista_arbol.configure(yscrollcommand = self.scroll_arbol.set)
        self.vista_arbol.grid(row=5, column=0, columnspan=3, rowspan=5, sticky=tkinter.NSEW)
        self.scroll_arbol.grid(row=5, column=4, rowspan=5, sticky=tkinter.NSEW)
        self.master.grid_rowconfigure(5, weight=1)    

        self.alta = tkinter.Button(self.master, text="Alta", command=self.accion_alta)
        self.alta.grid(row=10, column=0)

        self.baja = tkinter.Button(self.master, text="Baja", command=self.accion_baja)
        self.baja.grid(row=10, column=1)

        self.modificacion = tkinter.Button(self.master, text="Modificación", command=self.accion_modificacion)
        self.modificacion.grid(row=10, column=2)

        self.entrada_titulo.bind("<FocusIn>", self.titulo_on_focus)
        self.entrada_titulo.bind("<FocusOut>", self.titulo_out_focus)

    def titulo_on_focus(self, event):
        self.Etiqueta_Titulo.configure(text="Sólo letras:", fg="purple")

    def titulo_out_focus(self, event):
        self.Etiqueta_Titulo.configure(text="Título", fg="black")

    def recuperar_registros(self):
        try:
            mibase = mysql.connector.connect(host="localhost", user="root", passwd="")
            micursor = mibase.cursor()
            micursor.execute("SELECT * FROM baseprueba3.producto")
            copia_base = micursor.fetchall()
            self.vista_arbol.delete(*self.vista_arbol.get_children())
            for row in copia_base:
                self.vista_arbol.insert("", "end", values=(row[0], row[1], row[2]))
        except:
            return None

    def accion_crearDB(self):
        try:
            mibase = mysql.connector.connect(host="localhost", user="root", passwd="")    
            micursor = mibase.cursor()
        except:
            tkinter.messagebox.showerror("Error", "Conexión a Base de Datos no disponible")
            self.master.focus_force()
            return None
        micursor.execute("CREATE DATABASE IF NOT EXISTS baseprueba3 CHARACTER SET UTF8 COLLATE utf8_spanish2_ci")
        micursor.execute("CREATE TABLE IF NOT EXISTS baseprueba3.producto(id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT, titulo VARCHAR(128) COLLATE utf8_spanish2_ci NOT NULL, descripcion text COLLATE utf8_spanish2_ci NOT NULL )")
        micursor.close()

    def accion_alta(self):
        try:
            mibase = mysql.connector.connect(host="localhost", user="root", passwd="", database="baseprueba3")
            micursor = mibase.cursor()
        except:
            application.accion_crearDB()
        if not self.val_titulo.get() and not self.val_descripcion.get():
            tkinter.messagebox.showinfo("Advertencia", "Registro en blanco. NO AGREGADO.")
            return None
        cadena = self.val_titulo.get()                             
        if modulovalidacion.validar(cadena) == False:
            self.entrada_titulo.delete(0, "end")          
            return None
        datos_alta = (self.val_titulo.get(), self.val_descripcion.get())
        sql_alta = "INSERT INTO producto (titulo, descripcion) VALUES (%s, %s)"
        try:
            micursor.execute(sql_alta, datos_alta)
            mibase.commit()
            self.entrada_titulo.delete(0, "end")
            self.entrada_descripcion.delete(0, "end")
            self.recuperar_registros()
            if mibase.is_connected() == True:
                micursor.close()
        except:
            tkinter.messagebox.showerror("Error", "Operación de alta no disponible")

    def accion_baja(self):
        try:
            mibase = mysql.connector.connect(host="localhost", user="root", passwd="", database="baseprueba3")
            micursor = mibase.cursor()
            item = self.vista_arbol.item(self.vista_arbol.focus())
            row_value = item.get("values")
            id_treeview = row_value[0]
            id_treeview = str(id_treeview)
            sql_baja= "DELETE FROM producto WHERE id = " + id_treeview
            micursor.execute(sql_baja)
            mibase.commit()
            self.recuperar_registros()
            micursor.close()
        except:
            tkinter.messagebox.showerror("Error", "Ningún registro seleccionado")

    def accion_modificacion(self):
        try:
            mibase = mysql.connector.connect(host="localhost", user="root", passwd="", database="baseprueba3")
            micursor = mibase.cursor()
            if not self.val_titulo.get() and not self.val_descripcion.get():
                tkinter.messagebox.showinfo("Advertencia", "Registro en blanco. NO MODIFICADO.")
                micursor.close()
                return None
            cadena = self.val_titulo.get()                             
            if modulovalidacion.validar(cadena) == False:
                self.entrada_titulo.delete(0, "end")          
                return None
            item = self.vista_arbol.item(self.vista_arbol.focus())
            row_value = item.get("values")
            id_treeview = row_value[0]
            id_treeview = str(id_treeview)
            sql_modificacion= "UPDATE producto SET titulo=%s, descripcion=%s WHERE id = " + id_treeview
            datos_modificacion = (self.val_titulo.get(), self.val_descripcion.get())
            micursor.execute(sql_modificacion, datos_modificacion)
            mibase.commit()
            self.entrada_titulo.delete(0, "end")
            self.entrada_descripcion.delete(0, "end")
            self.recuperar_registros()
            micursor.close()
        except:
            tkinter.messagebox.showerror("Error", "Ningún registro seleccionado")

if __name__ == '__main__':
    window = tkinter.Tk()
    application = Producto(window)
    application.accion_crearDB()
    application.recuperar_registros()
    window.mainloop()