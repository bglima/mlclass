'''
Created on 6 de mar de 2018

@authors: Bruno Lima
          João Paulo
          Nilson Sales
'''

import numpy as np
import requests
import time
import random
import os

def step(angles):
    url = 'http://localhost:8080/antenna/simulate?phi1={}&theta1={}&phi2={}&theta2={}&phi3={}&theta3={}'.format(angles[0],angles[1],
                                                                                                                angles[2],angles[3],
                                                                                                                angles[4],angles[5])
    try:
        s = requests.post(url)
    except:
        print('erro na requisição')
    else:
        return float(s.content.decode('utf-8').split('\n')[0])
    
def saveMaxAngle(max_angle, max_prec):
    dirname = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(dirname, 'max.txt')
    
    f = open(filename, 'w')
    f.write('Max prec from {} with {}. Result obtained on {}'.format(max_angle, max_prec,time.strftime("%H:%M:%S")))


#angles = [10,180,242,315,180,155]
angles = [90,90,90,90,90,90]

initial_angles = angles
prev_prec = 0
max_prec = 0
max_angle = []
curr_prec = step(angles)
print('Acc for {} w/o thresh: {}'.format(angles, curr_prec))
thresh = [0, 0, 0, 0, 0, 0]


try:
    while(True):
        in_range = True
         
        max_rand = 180
        
        # Try near combination of values if the precision is high
        # Risk of falling into a local minimum
        if curr_prec > 15:
            max_rand = 3
            
            # checks if the derivate is positive
            if (curr_prec - prev_prec) > 0.5:
                angles += thresh
            else:
                max_rand = 12
    
            
        thresh = (np.random.rand(6) * max_rand) - max_rand / 3
        #thresh = np.round(thresh, 2)
        
        new_angles = np.array([])
        new_angles = angles + thresh
        new_angles = new_angles.astype(int)
        
        prev_prec = curr_prec
        curr_prec = step(new_angles)
        curr_loss = 1 - curr_prec
        
        if curr_prec > max_prec: 
            max_prec = curr_prec
            max_angle = new_angles
        
        # Checks if angles are in range, if not, goes back to initial angles
        for angle in new_angles:
            if (angle < 0) or (angle >360):
                in_range = False
                angles = initial_angles            
        
        if in_range: 
            print('Acc for {} is {}'.format(new_angles, curr_prec))
        else:
            print('Out of range')
        
except:
    print('\nMax prec from {} with {}'.format(max_angle, max_prec))
    saveMaxAngle(max_angle, max_prec)
