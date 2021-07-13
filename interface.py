# -*- coding: utf-8 -*-

import os
import sys
from tkinter import *
from tkinter import filedialog

root = Tk()
root.title("Generador de Archivos - Libro IVA")
PATH = os.path.dirname(sys.argv[0]) # Ruta del Script actual
root.iconbitmap(PATH + '\\icono.ico')
root.geometry('1000x400')

'''.Boton para dar opcion a importar solo la base de cuit determinado.'''
def activeentry():
    if cuitoption.get() == 1:
        cuitentry.grid(row=0, column=3)
    else:
        cuitentry.delete(0, END)
        cuitentry.grid_remove()

selectcuit = Label(root, text='Indicar CUIT Cliente: ')
selectcuit.grid(row=0, column=0)
cuitentry = Entry(root, )
cuitoption = IntVar() 
radioButtonno = Radiobutton(root, text='No, generar todos', variable=cuitoption, value=0, command=activeentry)
radioButtonyes = Radiobutton(root, text='Si', variable=cuitoption, value=1, command=activeentry)
radioButtonno.grid(row=0, column=1)
radioButtonyes.grid(row=0, column=2)
'''.*********************************************************************·'''

'''. Menu desplegable para seleccionar basetype .'''
basetypelabel = Label(root, text='Seleccione las bases a utilizar')
basetypelabel.grid(row=1, column=0)
BASE_OPTIONS = ['COMPRAS', 'VENTAS', 'COMPRAS Y VENTAS']
basetype = StringVar()
basetype.set(BASE_OPTIONS[0])
basetypemenu = OptionMenu(root, basetype, *BASE_OPTIONS)
basetypemenu.grid(row=1, column=1)

base1filenamelabel = Label(root, text='')
base2filenamelabel = Label(root, text='')
base1filenamelabel.grid(row=2, column=3)
base2filenamelabel.grid(row=3, column=3)

filename1 = ''
filename2 = ''

def openfile(n):
    global filename1
    global filename2
    if n == 1:
        filename1 = filedialog.askopenfilename(title='Buscar...')
        base1filenamelabel = Label(root, text=filename1)
        base1filenamelabel.grid(row=2, column=3)
    else:
        filename2 = filedialog.askopenfilename(title='Buscar...')
        base2filenamelabel = Label(root, text=filename2)
        base2filenamelabel.grid(row=3, column=3)

def showopenfilesboxes():
    widgetstoclean = root.grid_slaves(row=2) + root.grid_slaves(row=3)
    for widget in widgetstoclean:
        widget.grid_remove()
    if basetype.get() == 'COMPRAS Y VENTAS':
        basecompraslabel = Label(root, text='Seleccione archivo de COMPRAS')
        basecompraslabel.grid(row=2, column=0)
        basecomprasbutton = Button(root, text='Buscar', command=lambda : openfile(1))
        basecomprasbutton.grid(row=2, column=1)
        
        baseventaslabel = Label(root, text='Seleccione archivo de VENTAS')
        baseventaslabel.grid(row=3, column=0)
        baseventasbutton = Button(root, text='Buscar', command=lambda : openfile(2))
        baseventasbutton.grid(row=3, column=1)
    else:
        baselabel = Label(root, text='Seleccione archivo de '+basetype.get())
        baselabel.grid(row=2, column=0)
        basebutton = Button(root, text='Buscar', command=lambda : openfile(1))
        basebutton.grid(row=2, column=1)
    
basetypebutton = Button(root, text='Cambiar tipo de base', command=showopenfilesboxes)
basetypebutton.grid(row=1, column=2)
'''.*********************************************************************·'''

'''. Solicito informacion sobre el periodo a importar .'''
periodlabel = Label(root, text='Periodo (Formato MM/AAAA): ')
periodlabel.grid(row=4, column=0)
periodentry = Entry(root)
periodentry.grid(row=4, column=1)
'''.*********************************************************************·'''

'''.Boton para comenzar la ejecucion.'''
import main
def start():
    if filename1[-3:].lower() != 'dbf':
        messagebox.showerror('Error en Base de Datos', 'El archivo es inválido. La extensión del archivo debe ser .DBF')
    elif filename2 != '' and filename2[-3:].lower() != 'dbf':
        messagebox.showerror('Error en Base de Datos', 'El archivo es inválido. La extensión del archivo debe ser .DBF')
    else:
        purchasesfile = ''
        salesfile = ''
        if basetype.get() == BASE_OPTIONS[0]:
            purchasesfile = filename1
        elif basetype.get() == BASE_OPTIONS[1]:
            salesfile = filename1 
        else:
            purchasesfile = filename1
            salesfile = filename2 
        
        if cuitoption.get() == 0:
            status = main.start(periodentry.get(), purchasesfile, salesfile)
        else:
            cuit = cuitentry.get().replace('-', '')
            if len(cuit) != 11:
                messagebox.showerror('Error CUIT', 'El nro de CUIT ingresado es inválido')
            else:
                status = main.start(periodentry.get(), purchasesfile, salesfile, cuit)
                
    if status == 'OK':
        messagebox.showinfo('Finalizado', 'El proceso finalizó correctamente. Puede cerrar el programa.')
    else:
        messagebox.showerror('Finalizado', 'Hubo un error al procesar la Base de Datos.')
        
        
startbutton = Button(root, text='Comenzar', command=start)
startbutton.grid(row=5, column=3)
'''.*********************************************************************·'''

root.mainloop()