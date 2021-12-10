import random as rand
from Fitness_Function import Fitness_Function


class Individual(object):

    def __init__(self,numGene,limit,tol):
        
        self.fitFun=Fitness_Function()
        self.gNum=numGene
        self.gLimit=limit
        self.gTol=tol
    
    def generate(self):
        
        self.chromo=[round(rand.uniform(self.gLimit["lower"][i],self.gLimit["upper"][i]),self.gTol[i]) for i in range(self.gNum)]
        self.fitVal=self.fitFun.calculate(self.chromo)
        return [self.chromo],self.fitVal




