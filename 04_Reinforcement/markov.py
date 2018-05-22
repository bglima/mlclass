'''
Created on 21 de mai de 2018

Objetivo: Provar a solução do problema de Monty Hall utilizando aprendizagem por reforço

@authors: Bruno Gabriel
          João Paulo Clarindo
          Nilson Sales
'''


import random as rand
import matplotlib.pyplot as plt


def plot(y):
    plt.plot(y)
    plt.ylabel('Success rate')
    plt.xlabel('Iterations')
    plt.show()


def do_not_change(n_doors, trials):  # Caso o jogador não troque a porta
    success = 0
    success_rates = []

    for i in range(1, trials):
        correct_door = rand.randint(1, n_doors)
        player_door = rand.randint(1, n_doors)

        if (correct_door == player_door):  # Caso o a porta do jogador seja a correta
            success += 1

        success_rates.append(success/i)

    print("Sem troca\nNúmero de tentativas:{}\nAcertos:{}\nPorcentagem:{}\n".format(trials, success,
                                                                                       success / trials))
    plot(success_rates)


def do_change(n_doors, trials): # Caso o jogador troque a porta
    rating = 0
    success = 0
    success_rates = []

    for i in range(1, trials):

        correct_door = rand.randint(1, n_doors)
        player_door = rand.randint(1, n_doors)

        # Criando lista com as outras portas pra abrir uma
        other_doors = list(range(1, n_doors+1))
        other_doors.remove(player_door)

        # Abre outra(s) porta(s) e deixa uma fechada
        # Se a porta do jogador for a correta, escolha uma porta aleatória pra trocar
        if player_door == correct_door:
            keep_closed = rand.choice(other_doors)
        # Se não, abre todas e deixa a correta
        else:
            keep_closed = correct_door

        # Troca a escolha
        player_door = keep_closed

        if (correct_door == player_door):  # Caso o a porta do jogador seja a correta
            success += 1  # houve sucesso

        success_rates.append(success/i)

    print("Com troca\nNúmero de tentativas:{}\nAcertos:{}\nPorcentagem:{}\n".format(trials, success,
                                                                                 success/trials))
    plot(success_rates)


n_doors = 3  # número de portas
trials = 1000  # número de tentativas

do_not_change(n_doors, trials)

do_change(n_doors, trials)
