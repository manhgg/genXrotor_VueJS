# !/usr/bin/python3
# -*- coding: utf-8 -*-
#Importaciones necesarias
import numpy as npy
from numpy.linalg import inv
import scipy as spy
import math 
import timeit
import csv
#import CodigoFuncionesComp as fcp

class Coef_Potencia:

    def Calculo(self,cadenaStr,valores,convergencia,N_Perf,opt,linRegModel):
        
        def linRegression(c,l,typeR):

            N=len(c)

            if typeR=="quadraticLupita":
                X=npy.column_stack((npy.ones(N),npy.power(l,2),npy.power(l,-1)))
            if typeR=="cubic":
                X=npy.column_stack((npy.ones(N),1/l,1/npy.power(l,2),1/npy.power(l,3)))
            if typeR=="poly":
                X=npy.column_stack((npy.ones(N),l,npy.power(l,2),npy.power(l,3),npy.power(l,4),npy.power(l,5),npy.power(l,6),npy.power(l,7),npy.power(l,8)))
            if typeR=="None":
                return c,None,None

            b= inv(X.T @ X) @ X.T @ c           #coeficientes del modelo
            y=X @ b                             #valores ajustados
            s=npy.sum(npy.square(y-c))          #suma del cuadrado del error
            return y,b,s



        #funcion auxiliar en la busqueda de coeficientes de levantamiento y arrastre
            #para el angulo de ataque calculado

        def buscador(vec,val):
            t=0
            while val>vec[t]:       #opt=1 Lupita's Version
                t=t+1               #opt=0 Mauricio's version
            if opt==1:
                if abs(vec[t]-val)>abs(vec[t-1]-val):
                    t=t-1
            return t

        #la funcion regresa los coeficientes de levantamiento y arrastre del perfil
        #usado en la posicion dada de longitud r, para el angulo de ataque calculado:alpf.

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
            if opt==1:
                cL=caracperfil[row,column+1]
                cD=caracperfil[row,column+2]
            if opt==0:                                       #opt=0 Mauricio's version
                    cL=caracperfil[row-1,column+1]+(alpha-caracperfil[row-1,column])*(caracperfil[row,column+1]-caracperfil[row-1,column+1])/(caracperfil[row,column]-caracperfil[row-1,column])
                    cD=caracperfil[row-1,column+2]+(alpha-caracperfil[row-1,column])*(caracperfil[row,column+2]-caracperfil[row-1,column+2])/(caracperfil[row,column]-caracperfil[row-1,column])

            return cL,cD

        # def isNaN(num):
        #     return num != num

        tic=timeit.default_timer()

        lamda=6 #relacion de velocidad de punta
        OffSet=0
        R=1.15 #radio propuesto
        B=3 #numero de palas
        N=int(convergencia[0]) #numero de divisiones de la pala 1,2,3,4,...18
        
        #N_Perf es un vector que contiene los perfiles perfiles que sea usaran. Ejemplo [9 0 10 2], [1,7,1,1]

       #idxVal, Lista que contiene los indices del vector valor para los perfiles seleccionados
        #considerando que siempre se guarda el primer perfil
        idxVal=[None]
        N_perf=0

        for i in range(4):
            if N_Perf[i]>0:
                idxVal.append(i)
                N_perf=N_perf+1
        
        del idxVal[0]                

        ##el vector u define la ubicacion [r/R] de los puntos donde hay cambio de perfil
        eps=npy.ones(N_perf)
        #eps=eps+0.15
        j=0
        for i in range(N_perf-1):
                eps[i]=valores[i+4]

        idxBorr=[None]
        for i in range(0,len(eps)-1):
            for j in range(i,len(eps)-1):
                if eps[i]>eps[j+1]:
                    idxBorr.append(j+1)

        del(idxBorr[0])
        u=npy.delete(eps,idxBorr)
        for t in range(len(idxBorr)):
            idxBorr[t]=idxBorr[t]+1

        idxVal=npy.delete(npy.asarray(idxVal),idxBorr)
        N_perf=len(idxVal)


        

        section_len=R/N #tamano de las secciones
        mid_section=section_len/2     #centro de las secciones
        r=npy.arange(mid_section,R,section_len) #Posiciones centrales de cada seccion de longitud
        perf=npy.ones(N)

        j=0
        for i in range(N):        #El vector Perf contiene el numero de perfil para cada sección                 
            if (r[i]/R)<=(u[j]):          #según  la distrubición dada por el vector U
                perf[i]=j
            else:
                j=j+1
                perf[i]=j

        #se leen los coeficientes de levantamiento y arrastre para un amplio rango
        # de angulos, de los perfiles elegidos
        #primera columna angulo, segunda columna Cl, tercera Cd
        #se conjunta todo en una sola matriz llamada caracperfil
        #tic1=timeit.default_timer()

        t=[[0,0]]
        len_t=[0]
        PerfUsados=[["Pefil :","Nada"]]
  
        for i in range(N_perf):
                t.append(npy.genfromtxt(cadenaStr[idxVal[i]],delimiter=','))
                PerfUsados.append(["Perf="+str(i),cadenaStr[idxVal[i]]])
                len_t.append(len(t[-1]))
        
        del(PerfUsados[0])
        caracperfil=npy.zeros((max(len_t),N_perf*3))

        for i in range(N_perf):
                caracperfil[0:len_t[i+1],i*3:(i+1)*3]=npy.asarray(t[i+1])
     
        #caracteristicas de los perfiles elegidos
        Cld=npy.zeros(N_perf)
        Cdd=npy.zeros(N_perf)

        #asigna los valores de Cl y Cd según el angulo de ataque del perfil elegido 
        #Valores contiene dicho angulos de ataque
        for i in range(N_perf):
            Cld[i],Cdd[i]=Coeficientes(valores[idxVal[i]],i,"Init")


        #forma de la pala para un rotor optimo
        j=0
        
        lamda_r=lamda*(r+OffSet)/(R+OffSet)
        lambda_r=lamda*(r)/(R)
        CL=npy.zeros(N)
        alpha=npy.zeros(N)
        theta_p=npy.zeros(N)
        c=npy.zeros(N)
            
        #phi=npy.divide(2*npy.arctan(1/lamda_r),3)
        phi=(2/3)*npy.arctan(1/lambda_r)

        for j in range(N):
            # pos=int()
            CL[j]=Cld[int(perf[j])]
            alpha[j]=valores[int(idxVal[int(perf[j])])]


        c=(8*npy.pi*(r)/(R))*npy.divide((1-npy.cos(phi)),(B*CL))
        theta_p=phi-(alpha*npy.pi/180)

        j=0
        k=0

        #buscando el punto maximo de la cuerda para el suavizado
        while c[k]<c[k+1]:
            k=k+1
        
        
        indi=0#con este indicador consideramos solamente las secciones que no estan dentro del cubo


        #suavizando los valores de la cuerda y theta con una regresion lineal multiple tipo
        #   b(1)+b(2)*r^2+b(3)/r ---> 'quadraticLupita'
        #   b(1) + b(2)/x + b(3)/x^2 + b(4)/x^3  --->'cubic'
        #   b(1) + b(2)*x +b(3)x^2 + ... + b(10)*x^9  --->'poly'
        if linRegModel =='None':
            s=None
            #s2=0
            b=None
            # while r[indi]<OffSet:
            #     indi=indi+1
        if linRegModel =='quadraticLupita':
            c[k:N],b,s=linRegression( c[k:N] , r[k:N],'quadraticLupita' )
            theta_p[k:N], _ ,s2=linRegression( theta_p[k:N] , r[k:N],'quadraticLupita' )
            while r[indi]<0.075:
                indi=indi+1
        # if linRegModel == 'cubic':
        #     c[0:k],b,s=linRegression( c[0:k] , r[0:k],'cubic' )
        #     c[k:N],b,_s=linRegression(c[k:N],r[k:N],'cubic')
        #     # theta_p, _ ,s2=linRegression( theta_p , r,'cubic' )
        # if linRegModel == 'poly':
        #     c,b,s=linRegression( c , r,'poly' )
            # theta_p[k:N], _ ,s2=linRegression( theta_p[k:N] , r[k:N],'quadraticLupita' )
        # if s2>2e-2:
        #     theta_p[k:N], _ ,s2=linRegression( theta_p[k:N] , r[k:N],'cubic' )
        # elif s2<2e-2:
        #     theta_p=_valuesTheta


        #calculo de coeficiente de potencia

        #inicializacion de los valores de angulo de viento relativo, a y a prima para el proceso iterativo
        # con las ecuaciones para pala optima

        i=slice(indi,N)

        sigmap=npy.divide(B*c[i],(2*npy.pi*(r[i]/R)))
        a=1/(1+npy.divide((4*npy.square(npy.sin(phi[i]))),(sigmap*CL[i]*npy.cos(phi[i]))))
        ap=(1-3*a)/(4*a-1)

        j=0
        i=0
        cp=0
        torque=0
        thrust=0
        power=0
        ##//proceso iterativo para el calculo del coeficiente de potencia de la geometria
        ##// modificada (una vez suavizadas las curvas)

        phij=npy.zeros(N-indi)
        F=npy.zeros(N-indi)
        alpp=npy.zeros(N-indi)
        Cl=npy.zeros(N-indi)
        Cd=npy.zeros(N-indi)
        CT=npy.zeros(N-indi)
        error=[[1,1,0]]
        counter=[None]
        counta=0
        for i in range(indi,N,1):
            t=1
            t2=1
            iterr=0
        
            while (t>convergencia[2] or t2>convergencia[2]) and iterr<convergencia[1]:
                
                phij[j]=math.atan((1-a[j])/((1+ap[j])*lamda_r[i]))
                
                try:
                    # F[j]=(2/math.pi)*math.acos(math.exp(-((B/2)*(1-((r[i]-OffSet)/(R-OffSet)))/(((r[i]-OffSet)/(R-OffSet))*math.sin(phij[j])))))
                    F[j]=(2/math.pi)*math.acos(math.exp(-((B/2)*(1-(r[i]/R)))/((r[i]/R)*math.sin(phij[j]))))
                
                except:
                    F[j]=1/(2*((j+1)/(N-indi)))
                
                alpp[j]=(phij[j]-theta_p[i])*180/math.pi
                Cl[j],Cd[j]=Coeficientes(alpp[j],i,"Calc")
                CT[j]=(sigmap[j])*(math.pow(1-a[j],2))*(Cl[j]*math.cos(phij[j])+Cd[j]*math.sin(phij[j]))/(math.pow(math.sin(phij[j]),2))
                apn=1/((4*F[j]*math.cos(phij[j])/(sigmap[j]*Cl[j]))-1)


                if CT[j]<0.96:
                    an=1/(1+4*F[j]*(math.pow(math.sin(phij[j]),2))/(sigmap[j]*Cl[j]*math.cos(phij[j])))
                else:
                    an=(1/F[j])*(0.143+math.sqrt(0.0203-0.6427*(0.889-CT[j])))

                t=abs((a[j]-an)/an)
                t2=abs((ap[j]-apn)/apn)
                # a[j]=an
                # ap[j]=apn
                if an<1: 
                    a[j]=an
                    ap[j]=apn
                    
                else:
                    a[j]=an
                    ap[j]=apn
                    counter.append(j)
                    break
                iterr=iterr+1
            
            error.append([t,t2,iterr])
            try:
                if(i<(N)):
                    cp+=(8/lamda**2)*F[j]*(math.pow(math.sin(phij[j]),2))*(math.cos(phij[j])-lamda_r[i]*math.sin(phij[j]))*(math.sin(phij[j])+lamda_r[i]*math.cos(phij[j]))*(1-(Cd[j]/Cl[j])*(1/math.tan(phij[j])))*math.pow(lamda_r[i],2)
                    torque+=2*F[j]*ap[j]*(1-a[j])*1.225*6*(lamda*6/R)*(r[j]**2)*2*math.pi*r[j]*section_len
                    thrust+=2*F[j]*1.225*6**2*a[j]*(1-a[j])*math.pi*2*r[j]*section_len
                    counta+=1
            except:
                print("Elemento "+str(j)+ "Fallido")
            j=j+1

        cp=cp*lamda/j# multiplicando por el diferencial de la integral (lamda-lamda_h)/No_Iter -->lamda_h=0
        power+=torque*(lamda*6/R)
        p=0.5*cp*1.225*R**2*(6**3)*math.pi
        phi[indi:N]=phij
        phi=phi*180/npy.pi

        if linRegModel == 'cubic':
            c[0:k],b,s=linRegression( c[0:k] , r[0:k],'cubic' )
            c[k:N],b,_s=linRegression(c[k:N],r[k:N],'cubic')
            theta_p, _ ,s2=linRegression( theta_p , r,'cubic' )
        if linRegModel == 'poly':
            c,b,s=linRegression( c , r,'poly' )
            theta_p[k:N], _ ,s2=linRegression( theta_p[k:N] , r[k:N],'quadraticLupita' )
            if s2>2e-2:
                theta_p[k:N], _ ,s2=linRegression( theta_p[k:N] , r[k:N],'cubic' )
        toc=timeit.default_timer()
        tiempo_ejec=toc-tic
        print("Potencia calculada. Elementwise [W]:",power)
        print("Torque calculado. Elementwise [Nm]:",torque)
        print("Empuje calculado. Elementwise [N]:",thrust)
        print("---------")
        print("Coeficiente de potencia calculado:",cp)
        print("Potencia calculada del Cp [W]:",p)
        print("---------")
        print('tiempo de ejecucion:',tiempo_ejec, 'segundos')
        # print("RMS Ajuste Cuerda: "+str(s))
        # print("RMS Ajuste Phi: "+str(s2))
        # print("RMS Ajuste Theta: "+str(s3))
        print(counter)
        print('------')
        return {'cp':cp,'PosCambio':u,'AlphIni':valores[idxVal],'Potencia':p,'c':c,'phig':phi,'l':r,'theta_p': theta_p*180/npy.pi,'alp_p':alpp,'perfUsados':PerfUsados,'perf':perf,'Coefs_b':b,'IndAxial':a,'IndAng':ap,'error':error}

        