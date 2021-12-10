import Clase_CGA_AllRandom as GA
import numpy as npy
import timeit

def Main_GA(ConfGA,Limites,Convergencia,Opt_Selec):
    tic=timeit.default_timer()

    #  Initialization
    Limits={}

    M = int(ConfGA[0]) #% number of chromosomes (cadinate solutions)
    N = len(Limites['UB']) #  % number of genes (variables) [alp1,alp2,alp3,alp4,U1,U2,U3]
    MaxGen = int(ConfGA[1])
    Pc = ConfGA[2]#Probabilit
    Pm = ConfGA[3]
    Er = ConfGA[4]

    #Limits=Limites

    Population  = GA.GeneratePopulation(M,N,Limites)
    Airfoils_mat= GA.Load_Airfoils()

    Population['Fitness']=[GA.Fitness_Func(Population['Chromo'][0],Airfoils_mat,Convergencia)]
    for i in range(1,M):
        Population['Fitness'].append(GA.Fitness_Func(Population['Chromo'][i],Airfoils_mat,Convergencia))

    Old_FitSum=0
    error=[]    
    # Main loop

    #If an odd number or chromosomes is conforming the Pop, then the last iteraration selects only 1 child
    if (M%2) > 0:
        Odd_pop=True
    else:
        Odd_pop=False

    for g in range(MaxGen):

        NewPopulation={}
        NewPopulation['Chromo']=[[None]*N]
        NewPopulation['Fitness']=[None]
        for k in range(0,M,2):
            #% Selection
            if Opt_Selec==0: #Tournament
                Parents = GA.Selection_Tourn(Population,2)
            elif Opt_Selec==1: #Roulette Wheel
                Parents = GA.Selection_RW(Population)
            
            #% Crossover
            Childs=GA.Crossover(Parents,Pc,Limites)
        
            #% Mutation
            Childs['Chromo'][0] = GA.Mutation(Childs['Chromo'][0],Limites,Pm)
            Childs['Chromo'][1] = GA.Mutation(Childs['Chromo'][1],Limites,Pm)
            if(not Odd_pop):
                NewPopulation['Chromo'].append(Childs['Chromo'][0])
                NewPopulation['Chromo'].append(Childs['Chromo'][1])

            if (Odd_pop):
                NewPopulation['Chromo'].append(Childs['Chromo'][0])
                if k<(M-1):
                    NewPopulation['Chromo'].append(Childs['Chromo'][1])
        del NewPopulation['Chromo'][0]
        del NewPopulation['Fitness'][0]

        #Recalculation of Fitness value on new population to perfom elitism
        for i in range (M):
            NewPopulation['Fitness'].append(GA.Fitness_Func(NewPopulation['Chromo'][i],Airfoils_mat,Convergencia))

        #% Elitism
        NewPopulation = GA.Elitism(Population,NewPopulation,Er)
        
        Population= NewPopulation
        print("Generation - ",str(g+1))
        
        FitSum=npy.sum(Population['Fitness'])
        error.append(abs(Old_FitSum-FitSum))
        Old_FitSum=FitSum
        if error[g]<Convergencia[1]:
            break
        if((g+1)%20)==0:
            indx = GA.SortVal(Population['Fitness'], True)[1]
            BestChrom={}
            BestChrom['Chromo']  = Population['Chromo'][indx[0]] 
            BestChrom['Fitness'] = Population['Fitness'][indx[0]]
            print(BestChrom)

        
    indx = GA.SortVal(Population['Fitness'], True)[1]
    BestChrom={}
    BestChrom['Chromo']  = Population['Chromo'][indx[0]] 
    BestChrom['Fitness'] = Population['Fitness'][indx[0]] 

    
    idxVal=[None]
    idxBorr=[None]
    N_perf=0

    tempPerf=BestChrom['Chromo'][0:4]
    tempPos=BestChrom['Chromo'][8:11]
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

    temp=[0]*N
    
    for i in range(N_perf):
        temp[i]=BestChrom['Chromo'][idxVal[i]]
        temp[i+4]=BestChrom['Chromo'][idxVal[i]+4]

    for i in range(N_perf-1):
        temp[i+8]=BestChrom['Chromo'][i+8]

    BestChrom['Chromo']=temp

    print(BestChrom)
    toc=timeit.default_timer()
    tiempo_ejec=toc-tic
    print("Ejecutado en ", tiempo_ejec," s")
    print("Con",str(tiempo_ejec/(g+1))," s por generacion")
    return BestChrom, error, {'TiempoEjec':tiempo_ejec,'Generaciones':g+1,'Individuos':ConfGA[0],'ProbCruce':ConfGA[2],'ProbMutacion':ConfGA[3],'Elite':ConfGA[4]}
