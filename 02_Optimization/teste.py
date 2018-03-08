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
    curr_gain_dict = createDict(max_angle, max_gain)

    try:
        last_gain_dict = json.load(open(filename))
        print('File found!')
        if last_gain_dict.get('max_gain') < curr_gain_dict.get('max_gain'):
            print('Saving new gain and angles')
            json.dump(curr_gain_dict, open(filename, 'w'))

    except:
        print('File not found! Creating new one.')
        json.dump(curr_gain_dict, open(filename, 'w'))


def createDict(max_angle, max_gain):
    return {'phi1':int(max_angle[0]),'theta1':int(max_angle[1]),'phi2':int(max_angle[2]),'theta2':int(max_angle[3]),'phi3':int(max_angle[4]),'theta3':int(max_angle[5]), 'max_gain':float(max_gain)}

def main():
    thresh_interval_array = [360, 180, 120, 80, 50, 45, 30, 20, 15, 8, 4, 2]
    angles = np.random.randint(thresh_interval_array[0], size=6)
    max_gain = 0
    prev_gain = 0
    new_angles = np.array([])
    max_angle = np.zeros((6,), dtype=np.int)
    curr_gain = step(angles)
    print('Acc for {} w/o thresh: {}'.format(angles, curr_gain))
    thresh = [0, 0, 0, 0, 0, 0]

    for thresh_interval in thresh_interval_array:
        for i in range(1500):
            thresh = np.random.randint(thresh_interval, size=6) - int(thresh_interval / 2)
            thresh = thresh.astype(int)

            new_angles = angles + thresh
            for i in range(6):
                new_angles[i] = new_angles[i] % 360

            prev_gain = curr_gain
            curr_gain = step(new_angles)

            if curr_gain > max_gain:
                max_gain = curr_gain
                max_angle = new_angles

        print('\nMax prec from [{}, {}, {}, {}, {}, {}] with {}'.format(max_angle[0], max_angle[1], max_angle[2],max_angle[3],max_angle[4],max_angle[5], max_gain))
        angles = max_angle

    saveMaxAngle(max_angle, max_gain)

if __name__ == '__main__':
    for i in range(5):
        main()
