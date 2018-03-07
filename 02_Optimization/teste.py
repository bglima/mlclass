'''
Created on 6 de mar de 2018

@authors: Bruno Lima
          João Paulo
          Nilson Sales
'''

import numpy as np
import requests
import os
import msvcrt
import json

def step(angles):
    url = 'http://localhost:8080/antenna/simulate?phi1={}&theta1={}&phi2={}&theta2={}&phi3={}&theta3={}'.format(angles[0],angles[1],angles[2],angles[3],angles[4],angles[5])
    try:
        s = requests.post(url)
    except:
        print('erro na requisição')
    else:
        return float(s.content.decode('utf-8').split('\n')[0])
    
def saveMaxAngle(max_angle, max_prec):      
    dirname = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(dirname, 'max.json')
    
    d = createDict(max_angle, max_prec)
    if not (os.path.exists(filename)):
        print('aqui')
        json.dump(d,open(filename, 'w'))
    else:
        old_d = json.load(open(filename))
        if float(d.get('max_prec')) > float(old_d.get('max_prec')):
            json.dump(d,open(filename, 'w'))
            print('Máximo absoluto encontrado!')
        else:
            print('O tamanho máximo dessa rodada não é o máximo absoluto.\nMáximo absoluto: {}'.format(old_d.get('max_prec')))
    
    
def createDict(max_angle, max_prec):
    return {'phi1':int(max_angle[0]),'theta1':int(max_angle[1]),'phi2':int(max_angle[2]),'theta2':int(max_angle[3]),'phi3':int(max_angle[4]),'theta3':int(max_angle[5]), 'max_prec':float(max_prec)}
    
angles = np.array([90,90,90,90,90,90])



max_prec = 0
prev_prec = 0
max_angle = []
curr_prec = step(angles)
print('Acc for {} w/o thresh: {}'.format(angles, curr_prec))
thresh = [0, 0, 0, 0, 0, 0]

while(True):
    max_rand = 265
    
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
    thresh = thresh.astype(int)
    
    new_angles = np.array([])
    new_angles = angles + thresh
    new_angles = new_angles.astype(int)        
    
    np.place(new_angles, new_angles < 0, angles)
    np.place(new_angles, new_angles >= 360, angles)
    
    prev_prec = curr_prec
    curr_prec = step(new_angles)
    curr_loss = 1 - curr_prec
    
    if curr_prec > max_prec: 
        max_prec = curr_prec
        max_angle = new_angles
    
    print('Acc for {} is {}'.format(new_angles, curr_prec))
    
    if msvcrt.kbhit():
        if ord(msvcrt.getch()) != None:
            print(new_angles)
            print('\nMax prec from {} with {}'.format(max_angle, max_prec))
            saveMaxAngle(max_angle, max_prec)
            break
