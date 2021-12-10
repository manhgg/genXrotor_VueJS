# !/usr/bin/python3
# -*- coding: utf-8 -*-

from Classes_Lib import Population
import timeit


tic=timeit.default_timer()

limit={'upper':[1,0,0,0,4,6,6,6,0.2,0.12,0.1],'lower':[7,13,13,13,10,12,12,12,0.33,1,1]}
tol=(0,0,0,0,2,2,2,2,3,3,3)
#1,0,0,0,4,6,6,6,0.2,0.12,0.1
#7,13,13,13,10,12,12,12,0.33,1,1
obj=Population(11,50,limit,tol)

poblacion=obj.generateRandPop()

toc=timeit.default_timer()
print(*poblacion['Chromo'],sep='\n')
print(toc-tic)

