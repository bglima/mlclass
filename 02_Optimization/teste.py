'''
Created on 6 de mar de 2018

@authors: Bruno Lima
          João Paulo
          Nilson Sales
'''

import numpy as np
import requests
import os
import json
from time import sleep

def step(angles):
    url = 'http://localhost:8080/antenna/simulate?phi1={}&theta1={}&phi2={}&theta2={}&phi3={}&theta3={}'.format(angles[0],angles[1],angles[2],angles[3],angles[4],angles[5])
    try:
        s = requests.post(url)
    except:
        print('erro na requisição')
    else:
        return float(s.content.decode('utf-8').split('\n')[0])

def saveMaxAngle(max_angle, max_gain):
    dirname = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(dirname, 'max.json')


    d = createDict(max_angle, max_gain)

    if not (os.path.exists(filename)):
        print('Diretório nao existente!')
        json.dump(d, open(filename, 'w'))
    else:
        old_d = json.load(open(filename))
        if old_d.get('max_gain') and (float(d.get('max_gain')) >= float(old_d.get('max_gain'))):
            json.dump(d, open(filename, 'w'))
            print('Máximo absoluto encontrado!')
        else:
            print('O tamanho máximo dessa rodada não é o máximo absoluto.\nMáximo absoluto: {}'.format(old_d.get('max_gain')))


def createDict(max_angle, max_gain):
    return {'phi1':int(max_angle[0]),'theta1':int(max_angle[1]),'phi2':int(max_angle[2]),'theta2':int(max_angle[3]),'phi3':int(max_angle[4]),'theta3':int(max_angle[5]), 'max_gain':float(max_gain)}

thresh_interval_array = [360, 180, 120, 80, 50, 45, 30, 20, 15, 8, 4, 2]
angles = np.random.randint(thresh_interval_array[0], size=6)
max_gain = 0
prev_gain = 0
new_angles = np.array([])
max_angle = np.zeros((6,), dtype=np.int) #np.array([])
curr_gain = step(angles)
print('Acc for {} w/o thresh: {}'.format(angles, curr_gain))
thresh = [0, 0, 0, 0, 0, 0]

""" Things TO DO:
    - Get best trial of N and show to user
    - Define when to reduce thresh_interval (e.g. whenever precision goes further required value; do N trials)
    - Find a way of not getting stuck into a local minimum
    - Do it in parallel with K local minimun
"""

# Max prec from [223 159 347  88 173 212] with 25.83223665952505
# Max prec from [228 159 344  87 181 208] with 28.1164302338536
# Max prec from [234 162 344  85 181 205] with 28.997204205603033
# Max prec from [225, 167, 347, 79, 181, 203] with 29.48429448699448
# Max prec from [229, 170, 347, 75, 180, 205] with 30.100344823569362
# Max prec from [230, 170, 348, 73, 181, 205] with 30.24811445417071
# Max prec from [230, 170, 348, 71, 180, 205] with 30.352217673641405
# Max prec from [231, 171, 349, 71, 180, 205] with 30.43005389127427
# Max prec from [231, 171, 349, 70, 180, 205] with 30.470835576196286

for thresh_interval in thresh_interval_array:

    for i in range(1000):
        # Try near combination of values if the precision is high
        # Risk of falling into a local minimum
        thresh = np.random.randint(thresh_interval, size=6) - int(thresh_interval / 2)
        thresh = thresh.astype(int)

        # Add thresh to previous angles
        new_angles = angles + thresh
        #print('New angles are: ', new_angles)
        for i in range(6):
            new_angles[i] = new_angles[i] % 360


        prev_gain = curr_gain
        curr_gain = step(new_angles)

        if curr_gain > max_gain:
            max_gain = curr_gain
            max_angle = new_angles

        #print('Acc for {} is {}'.format(new_angles, curr_gain))
        #print(new_angles)

    print('\nMax prec from [{}, {}, {}, {}, {}, {}] with {}'.format(max_angle[0], max_angle[1], max_angle[2],max_angle[3],max_angle[4],max_angle[5], max_gain))
    angles = max_angle

saveMaxAngle(max_angle, max_gain)