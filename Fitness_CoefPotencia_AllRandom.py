# !/usr/bin/python3
# -*- coding: utf-8 -*-
#Importaciones necesarias
import numpy as npy
from numpy.linalg import inv
import math 
import timeit

#import CodigoFuncionesComp as fcp

class Coef_Potencia:

    def Calculo(val,Convergencia):
        
        idxVal=[None]
        idxBorr=[None]
        N_perf=0

        tempPerf=val[0:4]
        tempPos=val[8:11]
        tempPos.append(1)
        for i in range(4):
            if tempPerf[i]>0:
                idxVal.append(i)
                N_perf=N_perf+1
            
        del idxVal[0]      
        for i in range(N_perf-1):
            for j in range(N_perf-1):
                if tempPos[i]>tempPos[j+1]:
                    idxBorr.append(j+1) 

        del idxBorr[0]

        idxVal=npy.delete(npy.asarray(idxVal),idxBorr).tolist()
        N_perf=len(idxVal)

        valores=npy.asarray(val)
        
        for i in range(N_perf):
            valores[i]=val[idxVal[i]]
            valores[i+4]=val[idxVal[i]+4]

        for i in range(N_perf-1):
            valores[i+8]=val[i+8]
        
        N_Perf=valores[0:4]
        valores=valores[4:]
        ListaPerf=['PerfZeros','s823','s808','s835','s833','s825','s825n','sg6040','s834','s826','s826n','s801','sg6041','sg6043','e387','fx63137','PerfCircular']
        pp1=npy.genfromtxt('Perfiles/'+str(ListaPerf[int(N_Perf[0])])+'.csv',delimiter=',')
        
        pp2=npy.genfromtxt('Perfiles/'+str(ListaPerf[int(N_Perf[1])])+'.csv',delimiter=',')
        
        pp3=npy.genfromtxt('Perfiles/'+str(ListaPerf[int(N_Perf[2])])+'.csv',delimiter=',')
        
        pp4=npy.genfromtxt('Perfiles/'+str(ListaPerf[int(N_Perf[3])])+'.csv',delimiter=',')

        ta=(int)(pp1.size/3)
        tb=(int)(pp2.size/3)
        tc=(int)(pp3.size/3)
        td=(int)(pp4.size/3)

        t=max(ta,tb,tc,td)

        caracperfil=npy.zeros((t,4*3))
        caracperfil[0:ta,0:3]=pp1
        caracperfil[0:tb,3:6]=pp2
        caracperfil[0:tc,6:9]=pp3
        caracperfil[0:td,9:12]=pp4 

        def limucuadinv(c,l):

            N=len(c)
            X=npy.column_stack((npy.ones(N),npy.power(l,2),npy.power(l,-1)))
            
            b= inv(X.T @ X) @ X.T @ c
            y=X @ b
            return y
            # s=npy.sum(npy.square(y-c))        #Se calcula el cuadrado de la diferencia para conocer el error
            # v=npy.zeros(len(b)+len(y)+1)      #y este se anexa al vector solucion además de las 
            # v[0:len(y)]=y                     # constantes de ajuste para b(1)+b(2)*r^2+b(3)/r
            # v[len(y):-1]=b
            # v[-1]=s
            # return v



        #funcion auxiliar en la busqueda de coeficientes de levantamiento y arrastre
            #para el angulo de ataque calculado

        def buscador(vec,val):
            t=0
            while val>vec[t]:
                t=t+1

            return t

        #la funcion regresa los coeficientes de levantamiento y arrastre del perfil
        #usado en la posicion dada de longitud r, para el angulo de ataque calculado:alpf.
        # def Coeficientes(alpha,indx):
        # Interpolción de Valores.----------

        def Coeficientes(alpha,indx,sType):

            if alpha>20:
                alpha=20
            elif alpha<-5:
                alpha=-5
            if sType=="Init":
                column=indx*3
            if sType=="Calc":
                column=int(perf[indx])*3
            row=buscador(caracperfil[:,column],alpha)   #opt=1 Lupita's Version
            #opt=0 Mauricio's version
            cL=caracperfil[row-1,column+1]+(alpha-caracperfil[row-1,column])*(caracperfil[row,column+1]-caracperfil[row-1,column+1])/(caracperfil[row,column]-caracperfil[row-1,column])
            cD=caracperfil[row-1,column+2]+(alpha-caracperfil[row-1,column])*(caracperfil[row,column+2]-caracperfil[row-1,column+2])/(caracperfil[row,column]-caracperfil[row-1,column])

            return cL,cD
            #ya que no se tiene la misma cantidad de datos para todos los pefiles se usa
            #la siguiente funcion para igualar la cantidad de filas de las matrices
            #anteriores y generar una nueva matriz que contenga los datos de todos los perfiles usados


        
        #tic=timeit.default_timer()

        lamda=6 #relacion de velocidad de punta
        OffSet=0.15
        R=1+OffSet #radio propuesto
        B=3 #numero de palas
        N=int(Convergencia[2]) #numero de divisiones de la pala 1,2,3,4,...18

        #el vector u define la ubicacion [r/R] de los puntos donde hay cambio de perfil
        #si el ultimo numero es igual a 1 el primer perfil solo esta en la raiz, 0 si
        #es usado en [r/R]<u[1]

       #idxVal, Lista que contiene los indices del vector valor para los perfiles seleccionados
        #considerando que siempre se guarda el primer perfil

               
        ##el vector u define la ubicacion [r/R] de los puntos donde hay cambio de perfil
        u=npy.ones(N_perf)+OffSet
        j=0
        for i in range(N_perf-1):
                u[i]=valores[i+4]

        if N_perf<=0:
            return [0]

        section_len=R/N #tamano de las secciones
        mid_section=section_len/2     #centro de las secciones
        r=npy.arange(mid_section,R,section_len) #Posiciones centrales de cada seccion de longitud
        perf=npy.ones(N)

        j=0
        for i in range(N):        #El vector Perf contiene el numero de perfil para cada sección                 
            if r[i]<=u[j]:          #según  la distrubición dada por el vector U
                perf[i]=j
            else:
                j=j+1
                perf[i]=j


        #caracteristicas de los perfiles elegidos
        Cld=npy.zeros(4)
        Cdd=npy.zeros(4)

        #asigna los valores de Cl y Cd según el angulo de ataque del perfil elegido 
        #Valores contiene dicho angulos de ataque
        for i in range(N_perf):
            Cld[i],Cdd[i]=Coeficientes(valores[i],i,"Init")

        #forma de la pala para un rotor optimo
        j=0
        
        lamda_r=lamda*r

        CL=npy.zeros(N)
        alp=npy.zeros(N)
        theta_p=npy.zeros(N)
        c=npy.zeros(N)
            
        phi=(2/3)*npy.arctan(1/lamda_r)

        for j in range(N):
            CL[j]=Cld[int(perf[j])]
            alp[j]=valores[int(perf[j])]

        c=(8*npy.pi*r*R)*((1-npy.cos(phi))/(B*CL))
        theta_p=phi-(alp*npy.pi/180)

        j=0
        k=0

        #buscando el punto maximo de la cuerda para el suavizado
        # while c[k]<c[k+1]:
        #     k=k+1

        #suavizando los valores de la cuerda y theta con una regresion lineal multiple tipo
        #    b(1)+b(2)*r^2+b(3)/r
        #tomando solo los valores apartir del elemento k es decir solo apartir del punto maximo 
        # de la cuerda
        # c[k:N]=limucuadinv( c[k:N] , r[k:N] )
        # theta_p[k:N]=limucuadinv( theta_p[k:N] , r[k:N] )



        indi=0#con este indicador consideramos solamente las secciones que no estan dentro del cubo

        # while r[indi]<0.075:
        #     indi=indi+1

        #calculo de coeficiente de potencia

        #inicializacion de los valores de angulo de viento relativo, a y a prima para el proceso iterativo
        # con las ecuaciones para pala optima

        i=slice(indi,N)

        sigmap=npy.divide(B* c[i],(2*npy.pi*r[i]*R))
        a=1/(1+npy.divide((4*npy.square(npy.sin(phi[i]))),(sigmap* CL[i]*npy.cos(phi[i]))))
        ap=(1-3*a)/(4*a-1)

        j=0
        i=0
        cp=0
        power=0

        ##//proceso iterativo para el calculo del coeficiente de potencia de la geometria
        ##// modificada (una vez suavizadas las curvas)

        phij=npy.zeros(N-indi)
        F=npy.ones(N-indi)
        alpp=npy.zeros(N-indi)
        Cl=npy.zeros(N-indi)
        Cd=npy.zeros(N-indi)
        CT=npy.zeros(N-indi)
        error=[[1,1,0]]
        for i in range(indi,N,1):
            t=1
            t2=1
            iterr=0
            #j=i-indi
            while (t>Convergencia[1] or t2>Convergencia[1]) and iterr<int(Convergencia[0]):
                
                phij[j]=math.atan((1-a[j])/((1+ap[j])*lamda_r[i]))
                
                try:
                    # F[j]=(2/math.pi)*math.acos(math.exp(-((B/2)*(1-r[i])/(r[i]*math.sin(phij[j])))))
                    F[j]=(2/math.pi)*math.acos(math.exp(-((B/2)*(1-(r[i]/R))/((r[i]/R)*math.sin(phij[j])))))
                except:
                    F[j]=1/(2*(j/(N-indi-1)))
                
                alpp[j]=(phij[j]-theta_p[i])*180/math.pi
                Cl[j],Cd[j]=Coeficientes(alpp[j],i,'Calc')
                CT[j]=(sigmap[j])*(math.pow(1-a[j],2))*(Cl[j]*math.cos(phij[j])+Cd[j]*math.sin(phij[j]))/(math.pow(math.sin(phij[j]),2))
                apn=1/((4*F[j]*math.cos(phij[j])/(sigmap[j]*Cl[j]))-1)


                if CT[j]<0.96:
                    an=1/(1+4*F[j]*(math.pow(math.sin(phij[j]),2))/(sigmap[j]*Cl[j]*math.cos(phij[j])))
                else:
                    an=(1/F[j])*(0.143+math.sqrt(0.0203-0.6427*(0.889-CT[j])))

                t=abs((a[j]-an)/an)
                t2=abs((ap[j]-apn)/apn)

                if an<1: 
                    a[j]=an
                    ap[j]=apn
                    
                else:
                    break
                
                iterr=iterr+1
            
            error.append([t,t2,iterr])
            cp+=(8/lamda**2)*F[j]*(math.pow(math.sin(phij[j]),2))*(math.cos(phij[j])-lamda_r[i]*math.sin(phij[j]))*(math.sin(phij[j])+lamda_r[i]*math.cos(phij[j]))*(1-(Cd[j]/Cl[j])*(1/math.tan(phij[j])))*math.pow(lamda_r[i],2)
            #power+=2*F[j]*ap[j]*(1-a[j])*1.225*6*(36**2)*(r[j]**2)*2*math.pi*r[j]*section_len
            j=j+1

        cp=cp*lamda/j

        if(cp<0):
            cp=0
        if(cp>0.59):
            cp=0.59
        #phi=phi*180/npy.pi
        # toc=timeit.default_timer()
        # tiempo_ejec=toc-tic
        
        # print("Coeficiente de potencia calculado:",cp)
        # print('tiempo de ejecucion:',tiempo_ejec, 'segundos')
        # print('------')
        p=0.5*cp*1.225*1*(6**3)*math.pi
        return [cp]

        

