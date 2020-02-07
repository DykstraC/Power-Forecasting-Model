# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 20:54:17 2019

@author: chris
"""
import os, sys, time


f = open('data.txt', 'w+')

points = []

number_of_points = int(input("Number of points to average: "))

points.append(str(number_of_points) +'\n')

points.append(input("Points to average: "))
points.append(',')

for i in range(number_of_points - 1):
    points.append(input("Points to average: "))
    points.append(',')
    
for j in range((number_of_points*2)):
    f.write(points[j])
    
f.close()

f = open('data.txt', 'r')
print(f.read())
f.close

os.system("%USERPROFILE%/Source/Repos/DykstraC/Power-Forecasting-Model/averageCalc.exe") 
#C:\Users\chris\Source\Repos\DykstraC\Power-Forecasting-Model

time.sleep(5)
v = open('validate.txt', 'w+t')
print(v.closed, '\n', v)

valid = v.read()
print(valid)
t1 = time.time()
print('Waiting for response from backend')

while valid != True:
    valid = v.read()
    t2 = time.time()
    if (t2-t1) > 10:
        print(t1, t2)
        broke = True
        break
if broke == True:
    v.close()
    v.closed
    
if valid == True:
    v.write('False')
    v.close()
    v.closed
    valid = ''
    r = open('result.txt')
    
else:
    print('An error has occured\nThe program failed to validate a response')
    
results = []    
with open('result.txt', 'r') as r:
    for line in r:
        results.append(line.strip())