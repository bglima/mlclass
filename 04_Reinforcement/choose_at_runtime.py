'''
Created on 21 de mai de 2018

Objetivo: Provar a solução do problema de Monty Hall utilizando Monte Carlo

@authors: Bruno Gabriel Lima
          João Paulo Clarindo
          Nilson Sales
'''

import random as rand
import matplotlib.pyplot as plt
import optparse
import time
import datetime
import numpy

# Retorna um nome de arquivo único usando o timestamp
def generate_filename():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return ('V_plot_' + st + '.png')


# Plota os valores de y na imagem img_name
def plot(y, name, fig, n_doors):
    plt.plot(y, label=name)
    plt.ylabel('Success rate')
    plt.xlabel('Iterations')
    title = "Monty Hall problem with " + str(n_doors) + " doors"
    plt.title(title)


# Parser. Trem três opções disponíveis. Caso o usuário não adicione as opções, valores padrões serão usados
def init_parser():
    parser = optparse.OptionParser("Uso: %prog [options]")
    parser.add_option("-d", "--doors", dest="n_doors",
                      default=default_n_doors, type="int", help="Number of doors")
    parser.add_option("-t", "--trials", dest="trials",
                      default=default_trials, type="int", help="Number of trials")
    parser.add_option("-a", "--alpha", dest="alpha",
                      default=default_alpha, type="float", help="Learning rate")

    options = parser.parse_args()[0]

    return (options.n_doors, options.trials, options.alpha)


# Inicializa as portas. Retorna um array com as portas e o índice da porta correta
def init_doors(n_doors):
    correct_door = rand.randint(1, n_doors)
    player_door = rand.randint(1, n_doors)
    return (correct_door, player_door)


# Deixa apenas duas portas fechadas: a inicial do jogador e mais uma. Uma delas deve conter o prêmio
def open_doors(player_door, correct_door, n_doors):
        # Criando lista com as outras portas disponíveis
        other_doors = list(range(1, n_doors+1))
        other_doors.remove(player_door)
        # Abre outra(s) porta(s) e deixa uma fechada
        # Se a porta do jogador for a correta, oferece uma porta aleatória pra trocar
        if player_door == correct_door:
            try:
                keep_closed = rand.choice(other_doors)
            except:
                print('Número de portas insuficiente para o problema')
        # Se não, abre todas e deixa a correta
        else:
            keep_closed = correct_door

        return keep_closed


# Executa a ação de trocar a porta do jogador ou permanecer com a inicial
def change_doors(current_door, another_door, change=True):
    if ( change ):
        return (another_door, current_door)
    else:
        return (current_door, another_door)


# Política aleatória
def change_random(current_door, another_door):
    change = rand.randint(0, 1)
    if ( change ):
        return (another_door, current_door)
    else:
        return (current_door, another_door)


# Política de alternar (ALTERNATE_EVERY_N_TRIALS)
def alternate_every_n(player_door, another_door, each_n, trial_index):
    if trial_index % each_n == 0:
        return (another_door, player_door)
    else:
        return (player_door, another_door)


# Checa a matriz de V e retorna a melhor
def find_best_policy( V_policy ):
    best_policy = max(V_policy.items(), key=lambda k: k[1])
    return best_policy

#  Avalie a política passada como parâmetro
def evaluate_and_act( V_policy, n_doors, trial_number, alpha ):
    # # Inicializa a função valor de forma arbitrária
    # V_policy_list = []  # Valores da função valor-estado seguindo a política especificada
    # success = 0         # Quantidade de acertos totais nos episódios


    # Inicializa o ambiente
    (correct_door, player_door) = init_doors( n_doors )
    montys_door = open_doors(player_door, correct_door, n_doors)

    # Checa qual a ação de melhor V
    (best_policy, best_policy_value) = find_best_policy( V_policy )

    # Execute a ação definida na política
    if 'ALWAYS_CHANGE' in best_policy:
        (player_door, montys_door) = change_doors(player_door, montys_door, True)
    elif 'CHANGE_EVERY_' in best_policy:
        n = int(best_policy.split('_')[2])  # Rodadas mantendo a porta até mudar
        (player_door, montys_door) = alternate_every_n(player_door, montys_door, n, trial_number)
    elif 'NEVER_CHANGE' in best_policy:
        (player_door, montys_door) = change_doors(player_door, montys_door, False)
    elif 'RANDOM_POLICY' in best_policy:
        (player_door, montys_door) = change_random(player_door, montys_door)
    else:
        print('Unknown policy... :( Please choose a valid one!\n')
        return -1

    # Retorno dado pelo ambiente
    if (correct_door == player_door):  # Verifica se a porta do jogador é a correta
        reinforcement = 1  # houve sucesso
    else:
        reinforcement = 0  # nope

    # Atualiza o valor da política usando Belmann
    V_policy[ best_policy ] = V_policy[ best_policy ] + alpha*( reinforcement - V_policy[best_policy] )
    return V_policy

# Valores Padrões
default_n_doors = 3
default_trials = 100000
default_alpha = 0.005
default_swap_door_every_n = [2, 10]
policies = ['ALWAYS_CHANGE', 'NEVER_CHANGE', 'RANDOM_POLICY', 'CHANGE_EVERY_2', 'CHANGE_EVERY_10']

def main():

    (n_doors, trials, alpha) = init_parser()

    V_policy =  {}  # Inicializa a matriz de Vs
    V_points = {}   # Inicializa a lista de pontos a serem plotados

    for policy in policies:
        V_policy[policy] = 1 # Inicia os Vs aleatoriamente entre 0 e 1
        V_points[policy] = []

    # Escolhe a melhor política apartir dos Vs aleatórios definidos anteriormente
    (last_best_policy, last_best_policy_value) = find_best_policy( V_policy )
    print('The best policy in event 0 is: ', last_best_policy, ' with V equal to ', last_best_policy_value)

    # Prepara as figuras a serem plotadas
    fig = plt.figure(figsize=(8, 6))
    ax = plt.subplot(111)

    # Executa os escolhendo agir sempre com a política ótima até então
    for trial_number in range(trials):
        # Checa a melhor política, age e atualiza a matriz dos Vs
        V_policy = evaluate_and_act( V_policy, n_doors, trial_number, alpha )
        # Avalia qual a melhor nova política
        (best_policy, best_policy_value ) = find_best_policy( V_policy )

        # Se a melhor política mudar, avise ao usuário
        if best_policy != last_best_policy:
            print("The best policy changed in event ", trial_number, "and now it is: ", best_policy, " with V equal to ", best_policy_value)
            last_best_policy = best_policy
            last_best_policy_value = last_best_policy_value

        # Adiciona os valores atuais ao gráfico
        for policy in policies:
            V_points[policy].append( V_policy[policy] )

    # Mostra o resultado final
    print('The best policy in event ', trials, ' is: ', last_best_policy, ' with V equal to ', V_policy[last_best_policy])

    # Plota e salva o gráfico
    for policy in policies:
        plot(V_points[policy], policy, fig, n_doors)

    ax.legend(loc='lower center')

    filename = generate_filename()
    fig.savefig(filename)
    plt.show()

if __name__ == '__main__':
    main()
