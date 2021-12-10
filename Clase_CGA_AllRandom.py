import numpy as npy
import random as rand
import Fitness_CoefPotencia_AllRandom as cp

def GeneratePopulation(M,N,Limits):
    # M  = number of chromosomes in the population
    # N = Number of genes for each gene
    Chromo=[None]*N
    Population={}
    Population['Chromo']=[[None]*N]*M
    for i in range(M):      
        for j in range(N):
            if j==0:
                Chromo[j]=rand.randint(1,7)
            if j>=1 and j<4:
                Chromo[j]=rand.randint(0,13)
            if j>=4 :
                Chromo[j]=(Limits['UB'][j] - Limits['LB'][j]) * rand.random() + Limits['LB'][j]


            if Chromo[j]>Limits['UB'][j]:
                Chromo[j]=Limits['UB'][j]
            elif Chromo[j]<Limits['LB'][j]:
                    Chromo[j]=Limits['LB'][j]

        Population['Chromo'][i]=[t for t in Chromo]
    
    #del Population['Chromo'][0]
    return Population

def Load_Airfoils():
    #se leen los coeficientes de levantamiento y arrastre para un amplio rango
    # de angulos, de los perfiles elegidos
    #primera columna angulo, segunda columna Cl, tercera Cd

    #S835
    pp1=npy.genfromtxt('Perfiles/s835.csv',delimiter=',')
    #SG6040
    pp2=npy.genfromtxt('Perfiles/sg6040.csv',delimiter=',')
    #S826
    pp3=npy.genfromtxt('Perfiles/s826.csv',delimiter=',')
    #SG6043
    pp4=npy.genfromtxt('Perfiles/sg6043.csv',delimiter=',')

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

    return caracperfil

def SortVal(Obj,descend):
    if(descend): 
        indx=npy.argsort(Obj,axis=None)[::-1]     
    else:
        indx=npy.argsort(Obj,axis=None)
    Obj=sorted(Obj,reverse=descend) 
    return Obj,indx                          

def Selection_RW(Population):

    M = len(Population['Chromo'])  #Number of Candidate Solution (Chromosomes) 
    TempPop={}
    #TempArray=[]
    #TempArray=Population['Fitness']
    #normalized_fitness = npy.asarray(TempArray)/sum(npy.asarray(TempArray))
    normalized_fitness = npy.asarray(Population['Fitness'])/sum(npy.asarray(Population['Fitness']))
    sorted_norm_fit_val , sorted_idx = SortVal(normalized_fitness , True) 

    TempPop['Chromo']=[Population['Chromo'][sorted_idx[0]]]
    TempPop['Fitness']=[Population['Fitness'][sorted_idx[0]]]

    for i in range(1,M):
        TempPop['Chromo'].append(Population['Chromo'][sorted_idx[i]] )
        TempPop['Fitness'].append(Population['Fitness'][sorted_idx[i]] )
#        TempPop['NormFit'][i] = normalized_fitness[sorted_idx[i]] 

    #cumsum = npy.zeros(M) 
    cumsum = npy.cumsum(sorted_norm_fit_val[::-1])[::-1] #TempPop['NormFit']

    # for i in range(M):
    #     for j in range(i,M)
    #         cumsum[i] = cumsum[i] + TempPop['NormFit'][j]

    R = rand.random()  # in [0,1] interval
    parent1_idx = M-1 

    for i in range(1,M):
        if R > cumsum[i]:
            parent1_idx = i-1
            break 

    parent2_idx = parent1_idx 
    stop_w = 0  # to break the while loop in rare cases where we keep getting the same index
    while (parent2_idx == parent1_idx):
        stop_w = stop_w + 1 
        R = rand.random()  # in [0,1]
        if stop_w > 20:
            break 

        for i in range(1,M):
            if R > cumsum[i]:
                parent2_idx = i-1
                break 

    Parents={}
    Parents['Chromo']=[TempPop['Chromo'][parent1_idx]]
    Parents['Chromo'].append(TempPop['Chromo'][parent2_idx])
    return Parents

