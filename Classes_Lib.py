# !/usr/bin/python3
# -*- coding: utf-8 -*-

#from Class_Individuo import Individual

import random as rand
from Fitness_Function import Fitness_Function


class Individual:

    def __init__(self,numGene,limit,tol):
        
        self.fitFun=Fitness_Function()
        self.gNum=numGene
        self.gLimit=limit
        self.gTol=tol
    
    def generate(self):
        
        self.chromo=[round(rand.uniform(self.gLimit["lower"][i],self.gLimit["upper"][i]),self.gTol[i]) for i in range(self.gNum)]
        self.fitVal=self.fitFun.calculate(self.chromo)
        return [self.chromo],self.fitVal

class Population:

    def __init__(self,numGene,numChromo,limit,tol):

        self.indiv_Obj=Individual(numGene,limit,tol)
        self.nChro=numChromo
        self.population={}
        self.population['Chromo']=[[None]*numGene]*numChromo
        self.population['Fit_Val']=[None]*numChromo


    def generateRandPop(self):

        for i in range(self.nChro):
            self.population['Chromo'][i],self.population['Fit_Val'][i]=self.indiv_Obj.generate()

        
        return self.population

        
