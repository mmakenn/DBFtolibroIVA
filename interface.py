# -*- coding: utf-8 -*-

import os
import sys
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

root = Tk()
root.title("Generador de Archivos - Libro IVA")
PATH = os.path.dirname(sys.argv[0]) # Ruta del Script actual
root.iconbitmap(PATH + '\\icono.ico')
root.geometry('1000x150')


'''.*********************************************************************·'''
'''.Boton para importar solo la base de cuit determinado.'''
selectcuit = Label(root, text='Indicar CUIT Cliente: ')
selectcuit.grid(row=0, column=0)
cuitentry = Entry(root)
cuitentry.grid(row=0, column=3)

'''.*********************************************************************·'''
'''.Botones para obtener las rutas de archivo.'''
purchasesFilename = ''
purchasesFilenameLabel = Label(root, text=purchasesFilename)
purchasesFilenameLabel.grid(row=1, column=4)

salesFilename = ''
salesFilenamelabel = Label(root, text=salesFilename)
salesFilenamelabel.grid(row=2, column=4)

def openPFile():
    global purchasesFilename
    purchasesFilename = filedialog.askopenfilename(title='Buscar...')
    purchasesFilenameLabel.config(text=purchasesFilename)

def openSFile():
    global salesFilename    
    salesFilename = filedialog.askopenfilename(title='Buscar...')
    salesFilenamelabel.config(text=salesFilename)
 
def deletePFile():
    global purchasesFilename
    purchasesFilename = ''
    purchasesFilenameLabel.config(text=purchasesFilename)

def deleteSFile():
    global salesFilename    
    salesFilename = ''
    salesFilenamelabel.config(text=salesFilename)
    
selectpurchases = Label(root, text='Archivo COMPRAS: ')
selectpurchases.grid(row=1, column=0) 
purchasesButton = Button(root, text="Buscar", command=openPFile)
purchasesButton.grid(row=1, column=1)

purchasesDeleteButton = Button(root, text="Borrar", command=deletePFile)
purchasesDeleteButton.grid(row=1, column=3)         

selectsales = Label(root, text='Archivo VENTAS: ')
selectsales.grid(row=2, column=0) 
salesButton = Button(root, text="Buscar", command=openSFile)
salesButton.grid(row=2, column=1)   

purchasesDeleteButton = Button(root, text="Borrar", command=deleteSFile)
purchasesDeleteButton.grid(row=2, column=3)

'''.*********************************************************************·'''
'''. Solicito informacion sobre el periodo a importar .'''
periodlabel = Label(root, text='Periodo (Formato AAAAMM): ')
periodlabel.grid(row=3, column=0)
periodentry = Entry(root)
periodentry.grid(row=3, column=1)

'''.*********************************************************************·'''
'''.Boton para comenzar la ejecucion.'''
import main
def start():
    status = ''
    cuit = cuitentry.get().replace('-', '')
    if purchasesFilename != '' and purchasesFilename[-3:].lower() != 'dbf':
        messagebox.showerror('Error en Base de Datos', 'El archivo es inválido. La extensión del archivo debe ser .DBF')
    elif salesFilename != '' and salesFilename[-3:].lower() != 'dbf':
        messagebox.showerror('Error en Base de Datos', 'El archivo es inválido. La extensión del archivo debe ser .DBF')
    elif cuit == '' or (cuit != '' and len(cuit) != 11):
        messagebox.showerror('Error en CUIT', 'El largo debe ser 11 caracteres')
    else:
        status = main.start(periodentry.get(), purchasesFilename, salesFilename, cuit)
        
    if status == 'OK':
        messagebox.showinfo('Finalizado', 'El proceso finalizó correctamente. Puede cerrar el programa.')
    elif status == 'FAILED':
        messagebox.showerror('Finalizado', 'Hubo un error al procesar la Base de Datos.')
        
        
startbutton = Button(root, text='Comenzar', command=start)
startbutton.grid(row=4, column=4)
'''.*********************************************************************·'''

root.mainloop()