import numpy as npy
import timeit
from tkinter import *
import os

# root = Tk()
# termf = Frame(root, height=400, width=500)

# termf.pack(fill=BOTH, expand=YES)
# wid = termf.winfo_id()
# os.system('xterm -into %d -geometry 40x20 -sb &' % wid)

# root.mainloop()
# #def fitness(P)
# def SortVal(Array1):
#     indx=npy.argsort(Array1)[::-1]
#     Array1=sorted(Array1,reverse=True)
#     return Array1,indx


# Population={}
# Chromosome=[[1.2,2.2,12.2,12.3,12.1,12.6,3.7,3.2,1.1]]
# Population['Chromo']=Chromosome
# #Population['Chromo'].append([1.2,2.2,12.2,12.3,12.1,12.6,3.7,3.2,1.1])
# #Population['Chromo'][1]=[1.2,2.2,12.2,12.3,12.1,12.6,3.7,3.2,52.1]
# #print ("Population")

# Population2=Population

# Lista=[]
# Lista=Population['Chromo']
# #for tupl in Population2['Chromo']:
#     #print (tupl)

# #print(len(Population['Chromo'][0]))
# suma=sum(npy.asarray(Lista))
# normalized_fitness = npy.asarray(Lista)/suma


# # code snippet to be executed only once 
# mysetup = "import numpy as npy"
  
# # code snippet whose execution time is to be measured 
# mycode = ''' 
# a=npy.ones(5)
# b=a.reshape(5,1)
# '''
  
# # timeit statement 
# print (timeit.timeit(setup = mysetup, 
#                     stmt = mycode, 
#                     number = 100000) )

# sorted_norm_fitness,indx =SortVal(Population['Chromo'])

# print("---------------")
# print(Population['Chromo'][0])
# print(normalized_fitness)
# print(sorted_norm_fitness)
# print(indx)
# A=npy.zeros((5,1))
# print(A[1])
# M=5
# N=10
# Lista=[npy.zeros(M)]*N
# print(Lista)
# print('-----------')
# v=npy.array([-1.45,-5.1,-5,-10.3])
# a=sorted(v)
# print(a)
# s=npy.argsort(v)
# print(s)
# f = open('file.txt','w')
# a = input('is python good?')
# f.write('answer:'+str(a))
# f.close()
from gekko import GEKKO
import numpy as np
import matplotlib.pyplot as plt  

# measurements
xm = np.array([0,1,2,3,4,5])
ym = np.array([0.1,0.2,0.3,0.5,0.8,2.0])

# GEKKO model
m = GEKKO()

# parameters
x = m.Param(value=xm)
a = m.FV()
a.STATUS=1

# variables
y = m.CV(value=ym)
y.FSTATUS=1

# regression equation
m.Equation(y==0.1*m.exp(a*x))

# regression mode
m.options.IMODE = 2

# optimize
m.solve(disp=False)

# print parameters
print('Optimized, a = ' + str(a.value[0]))

plt.plot(xm,ym,'bo')
plt.plot(xm,y.value,'r-')
plt.show()