import re
import tkinter.messagebox

#Función que valida el campo de datos de la variable Título contra un patrón establecido.

def validar(cadena): 
    patron = "^[A-Za-z]+(?:[ _-][A-Za-z]+)*$"
    if(re.match(patron,cadena)):
        tkinter.messagebox.showinfo("Cadena válida", "Campo Título validado")
        return True
    else:
        tkinter.messagebox.showerror("Cadena no válida", "Campo Título no validado")
        return False


        

