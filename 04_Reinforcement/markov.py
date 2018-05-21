'''
Created on 21 de mai de 2018

Objetivo: Provar a solução do problema de Monty Hall utilizando aprendizagem por reforço

@author: Nilson Sales
'''

import random as rand


def do_not_change(n_doors, trials):  # Caso o jogador não troque a porta
    rating = 0
    success = 0

    for i in range(1, trials):
        correct_door = rand.randint(1, n_doors)
        player_door = rand.randint(1, n_doors)

        if (correct_door == player_door):  # Caso o a porta do jogador seja a correta
            rating += 2  # houve sucesso
            success += 1
        else:
            rating -= 1

    print("Sem troca\nNúmero de tentativas:{}\nNota:{}\nPorcentagem:{}\n".format(trials, rating,
                                                                                              success / trials))


def do_change(n_doors, trials): # Caso o jogador troque a porta
    rating = 0
    success = 0
    
    for i in range(1, trials):

        correct_door = rand.randint(1, n_doors)
        player_door = rand.randint(1, n_doors)

        # Criando lista com as outras portas pra abrir uma
        other_doors = list(range(1, n_doors+1))
        other_doors.remove(player_door)

        # Procura uma porta vazia pra abrir
        door_to_open = rand.choice(other_doors)

        if door_to_open == correct_door:
            door_to_open = sum(other_doors) - door_to_open

        other_doors.remove(door_to_open)

        # Troca a escolha
        player_door = other_doors[0]

        if (correct_door == player_door):  # Caso o a porta do jogador seja a correta
            rating += 2  # houve sucesso
            success += 1
        else:
            rating -= 1

    print("Com troca\nNúmero de tentativas:{}\nNota:{}\nPorcentagem:{}\n".format(trials, rating,
                                                                                 success / trials))


n_doors = 3  # número de portas
trials = 100000  # número de tentativas

do_not_change(n_doors, trials)

do_change(n_doors, trials)
