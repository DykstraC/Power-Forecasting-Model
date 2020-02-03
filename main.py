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

os.system("%USERPROFILE%/OneDrive/PhysicsCalc/averageCalc.exe")

time.sleep(5)
v = open('validate.txt', 'w+')

valid = v.read()
t1 = time.time()

while valid != True:
    print('Waiting for response from backend')
    valid = v.read()
    t2 = time.time()
    if (t2-t1) > 10:
        print(t1, t2)
        break
        
    
if valid == True:
    v.write('False')
    v.close()
    valid = ''
    r = open('result.txt')
    
else:
    print('An error has occured\n The program failed to validate a response')
    
results = []    
with open('result.txt', 'r') as r:
    for line in r:
        results.append(line.strip())