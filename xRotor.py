from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import filedialog
import webbrowser

#Importaciones matematicas
import numpy as npy
from numpy import *

# Para las graficas
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

#Importacion de otros scripts 
#import ClaseCoefPotencia_Old as clase
import Clase_CoefPotencia as clase
import MainCGA as GA

from PIL import Image,ImageTk
ima = Image.open("GenxRotor_logo.png")
imaIco=Image.open("icono\GalaxyM101.ico")

class GenxRotor(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Segoe UI', size=18, weight="bold", slant="italic")
        self.subtitle_font = tkfont.Font(family='Verdana', size=16, slant="italic")
        #self.image=ImageTk.PhotoImage(ima)
        resized = ima.resize((600, 549),Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized)
        self.imageIco=ImageTk.PhotoImage(imaIco)
        
        self.TxtPerfil1 = tk.StringVar()
        self.TxtPerfil2 = tk.StringVar()
        self.TxtPerfil3 = tk.StringVar()
        self.TxtPerfil4 = tk.StringVar()
        self.TxtAlp1 = tk.StringVar()
        self.TxtPos1 = tk.StringVar()
        self.TxtAlp2 = tk.StringVar()
        self.TxtPos2 = tk.StringVar()
        self.TxtAlp3 = tk.StringVar()
        self.TxtPos3 = tk.StringVar()
        self.TxtAlp4 = tk.StringVar()
        self.TxtSec = tk.StringVar()
        self.TxtIter = tk.StringVar()
        self.TxtConv = tk.StringVar()
        self.combo =tk.StringVar()
        self.ngraph = tk.IntVar()
        self.CalcDone = tk.IntVar()
        self.CalcDone.set(0)
        self.GADone =tk.IntVar()
        self.GADone.set(0)
        self.Valores={}
        self.BestChrom={}
        self.paramEjec={}
        self.Perf1 = IntVar()
        self.Perf1.set(1)
        self.ChkVar1= IntVar()
        # self.ChkVar1.set(1)
        self.ChkVar2= IntVar()
        # self.ChkVar2.set(1)
        self.ChkVar3= IntVar()
        self.ComboVar =IntVar()
        self.ComboVar.set(3)
        self.RadioVar=IntVar()
        # self.ChkVar3.set(1)
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames ={}
        for F in (StartPage, CalcPage, GA_Page, AboutPage,GA_Param_Page):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.event_generate("<<ShowFrame>>")
        frame.tkraise()
        
        
        


class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        wid=400
        hei=260
        
         # create a toplevel menu
        menubar = Menu(self)

        # create a pulldown menu, and add it to the menu bar
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Guardar",command=self.saveCase)#, command=menuCall)
        filemenu.add_command(label="Abrir")#, command=hello)
        filemenu.add_command(label="Caso Lupita", command=self.loadLupita)
        filemenu.add_command(label="Caso A", command=self.loadA)
        filemenu.add_command(label="Caso B.1", command=self.loadB1)
        filemenu.add_command(label="Caso B.2", command=self.loadB2)
        filemenu.add_separator()
        filemenu.add_command(label="Salir")#, command=lambda: self.close())
        menubar.add_cascade(label="Archivo", menu=filemenu)

        # create more pulldown menus
        calcmenu = Menu(menubar, tearoff=0)
        calcmenu.add_command(label="Coeficiente de Potencia", command=lambda: controller.show_frame("CalcPage"))
        calcmenu.add_command(label="Algoritmo Génetico", command=lambda: controller.show_frame("GA_Page"))
        calcmenu.add_command(label="----")#, command=hello)
        menubar.add_cascade(label="Cálculos", menu=calcmenu)
		
        menubar.add_command(label="Acerca", command=lambda: controller.show_frame("AboutPage"))

        menubar.add_command(label="Salir", command=self.close)

        LabelTitulo = tk.Label(self, text="Diseño de un Rotor de Generación Eólica", font=controller.title_font)
        LabelTitulo.pack(side="top", fill="x", pady=10)
        LabelSubtitulo = tk.Label(self, text="Optimización con Algoritmos Genéticos", font=controller.subtitle_font)
        LabelSubtitulo.pack(side="top", fill="x", pady=10)
        LabelFoto=Label(self, image=controller.image).pack(expand='yes',side='bottom',fill='both')
        controller.configure(menu = menubar)
        

    def loadA(self):
        self.controller.TxtAlp1.set(str(7))
        self.controller.TxtPos1.set(str(0))
        self.controller.TxtAlp2.set(str(0))
        self.controller.TxtPos2.set(str(0))
        self.controller.TxtAlp3.set(str(0))
        self.controller.TxtPos3.set(str(0))
        self.controller.TxtAlp4.set(str(0))
        self.controller.TxtSec.set(str(200))
        self.controller.TxtIter.set(str(5000))
        self.controller.TxtConv.set(str(1e-6))
        self.controller.ChkVar1.set(0)
        self.controller.ChkVar2.set(0)
        self.controller.ChkVar3.set(0)
        self.controller.ComboVar.set(3)
        self.controller.RadioVar.set(0)
        self.controller.TxtPerfil1.set('Perfiles/sg6043.csv')
        self.controller.TxtPerfil2.set('Perfiles/sg6040.csv')
        self.controller.TxtPerfil3.set('Perfiles/s826.csv')
        self.controller.TxtPerfil4.set('Perfiles/sg6043.csv')
        self.controller.show_frame("CalcPage")

    def loadB1(self):
        self.controller.TxtAlp1.set(str(8.75))
        self.controller.TxtPos1.set(str(0.297))
        self.controller.TxtAlp2.set(str(7.25))
        self.controller.TxtPos2.set(str(0))
        self.controller.TxtAlp3.set(str(0))
        self.controller.TxtPos3.set(str(0))
        self.controller.TxtAlp4.set(str(0))
        self.controller.TxtSec.set(str(200))
        self.controller.TxtIter.set(str(5000))
        self.controller.TxtConv.set(str(1e-6))
        self.controller.ChkVar1.set(1)
        self.controller.ChkVar2.set(0)
        self.controller.ChkVar3.set(0)
        self.controller.ComboVar.set(3)
        self.controller.RadioVar.set(0)
        self.controller.TxtPerfil1.set('Perfiles/s825.csv')
        self.controller.TxtPerfil2.set('Perfiles/sg6043.csv')
        self.controller.TxtPerfil3.set('Perfiles/s826.csv')
        self.controller.TxtPerfil4.set('Perfiles/sg6043.csv')
        self.controller.show_frame("CalcPage")
    
    def loadB2(self):
        self.controller.TxtAlp1.set(str(8.92))
        self.controller.TxtPos1.set(str(0.326))
        self.controller.TxtAlp2.set(str(7))
        self.controller.TxtPos2.set(str(0))
        self.controller.TxtAlp3.set(str(0))
        self.controller.TxtPos3.set(str(0))
        self.controller.TxtAlp4.set(str(0))
        self.controller.TxtSec.set(str(200))
        self.controller.TxtIter.set(str(5000))
        self.controller.TxtConv.set(str(1e-6))
        self.controller.ChkVar1.set(1)
        self.controller.ChkVar2.set(0)
        self.controller.ChkVar3.set(0)
        self.controller.ComboVar.set(3)
        self.controller.RadioVar.set(0)
        self.controller.TxtPerfil1.set('Perfiles/sg6040.csv')
        self.controller.TxtPerfil2.set('Perfiles/sg6043.csv')
        self.controller.TxtPerfil3.set('Perfiles/s826.csv')
        self.controller.TxtPerfil4.set('Perfiles/sg6043.csv')
        self.controller.show_frame("CalcPage")

    def loadLupita(self):
        self.controller.TxtAlp1.set(str(8.75))
        self.controller.TxtPos1.set(str(0.15))
        self.controller.TxtAlp2.set(str(9))
        self.controller.TxtPos2.set(str(0.35))
        self.controller.TxtAlp3.set(str(8.25))
        self.controller.TxtPos3.set(str(0.75))
        self.controller.TxtAlp4.set(str(7.25))
        self.controller.TxtSec.set(str(18))
        self.controller.TxtIter.set(str(1000))
        self.controller.TxtConv.set(str(1e-5))
        self.controller.ChkVar1.set(1)
        self.controller.ChkVar2.set(1)
        self.controller.ChkVar3.set(1)
        self.controller.ComboVar.set(2)
        self.controller.RadioVar.set(1)
        self.controller.TxtPerfil1.set('Perfiles/s835.csv')
        self.controller.TxtPerfil2.set('Perfiles/sg6040.csv')
        self.controller.TxtPerfil3.set('Perfiles/s826.csv')
        self.controller.TxtPerfil4.set('Perfiles/sg6043.csv')
        self.controller.show_frame("CalcPage")

    def close(self):
        if tk.messagebox.askokcancel("Atención","¿Desea cerrar la ventana?"):
            self.controller.destroy()
            

    def saveCase(self):
        if self.controller.CalcDone == 1:

            f = open('Cp_'+str(self.controller.Valores['cp'])+'.txt','w+')
            f.write("Regression Method: "+self.controller.combo.get())
            f.write('\n')
            f.write("Iterations: "+self.controller.TxtIter.get())
            f.write('\n')
            f.write("Spanwise Elements: "+self.controller.TxtSec.get())
            f.write('\n')
            f.write("Convergence Criteria: "+self.controller.TxtConv.get())
            for key, val in self.controller.Valores.items():
                f.write('\n')
                f.write(key)
                f.write('\n')
                f.write(str(val))
                f.write('\n')
            
            f.close()
            tk.messagebox.showinfo(title="Listo!",message="Archivo Guardado en el directorio de la aplicación\n"+'Cp_'+str(self.controller.Valores['cp'])+'.txt')

        if self.controller.GADone==1:
            f = open('GA_Cp_'+str(self.controller.BestChrom['Fitness'])+'.txt','w+')
            for key, val in self.controller.BestChrom.items():
                f.write('\n')
                f.write(key)
                f.write('\n')
                f.write(str(val))
                f.write('\n')
            for key, val in self.controller.paramEjec.items():
                f.write('\n')
                f.write(key)
                f.write('\n')
                f.write(str(val))
                f.write('\n')
            f.close()
            tk.messagebox.showinfo(title="Listo!",message="Archivo Guardado en el directorio de la aplicación\n"+'GA_Cp_'+str(self.controller.BestChrom['Fitness'])+'.txt')

class CalcPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.bind("<<ShowFrame>>", self.On_Show)



        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid(sticky="nsew")
        
        
        self.controller.TxtPerfil1.set('Perfiles/s835.csv')
        self.controller.TxtPerfil2.set('Perfiles/sg6040.csv')
        self.controller.TxtPerfil3.set('Perfiles/s826.csv')
        self.controller.TxtPerfil4.set('Perfiles/sg6043.csv')

        self.controller.TxtAlp1.set("7.3491")
        self.controller.TxtPos1.set("0.07918")
        self.controller.TxtAlp2.set("9.9134")
        self.controller.TxtPos2.set("0.595326")
        self.controller.TxtAlp3.set("9.5892")
        self.controller.TxtPos3.set("0.774715")
        self.controller.TxtAlp4.set("7.9370")
        self.controller.TxtSec.set("18")
        self.controller.TxtIter.set("500")
        self.controller.TxtConv.set("1e-5")

        self.TxtCoefPot = StringVar()
        self.TxtCoefPot.set('Cp: ___')
        
        self.Opt = IntVar()
        self.N_Perf=npy.zeros(4,dtype=int)
        self.N_Perf[0]=self.controller.Perf1.get()
        #self.Opt=1
        LabelDatos=Label(self,text="Datos de Perfil",width=20).grid(row=1,column=3)
        Label(self,text="_____________________________________________",width=30).grid(row=2,column=2,columnspan=3)
        LabelPerfil1=Label(self, textvariable=self.controller.TxtPerfil1, width=20).grid(row=3,column=3)
        Label(self,text="Ángulo Alpha",width=15).grid(row=4, column=2, sticky="e")
        Label(self,text="_____________________________________________",width=30).grid(row=5,column=2,columnspan=3)
        LabelPerfil2=Label(self, textvariable=self.controller.TxtPerfil2, width=20).grid(row=6,column=3)
        Label(self,text="Cambio de Perfil",width=15).grid(row=7,column=2, sticky="e")
        Label(self,text="Ángulo Alpha",width=15).grid(row=8, column=2, sticky="e")
        Label(self,text="_____________________________________________",width=30).grid(row=9,column=2,columnspan=3)
        LabelPerfil3=Label(self, textvariable=self.controller.TxtPerfil3, width=20).grid(row=10,column=3)
        Label(self,text="Cambio de Perfil",width=15).grid(row=11,column=2, sticky="e")
        Label(self,text="Ángulo Alpha",width=15).grid(row=12, column=2, sticky="e")
        Label(self,text="_____________________________________________",width=30).grid(row=13,column=2,columnspan=3)
        LabelPerfil4=Label(self, textvariable=self.controller.TxtPerfil4, width=20).grid(row=14,column=3)
        Label(self,text="Cambio de Perfil",width=15).grid(row=15,column=2, sticky="e")
        Label(self,text="Ángulo Alpha",width=15).grid(row=16, column=2, sticky="e")
        Label(self,text="_____________________________________________",width=30).grid(row=17,column=2,columnspan=3)
        Label(self,text="Modelo Regresión",width=15).grid(row=18, column=2, sticky="e")
        RadBtnOpt1= Radiobutton(self,text="Aproximación de Valores",  value=1, variable=self.Opt, indicatoron=False).grid(row=19,column=2)
        RadBtnOpt0= Radiobutton(self,text='Interpolación de Valores' , value=0, variable=self.Opt, indicatoron=False).grid(row=19,column=3)
        Label(self,text="_____________________________________________",width=30).grid(row=20,column=2,columnspan=3)
        Label(self,text="Número de Elementos\n de pala", width=17).grid(row=21,column=2, sticky="e")
        Label(self,text="Número Máximo\n de iteraciones", width=17).grid(row=22,column=2, sticky="e")
        Label(self,text="Criterio de \n Convergencia", width=17).grid(row=23,column=2, sticky="e")
        Label(self,text="_____________________________________________",width=30).grid(row=24,column=2,columnspan=3)
        
        LabelCoefPot=Label(self, textvariable=self.TxtCoefPot, width=20).grid(row=25,column=3)
        LabelDatos=Label(self,text="_",width=35).grid(row=25,column=1)

        self.BtnAbrir1 = Button(self, text = "Abrir", command = lambda: self.AbrirArchivo(1),width=12)
        self.BtnAbrir1.grid(row=3,column=4,padx=4)
        self.BtnAbrir2 = Button(self, text = "Abrir", command = lambda: self.AbrirArchivo(2),width=12,state='normal')
        self.BtnAbrir2.grid(row=6,column=4,padx=4)
        self.BtnAbrir3 = Button(self, text = "Abrir", command = lambda: self.AbrirArchivo(3),width=12,state='normal')
        self.BtnAbrir3.grid(row=10,column=4,padx=4)
        self.BtnAbrir4 = Button(self, text = "Abrir", command = lambda: self.AbrirArchivo(4),width=12,state='normal')
        self.BtnAbrir4.grid(row=14,column=4,padx=4)

        self.ComboLinReg =  ttk.Combobox(self,state="readonly",textvariable=self.controller.combo, values=["poly","cubic","quadraticLupita","None"], )
        self.ComboLinReg.grid(row=18,column=3)
        #self.ComboLinReg.current(3)
        BtnCalculo = Button(self, text = "Calcular",command = self.Calculo,width=12).grid(row=25,column=4,padx=4)
        BtnRegresar = Button(self, text="Atrás", command= lambda: controller.show_frame("StartPage"),width=12).grid(row=1,column=1)

        self.ChkPerf1 = Checkbutton(self,text="Habilitar",variable=self.controller.ChkVar1,command=self.PerfState)
        self.ChkPerf1.grid(row=6,column=2)
        self.ChkPerf1.select()
        self.ChkPerf2 = Checkbutton(self,text="Habilitar",variable=self.controller.ChkVar2,command=self.PerfState)
        self.ChkPerf2.grid(row=10,column=2)
        self.ChkPerf2.select()
        self.ChkPerf3 = Checkbutton(self,text="Habilitar",variable=self.controller.ChkVar3,command=self.PerfState)
        self.ChkPerf3.grid(row=14,column=2)
        self.ChkPerf3.select()

        self.CajaAlpha1 = Entry(self, textvariable=self.controller.TxtAlp1)
        self.CajaAlpha1.grid(row=4,column=3)
        self.CajaPos1 = Entry(self, textvariable=self.controller.TxtPos1,state='normal')
        self.CajaPos1.grid(row=7,column=3)
        self.CajaAlpha2 = Entry(self, textvariable=self.controller.TxtAlp2,state='normal')
        self.CajaAlpha2.grid(row=8,column=3)
        self.CajaPos2 = Entry(self, textvariable=self.controller.TxtPos2,state='normal')
        self.CajaPos2.grid(row=11,column=3)
        self.CajaAlpha3 = Entry(self, textvariable=self.controller.TxtAlp3,state='normal')
        self.CajaAlpha3.grid(row=12,column=3)
        self.CajaPos3 = Entry(self, textvariable=self.controller.TxtPos3,state='normal')
        self.CajaPos3.grid(row=15,column=3)
        self.CajaAlpha4 = Entry(self, textvariable=self.controller.TxtAlp4,state='normal')
        self.CajaAlpha4.grid(row=16,column=3)
        self.CajaSec = Entry(self, textvariable=self.controller.TxtSec)
        self.CajaSec.grid(row=21,column=3)
        self.CajaIter = Entry(self, textvariable=self.controller.TxtIter)
        self.CajaIter.grid(row=22,column=3)
        self.CajaConv = Entry(self, textvariable=self.controller.TxtConv)
        self.CajaConv.grid(row=23,column=3)
        self.controller.ngraph=0
        self.Graph([0,0],[0,0],'Eje X','Eje Y')
    def On_Show(self,event):
        self.PerfState()
        

    def PerfState(self):

        self.ComboLinReg.current(self.controller.ComboVar.get())
        self.Opt.set(self.controller.RadioVar.get())

        if self.controller.ChkVar1.get()==0:
            self.CajaPos1['state']='disabled'
            self.CajaAlpha2['state']='disabled'
            self.BtnAbrir2['state']='disabled'
            
        elif self.controller.ChkVar1.get()==1:
            self.CajaPos1['state']='normal'
            self.CajaAlpha2['state']='normal'
            self.BtnAbrir2['state']='normal'
            

        if self.controller.ChkVar2.get()==0:
            self.CajaPos2['state']='disabled'
            self.CajaAlpha3['state']='disabled'
            self.BtnAbrir3['state']='disabled'
            
        elif self.controller.ChkVar2.get()==1:
            self.CajaPos2['state']='normal'
            self.CajaAlpha3['state']='normal'
            self.BtnAbrir3['state']='normal'
            

        if self.controller.ChkVar3.get()==0:
            self.CajaPos3['state']='disabled'
            self.CajaAlpha4['state']='disabled'
            self.BtnAbrir4['state']='disabled'
            
        elif self.controller.ChkVar3.get()==1:
            self.CajaPos3['state']='normal'
            self.CajaAlpha4['state']='normal'
            self.BtnAbrir4['state']='normal'
            


    def SigGraph(self,NoGraf):
        
        self.controller.ngraph+=NoGraf
        if self.controller.ngraph==1:
            self.Graph(self.controller.Valores['l'],self.controller.Valores['c'],"Longitud [r/L]","Cuerda [y/c]")
        if self.controller.ngraph==2:
            self.Graph(self.controller.Valores['l'],self.controller.Valores['phig'],"Longitud [r/L]","Angulo Phi [°]")
        if self.controller.ngraph==3:
            self.Graph(self.controller.Valores['l'],self.controller.Valores['theta_p'],"Longitud [r/L]","Angulo Theta [°]")
            self.controller.ngraph=0
        BtnSigGraf = Button(self, text="Sig ->", command=lambda: self.SigGraph(1),width=12).grid(row=25,column=1,padx=4)
        
    def Graph(self,DatosX,DatosY,titleX,titleY):
        plotframe = tk.Frame(self)
        plotframe.grid(column=1,row=2,rowspan=25,sticky="nsew")
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        
        a.plot(DatosX,DatosY)
        a.set_xlabel(titleX)
        a.set_ylabel(titleY)
        a.grid(color='r', linestyle='-', linewidth=0.5)
        # for i in range(len(DatosY)):
        #     a.plot(DatosX[i],DatosY[i],'o', color='green')
        canvas = FigureCanvasTkAgg(f, plotframe)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(canvas, plotframe)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def AbrirArchivo(self,value):
        filename = tk.filedialog.askopenfilename(initialdir = "A:\Tesis\Codigo\Perfiles",title="Elige solo archivos CSV...",filetypes = (("Archivos CSV","*.csv"),("all files","*.*"))) # show an "Open" dialog box and return the path to the selected file
        if filename != '':
            if value==1:
                self.controller.TxtPerfil1.set(filename)
            if value==2:
                self.controller.TxtPerfil2.set(filename)
            if value==3:
                self.controller.TxtPerfil3.set(filename)
            if value==4:
                self.controller.TxtPerfil4.set(filename)
            
    def Calculo(self):
        self.controller.ComboVar.set(self.ComboLinReg.current())
        self.controller.RadioVar.set(self.Opt.get())

        DatTemp=[self.CajaAlpha1.get(),self.CajaAlpha2.get(),self.CajaAlpha3.get(),
        self.CajaAlpha4.get(),self.CajaPos1.get(),self.CajaPos2.get(),self.CajaPos3.get()]
        if DatTemp[0]=="None":
            self.N_Perf[0]=0
        else:
            self.N_Perf[0]=1
        for i in range(7):
            if DatTemp[i]=="None":
                DatTemp[i]=0
            else:
                DatTemp[i]=float(DatTemp[i])
        # Datos=npy.array([float(self.CajaAlpha1.get()),float(self.CajaAlpha2.get()),float(self.CajaAlpha3.get()),
        # float(self.CajaAlpha4.get()),float(self.CajaPos1.get()),float(self.CajaPos2.get()),float(self.CajaPos3.get())])
        Datos= npy.asarray(DatTemp)
        Convergencia=npy.array([float(self.CajaSec.get()),float(self.CajaIter.get()),float(self.CajaConv.get())])
        
        RutaStr=npy.array([self.controller.TxtPerfil1.get(),self.controller.TxtPerfil2.get(),self.controller.TxtPerfil3.get(),self.controller.TxtPerfil4.get()])
        self.controller.ngraph=1
        
        self.N_Perf[1]=self.controller.ChkVar1.get()
        self.N_Perf[2]=self.controller.ChkVar2.get()
        self.N_Perf[3]=self.controller.ChkVar3.get()
        # if self.controller.GADone ==1:
        #     N_Perf=npy.array([self.controller.Perf1,self.controller.ChkVar1.get(),self.controller.ChkVar2.get(),self.controller.ChkVar3.get()])
        
        # if self.controller.GADone ==0:
        #     N_Perf=npy.array([self.controller.Perf1,self.controller.ChkVar1,self.controller.ChkVar2,self.controller.ChkVar3])
        
        print(self.controller.combo.get())
        self.controller.Valores=clase.Coef_Potencia.Calculo(self,RutaStr,Datos,Convergencia,self.N_Perf,self.Opt.get(),self.controller.combo.get())
        self.controller.CalcDone=1
        
        self.TxtCoefPot.set("Cp:\n "+ str(self.controller.Valores['cp']))
        self.Graph(self.controller.Valores['l'],self.controller.Valores['c'],"Longitud [r/L]","Cuerda [y/c]")

        BtnSigGraf = Button(self, text="Sig ->", command=lambda: self.SigGraph(1),width=12).grid(row=25,column=1,padx=4)
        
class GA_Page(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller=controller
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid(sticky="nsew")
        
        self.TxtCrom = StringVar()
        self.TxtCrom.set('100')
        self.TxtGen = StringVar()
        self.TxtGen.set("50")
        
        self.TxtLB = StringVar()
        self.TxtLB.set("1,0,0,0,4,6,6,6,0.2,0.12,0.1")
        self.TxtUB = StringVar()
        self.TxtUB.set('7,13,13,13,10,12,12,12,0.33,1,1')

        self.TxtPc = StringVar()
        self.TxtPc.set("0.95")
        self.TxtPm = StringVar()
        self.TxtPm.set("0.015")
        self.TxtEr = StringVar()
        self.TxtEr.set("0.05")   

        self.TxtConv= StringVar()
        self.TxtConv.set("1e-4")
        self.TxtIter = StringVar()
        self.TxtIter.set("2500")
        self.TxtSec = StringVar()
        self.TxtSec.set('200')

        self.TxtBestC = StringVar()
        self.TxtBestC.set('Candidato más ajustado:')

        self.Opt = IntVar()

        self.Calculado=False

        Label(self,text="Número de Cromosomas",width=35).grid(row=2, column=2, sticky="e")
        Label(self,text="Generaciones Máximas",width=35).grid(row=3,column=2, sticky="e")
        Label(self,text="_____________________________________________",width=35).grid(row=4,column=2,columnspan=3)

        Label(self,text="Limites Inferiores",width=35).grid(row=5, column=2, sticky="e")
        Label(self,text="Limites Superiores",width=35).grid(row=6,column=2, sticky="e")
        Label(self,text="_____________________________________________",width=35).grid(row=7,column=2,columnspan=3)
        Label(self,text="Probabilidad de Recombinación",width=35).grid(row=8, column=2, sticky="e")
        Label(self,text="Probabilidad de Mutación",width=35).grid(row=9,column=2, sticky="e")
        Label(self,text="Porcentaje de Elites", width=35).grid(row=10,column=2, sticky="e")
        Label(self,text="_____________________________________________",width=35).grid(row=11,column=2,columnspan=3)
        Label(self,text="Criterio de Convergencia",width=35).grid(row=12, column=2, sticky="e")           
        Label(self,text="Número Máximo de Iteraciones", width=35).grid(row=13,column=2, sticky="e")
        Label(self,text="_____________________________________________",width=35).grid(row=14,column=2,columnspan=3)
        Label(self,text="Número de Elementos de Pala", width=35).grid(row=15,column=2, sticky="e")
        Label(self,text="_____________________________________________",width=35).grid(row=17,column=2,columnspan=3)

        LabelBestChr=Label(self, textvariable=self.TxtBestC, width=90).grid(row=19,column=1,columnspan=2,sticky='s')
        Label(self,text="|",width=35).grid(row=18,column=1,columnspan=2,sticky='s')
        Label(self,text="|",width=35).grid(row=20,column=1,columnspan=2,sticky='s')

        RadBtnOpt1= Radiobutton(self,text="Selector: Rueda de Ruleta",  value=1, variable=self.Opt, indicatoron=False).grid(row=16,column=2)
        RadBtnOpt0= Radiobutton(self,text='Selector: Torneo' , value=0, variable=self.Opt, indicatoron=False).grid(row=16,column=3)

        BtnCalculo = Button(self, text = "Calcular",command = self.Calculo,width=15).grid(row=18,column=3,padx=4)
        BtnTraspaso = Button(self, text="Traspaso -> Cp",command=self.Traspaso, width=15 ).grid(row=19, column=3, padx=4)
        BtnRegresar = Button(self, text="Atrás", command= lambda: controller.show_frame("StartPage"),width=12).grid(row=1,column=1)
        #BtnSigGraf = Button(self, text="Sig ->", command= self.SigGraph,width=12).grid(row=19,column=1,padx=4)

        self.CajaCrom = Entry(self, textvariable=self.TxtCrom)
        self.CajaCrom.grid(row=2,column=3,padx=4)
        self.CajaGen = Entry(self, textvariable=self.TxtGen)
        self.CajaGen.grid(row=3,column=3,padx=4)
        self.CajaLB = Entry(self, textvariable=self.TxtLB)
        self.CajaLB.grid(row=5,column=3,padx=4)
        self.CajaUB = Entry(self, textvariable=self.TxtUB)
        self.CajaUB.grid(row=6,column=3,padx=4)
        self.CajaPc = Entry(self, textvariable=self.TxtPc)
        self.CajaPc.grid(row=8,column=3,padx=4)
        self.CajaPm = Entry(self, textvariable=self.TxtPm)
        self.CajaPm.grid(row=9,column=3,padx=4)
        self.CajaEr = Entry(self, textvariable=self.TxtEr)
        self.CajaEr.grid(row=10,column=3,padx=4)
        self.CajaConv = Entry(self, textvariable=self.TxtConv)
        self.CajaConv.grid(row=12,column=3,padx=4)
        self.CajaIter = Entry(self, textvariable=self.TxtIter)
        self.CajaIter.grid(row=13,column=3,padx=4)
        self.CajaSec = Entry(self, textvariable=self.TxtSec)
        self.CajaSec.grid(row=15,column=3,padx=4)

        self.Graph([1,1],[1,1],'Eje X','Eje Y')
        
        
    def Graph(self,DatosX,DatosY,titleX,titleY):
        plotframe = tk.Frame(self)
        plotframe.grid(column=1,row=2,rowspan=17,sticky="nsew")
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.semilogy(DatosX,DatosY)
        a.set_xlabel(titleX)
        a.set_ylabel(titleY)
        a.grid(color='r', linestyle='-', linewidth=0.5)
        for i in range(len(DatosY)):
            a.plot(DatosX[i],DatosY[i],'o', color='green')
        canvas = FigureCanvasTkAgg(f, plotframe)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(canvas, plotframe)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def Calculo(self):
        Limits={}
        Limits['LB']=npy.fromstring(self.CajaLB.get(), sep=',')
        Limits['UB']=npy.fromstring(self.CajaUB.get(), sep=',')
        Convergencia=npy.array([float(self.CajaIter.get()),float(self.CajaConv.get()),float(self.CajaSec.get())])
        Datos=npy.array([float(self.CajaCrom.get()),float(self.CajaGen.get()),float(self.CajaPc.get()),float(self.CajaPm.get()),float(self.CajaEr.get())])
        
        
        self.Error=[]
        self.controller.BestChrom,self.Error,self.controller.paramEjec=GA.Main_GA(Datos,Limits,Convergencia,self.Opt.get())
        self.TxtBestC.set('Cp: '+str(self.controller.BestChrom['Fitness'])+'\nPerf: '+str(self.controller.BestChrom['Chromo'][0:4])+'\nAlpha: '+str(self.controller.BestChrom['Chromo'][4:8])+'\nU: '+str(self.controller.BestChrom['Chromo'][8:11]))
        self.controller.GADone=1
        if (int(Datos[1])==1):
            self.Graph([1],self.Error,'Número de Generaciones', 'Error')
        elif int(Datos[1])>1:
            self.Graph(range(1,len(self.Error)+1),self.Error,'Número de Generaciones', 'Error')


    def Traspaso(self):
        ListaPerf=['PerfZeros','s823','s808','s835','s833','s825','s825n','sg6040','s834','s826','s826n','s801','sg6041','sg6043','e387','fx63137','PerfCircular']
       
        if self.controller.GADone==1:

            if self.controller.BestChrom['Chromo'][0]>=1:
                self.controller.TxtAlp1.set(str(self.controller.BestChrom['Chromo'][4]))
                self.controller.TxtPerfil1.set('Perfiles/'+str(ListaPerf[int(self.controller.BestChrom['Chromo'][0])])+'.csv')
            elif self.controller.BestChrom['Chromo'][0]==0:
                self.controller.TxtAlp1.set("None")
                self.controller.Perf1=0

            if  self.controller.BestChrom['Chromo'][1]>=1:
                self.controller.TxtPos1.set(str(self.controller.BestChrom['Chromo'][8]))
                self.controller.TxtAlp2.set(str(self.controller.BestChrom['Chromo'][5]))
                self.controller.TxtPerfil2.set('Perfiles/'+str(ListaPerf[int(self.controller.BestChrom['Chromo'][1])])+'.csv')
                self.controller.ChkVar1.set(1)
            elif self.controller.BestChrom['Chromo'][1]==0:
                self.controller.ChkVar1.set(0)
                #self.controller.ChkPerf1['state']='disabled'
                self.controller.TxtPos1.set("None")
                self.controller.TxtAlp2.set("None")
            
            if self.controller.BestChrom['Chromo'][2]>=1:
                self.controller.TxtPos2.set(str(self.controller.BestChrom['Chromo'][9]))
                self.controller.TxtAlp3.set(str(self.controller.BestChrom['Chromo'][6]))
                self.controller.TxtPerfil3.set('Perfiles/'+str(ListaPerf[int(self.controller.BestChrom['Chromo'][2])])+'.csv')
                self.controller.ChkVar2.set(1)
            elif self.controller.BestChrom['Chromo'][2]==0:
                self.controller.ChkVar2.set(0)
                #self.controller.ChkPerf2['state']='disabled'
                self.controller.TxtPos2.set("None")
                self.controller.TxtAlp3.set("None")

            if self.controller.BestChrom['Chromo'][3]>=1:
                self.controller.TxtPos3.set(str(self.controller.BestChrom['Chromo'][10]))
                self.controller.TxtAlp4.set(str(self.controller.BestChrom['Chromo'][7]))
                self.controller.TxtPerfil4.set('Perfiles/'+str(ListaPerf[int(self.controller.BestChrom['Chromo'][3])])+'.csv')
                self.controller.ChkVar3.set(1)
            elif self.controller.BestChrom['Chromo'][3]==0:
                self.controller.ChkVar3.set(0)
                #self.controller.ChkPerf3['state']='disabled'
                self.controller.TxtPos3.set("None")
                self.controller.TxtAlp4.set("None")
                
            self.controller.TxtSec.set(self.TxtSec.get())
            self.controller.TxtIter.set(self.TxtIter.get())
            self.controller.TxtConv.set(self.TxtConv.get())
            self.controller.ComboVar.set(3)
            self.controller.RadioVar.set(0)
            # self.controller.PerfState()
            self.controller.show_frame("CalcPage")

class AboutPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_columnconfigure( 1, weight=1)
        self.Txt = StringVar()
        self.hiperLinkText =StringVar()
        self.hiperLinkText.set("\n\nEste software está bajo licencia GNU/GPL")
        self.Txt.set("Software implementado en Python 3.x \n (González G., Mauricio N.). 2019. Optimización del Diseño Aerodinámico (BEM-CFD)de un Microaerogenerador \n mediante Algoritmos Genéticos, Computo Paralelo y OpenFOAM \n\nRevisión y optimización, e implementación del algoritmo génetico, \ny para coeficiente de potencia utilizado para este software: \nMauricio Nahún González Guevara\nmauricio.nahun.gg@gmail.com\n2019") 
        LabelAcerca = Label(self, text="Acerca del software",font=controller.title_font)
        LabelAcerca.grid(column=1,row=1,sticky='nswe')
        LabelDat=Label(self, width=120, textvariable=self.Txt)
        LabelDat.grid(column=1,row=2,sticky='we')
        LabelHiperLink=Label(self, width=120, textvariable=self.hiperLinkText, fg="blue", cursor="hand2")
        LabelHiperLink.grid(column=1,row=3,sticky='we')
        LabelHiperLink.bind("<Button-1>", lambda e: self.hiperLink_call("https://www.gnu.org/licenses/gpl-3.0.txt"))
        
        LabelFoto=Label(self, image=controller.imageIco).grid(column=1,row=4,sticky='we')
        button1 = Button(self, text="Regresar",command=lambda: controller.show_frame("StartPage"))
        button1.grid(column=1,row=5)


    def hiperLink_call(self,url):
        webbrowser.open_new(url)


        
class GA_Param_Page(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller=controller
        LabelDatos=Label(self,text="Configuración de los Límites de Búsqueda",width=60).grid(row=1,column=3)
        Label(self,text="_____________________________________________",width=30).grid(row=2,column=2,columnspan=3)

        Label(self,text="Relación de Velocidad de Punta",width=15).grid(row=4, column=2, sticky="e")
        Label(self,text="_____________________________________________",width=30).grid(row=5,column=2,columnspan=3)

        Label(self,text="Radio",width=15).grid(row=7,column=2, sticky="e")
        Label(self,text="Número de Palas",width=15).grid(row=8, column=2, sticky="e")
        Label(self,text="_____________________________________________",width=30).grid(row=9,column=2,columnspan=3)

        Label(self,text="Número de Perfiles",width=15).grid(row=11,column=2, sticky="e")
        Label(self,text="Ángulo Alpha",width=15).grid(row=12, column=2, sticky="e")
        Label(self,text="_____________________________________________",width=30).grid(row=13,column=2,columnspan=3)

        Label(self,text="Cambio de Perfil",width=15).grid(row=15,column=2, sticky="e")
        Label(self,text="Ángulo Alpha",width=15).grid(row=16, column=2, sticky="e")
        Label(self,text="_____________________________________________",width=30).grid(row=17,column=2,columnspan=3)
        Label(self,text="Modelo Regresión",width=15).grid(row=18, column=2, sticky="e")
        # RadBtnOpt1= Radiobutton(self,text="Aproximación de Valores",  value=1, variable=self.Opt, indicatoron=False).grid(row=19,column=2)
        # RadBtnOpt0= Radiobutton(self,text='Interpolación de Valores' , value=0, variable=self.Opt, indicatoron=False).grid(row=19,column=3)
        Label(self,text="_____________________________________________",width=30).grid(row=20,column=2,columnspan=3)
        Label(self,text="Número de Elementos\n de pala", width=17).grid(row=21,column=2, sticky="e")
        Label(self,text="Número Máximo\n de iteraciones", width=17).grid(row=22,column=2, sticky="e")
        Label(self,text="Criterio de \n Convergencia", width=17).grid(row=23,column=2, sticky="e")
        Label(self,text="_____________________________________________",width=30).grid(row=24,column=2,columnspan=3)
        
        # LabelCoefPot=Label(self, textvariable=self.TxtCoefPot, width=20).grid(row=25,column=3)
        # LabelDatos=Label(self,text="_",width=35).grid(row=25,column=1)

        # self.BtnAbrir1 = Button(self, text = "Abrir", command = lambda: self.AbrirArchivo(1),width=12)
        # self.BtnAbrir1.grid(row=3,column=4,padx=4)
        # self.BtnAbrir2 = Button(self, text = "Abrir", command = lambda: self.AbrirArchivo(2),width=12,state='normal')
        # self.BtnAbrir2.grid(row=6,column=4,padx=4)
        # self.BtnAbrir3 = Button(self, text = "Abrir", command = lambda: self.AbrirArchivo(3),width=12,state='normal')
        # self.BtnAbrir3.grid(row=10,column=4,padx=4)
        # self.BtnAbrir4 = Button(self, text = "Abrir", command = lambda: self.AbrirArchivo(4),width=12,state='normal')
        # self.BtnAbrir4.grid(row=14,column=4,padx=4)

        # self.ComboLinReg =  ttk.Combobox(self,state="readonly",textvariable=self.controller.combo, values=["poly","cubic","quadraticLupita","None"], )
        # self.ComboLinReg.grid(row=18,column=3)
        # self.ComboLinReg.current(3)
        # BtnCalculo = Button(self, text = "Calcular",command = self.Calculo,width=12).grid(row=25,column=4,padx=4)
        # BtnRegresar = Button(self, text="Atrás", command= lambda: controller.show_frame("StartPage"),width=12).grid(row=1,column=1)

        # self.ChkPerf1 = Checkbutton(self,text="Habilitar",variable=self.controller.ChkVar1,command=self.PerfState)
        # self.ChkPerf1.grid(row=6,column=2)
        # self.ChkPerf1.select()
        # self.ChkPerf2 = Checkbutton(self,text="Habilitar",variable=self.controller.ChkVar2,command=self.PerfState)
        # self.ChkPerf2.grid(row=10,column=2)
        # self.ChkPerf2.select()
        # self.ChkPerf3 = Checkbutton(self,text="Habilitar",variable=self.controller.ChkVar3,command=self.PerfState)
        # self.ChkPerf3.grid(row=14,column=2)
        # self.ChkPerf3.select()

        # self.CajaAlpha1 = Entry(self, textvariable=self.controller.TxtAlp1)
        # self.CajaAlpha1.grid(row=4,column=3)
        # self.CajaPos1 = Entry(self, textvariable=self.controller.TxtPos1,state='normal')
        # self.CajaPos1.grid(row=7,column=3)
        # self.CajaAlpha2 = Entry(self, textvariable=self.controller.TxtAlp2,state='normal')
        # self.CajaAlpha2.grid(row=8,column=3)
        # self.CajaPos2 = Entry(self, textvariable=self.controller.TxtPos2,state='normal')
        # self.CajaPos2.grid(row=11,column=3)
        # self.CajaAlpha3 = Entry(self, textvariable=self.controller.TxtAlp3,state='normal')
        # self.CajaAlpha3.grid(row=12,column=3)
        # self.CajaPos3 = Entry(self, textvariable=self.controller.TxtPos3,state='normal')
        # self.CajaPos3.grid(row=15,column=3)
        # self.CajaAlpha4 = Entry(self, textvariable=self.controller.TxtAlp4,state='normal')
        # self.CajaAlpha4.grid(row=16,column=3)
        # self.CajaSec = Entry(self, textvariable=self.controller.TxtSec)
        # self.CajaSec.grid(row=21,column=3)
        # self.CajaIter = Entry(self, textvariable=self.controller.TxtIter)
        # self.CajaIter.grid(row=22,column=3)
        # self.CajaConv = Entry(self, textvariable=self.controller.TxtConv)
        # self.CajaConv.grid(row=23,column=3)
if __name__ == "__main__":
    app = GenxRotor()
    wid=1000
    hei=680
    app.geometry(("%dx%d" % (wid,hei)))
    app.title('GenxRotor v0.7 [beta]')
    app.iconbitmap('icono/GalaxyM101.ico')
    app.mainloop()

