

import tkinter as tk                

from tkinter import messagebox
from tkinter import ttk
from tkinter import font  as tkfont 
from tkinter import filedialog

import webbrowser
import numpy as npy 

from PIL import Image,ImageTk

ima = Image.open("genexRotor_logo.png")
resized = ima.resize((600, 656),Image.ANTIALIAS)


class App_GenxRotor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title_font = tkfont.Font(family='Segoe UI', size=18, weight="bold", slant="italic")
        self.subtitle_font = tkfont.Font(family='Verdana', size=16, slant="italic")
        #self.image=ImageTk.PhotoImage(ima)
        
        
        self.title("gene xRotor [beta v0.8]")
        self.geometry("1000x680")
        self.resizable(False,False)


        # GenxRotor background image and Mau icon load
        self.image=ImageTk.PhotoImage(resized)
        ttk.Label(self, image=self.image).pack(expand='yes',side='bottom')
        self.iconbitmap('icono/GalaxyM101.ico')
        
        menubar = tk.Menu(self)

        # create a pulldown menu, and add it to the menu bar
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Guardar")#, command=menuCall)
        filemenu.add_command(label="Abrir")#, command=hello)

        filemenu.add_separator()
        filemenu.add_command(label="Salir")#, command=lambda: self.close())
        menubar.add_cascade(label="Archivo", menu=filemenu)

        # create more pulldown menus
        calcmenu = tk.Menu(menubar, tearoff=0)
        calcmenu.add_command(label="Coeficiente de Potencia", command=lambda: self.show_frame("CalcPage"))
        calcmenu.add_command(label="Algoritmo Génetico", command=lambda: self.show_frame("GA_Page"))
        calcmenu.add_command(label="----")#, command=hello)
        menubar.add_cascade(label="Cálculos", menu=calcmenu)
		
        menubar.add_command(label="Acerca", command=lambda: self.show_frame("AboutPage"))

        menubar.add_command(label="Salir", command=self.close)

        #LabelTitulo = ttk.Label(self, text="Diseño de un Rotor de Generación Eólica", font=self.title_font)
        #LabelTitulo.grid(row=1, column=0, sticky="e")
        #LabelSubtitulo = ttk.Label(self, text="Optimización con Algoritmos Genéticos", font=self.subtitle_font)
        #LabelSubtitulo.grid(row=2, column=0, sticky="e")
        self.configure(menu = menubar)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.event_generate("<<ShowFrame>>")
        frame.tkraise()

    def close(self):
        if tk.messagebox.askokcancel("Atención","¿Desea cerrar genexRotor?"):
            self.destroy()


class Main_Frame(ttk.Frame):
    def __init__(self,container):
        super().__init__(container)




if __name__ == "__main__":
    app = App_GenxRotor()
    
    Main_Frame(app)
    app.mainloop()
        


