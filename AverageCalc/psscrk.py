import random
import math
from itertools import permutations

def pswcrk():
    lower = [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z]
    upper = [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z]
    number = ['0','1','2','3','4','5','6','7','8','9']
    password = []
    i = 0
    
    perm = permutations((lower, upper, number), 127)

    for i in range(126):
        psschar = random.randrange(1,3,1)
        if psschar == 1:
            #lower
            char = random.randrange(0,(len(lower)-1),1)
            password.append(char)
        elif psschar == 2:
            #upper
            char = random.randrange(0,(len(upper)-1),1)
            password.append(char)
        elif psschar == 3:
            #number
            num = random.randrange(0,(len(number)-1),1)
            password.append(num)
pswcrk()