'''
Created on 21 de mai de 2018

Objetivo: Provar a solução do problema de Monty Hall utilizando Monte Carlo

@author: João Paulo Clarindo
'''
from random import randint
n = 3                                       # numero de portas
success = 0                                 # quantidade de vezes que o jogador acertou
trials = 100000                                 # número de tentativas

#Caso o jogador não troque a porta

for i in range (1, trials):
    correct_door = randint(1,n)
    player_door = randint(1,n)
    
    if (correct_door == player_door):      # Caso o a porta do jogador seja a correta
        success += 1                       # houve sucesso 
        
print("Sem troca\nNúmero de tentativas:{}\nNúmero de acertos:{}\nPorcentagem:{}\n".format(trials,success,success/trials))

#Caso o jogador troque a porta

success = 0                                 # quantidade de vezes que o jogador acertou

for i in range (1,trials):
    correct_door = randint(1,n)
    player_door = randint(1,n)
    
    '''
    A porta que o apresentador abrirá (empty_door) não pode ser nem a porta que
    o jogador escolheu e nem a porta que está o prêmio. Um número aleatório que
    não represente as portas para escolha é gerado.
    '''
    empty_door = player_door
    
    while((empty_door == player_door) or (empty_door == correct_door)):
        empty_door = randint(1,n)
    
    