def Selection_Tourn(Population, k):
    M = len(Population['Chromo'])
    bestIdx1 = None

    for i in range(k):
        randIdx=rand.randint(0, M-1)
        if (bestIdx1 == None) or Population['Fitness'][randIdx] > Population['Fitness'][bestIdx1]:
            bestIdx1 = randIdx
    
    bestIdx2=bestIdx1
    
    while(bestIdx2==bestIdx1):
        bestIdx2 = None
        for i in range(k):
            randIdx=rand.randint(0,M-1)
            if (bestIdx2 == None) or Population['Fitness'][randIdx] > Population['Fitness'][bestIdx2]:
                bestIdx2 = randIdx
    
    Parents={}
    Parents['Chromo']=[Population['Chromo'][bestIdx1]]
    Parents['Chromo'].append(Population['Chromo'][bestIdx2])
    return Parents 

def Crossover(Parents,Pc,Limits): #Limits parameter optional

    N=len(Parents['Chromo'][0])
    Childs={}

    child1 = npy.zeros(N) 
    child2 = npy.zeros(N)


    Cross_P = rand.randint(0,2)

    child1[0:Cross_P+1] = Parents['Chromo'][0][0:Cross_P+1] 
    child1[Cross_P+1:4] = Parents['Chromo'][1][Cross_P+1:4]
    
    child2[0:Cross_P+1] = Parents['Chromo'][1][0:Cross_P+1] 
    child2[Cross_P+1:4] = Parents['Chromo'][0][Cross_P+1:4]

    for k in range(4,N):
        beta = rand.random()  #[0,1]
        child1[k] = beta * Parents['Chromo'][0][k] + (1-beta) * Parents['Chromo'][1][k]   
        child2[k] = (1-beta) * Parents['Chromo'][0][k]  + beta * Parents['Chromo'][1][k]  
        
#Compare the values of each child gene to bound inside the limit (Optional)
        if child1[k] > Limits['UB'][k]:
            child1[k]  =  Limits['UB'][k] 
    
        if child1[k] < Limits['LB'][k]:
            child1[k] = Limits['LB'][k]
        
        if child2[k] > Limits['UB'][k]: 
            child2[k]  =  Limits['UB'][k] 
        
        if child2[k] < Limits['LB'][k]:
            child2[k] = Limits['LB'][k] 

    R1 = rand.random() #[0,1]

    if R1 <= Pc:
        child1 = child1.tolist()
    else:
        child1 = Parents['Chromo'][0] 


    R2 = rand.random() #[0,1]

    if R2 <= Pc:
        child2 = child2.tolist()
    else:
        child2 = Parents['Chromo'][1] 
    
    Childs['Chromo']=[child1]
    Childs['Chromo'].append(child2)

    return Childs



def Mutation(Genes,Limits,Pm):

    N = len(Genes)

    for k in range(N):
        R = rand.random()
        if k>=0 and k <4:
            if R < Pm:
                Genes[k]=rand.randint(0,13)
        if k>=4 :#and k <=8:
            if R < Pm:
                Genes[k] = (Limits['UB'][k] - Limits['LB'][k] ) * rand.random() + Limits['UB'][k]

    #Compare the values of each child gene to bound inside the limit (Optional)
        if Genes[k] > Limits['UB'][k]:
            Genes[k]  =  Limits['UB'][k] 
        
        if Genes[k] < Limits['LB'][k]:
            Genes[k] = Limits['LB'][k]
        
    return Genes

def Elitism(Population,NewPopulation,Er):

    M = len(Population['Chromo'])
    Elite_no = int(round((M * Er)))

    indx = SortVal( Population['Fitness']  , True)[1]      
    indx2 = SortVal(NewPopulation['Fitness'] , False)[1]     

    NewPopulation2=NewPopulation

    for k in range(Elite_no):
        if Population['Fitness'][indx[k]]>NewPopulation2['Fitness'][indx2[k]]:
            NewPopulation2['Chromo'][indx2[k]]=Population['Chromo'][indx[k]]    
            NewPopulation2['Fitness'][indx2[k]] =Population['Fitness'][indx[k]]

    return NewPopulation2

def Fitness_Func(Chromo,Airfoils_mat,Convergencia): 

    return cp.Coef_Potencia.Calculo(Chromo,Convergencia)
