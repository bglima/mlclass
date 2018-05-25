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

# Valores Padrões
default_n_doors = 3
default_trials = 5000
default_swap_door_every_n = [2, 10]


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

    options = parser.parse_args()[0]

    return (options.n_doors, options.trials)


# Inicializa as portas. Retorna um array com as portas e o índice da porta correta
def init_doors(n_doors):
    correct_door = rand.randint(1, n_doors)
    player_door = rand.randint(1, n_doors)
    return (correct_door, player_door)


# Inicializa a lista de políticas. Para os casos de alternância, adiciona cada mudança à lista
def init_policies(swap_door_every_n):
    policies = ['ALWAYS_CHANGE', 'NEVER_CHANGE', 'RANDOM_POLICY']

    if len(swap_door_every_n) == 0:
        return policies
    else:
        for n in swap_door_every_n:
            policies.append('CHANGE_EVERY_' + str(n))
        return policies


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


#  Avalie a política passada como parâmetro
def evaluate_policy_dt( policy, n_doors, trials ):
    # Inicializa a função valor de forma arbitrária
    V_policy_list = []  # Valores da função valor-estado seguindo a política especificada
    success = 0         # Quantidade de acertos totais nos episódios

    # Repete para cada tentativa
    for i in range(1, trials):
        (correct_door, player_door) = init_doors( n_doors )
        montys_door = open_doors(player_door, correct_door, n_doors)

        # Execute a ação definida na política
        if 'ALWAYS_CHANGE' in policy:
            (player_door, montys_door) = change_doors(player_door, montys_door, True)
        elif 'CHANGE_EVERY_' in policy:
            n = int(policy.split('_')[2])  # Muda a porta a cada CHANGE rodadas, permanecendo com a porta original nas demais
            (player_door, montys_door) = alternate_every_n(player_door, montys_door, n, i)
        elif 'NEVER_CHANGE' in policy:
            (player_door, montys_door) = change_doors(player_door, montys_door, False)
        elif 'RANDOM_POLICY' in policy:
            (player_door, montys_door) = change_random(player_door, montys_door)
        else:
            print('Unknown policy... :( Please choose a valid one!\n')
            return -1

        # Retorno dado pelo ambiente
        if (correct_door == player_door):  # Verifica se a porta do jogador é a correta
            reinforcement = 1  # houve sucesso
        else:
            reinforcement = 0  # nope

        # Atualiza o valor da política
        success += reinforcement
        V_policy_last = success / i  # Média dos valores
        V_policy_list.append(V_policy_last)

    return (success, V_policy_list)


def main():

    (n_doors, trials) = init_parser()

    best_policy = {"name": "",
                   "success": 0}

    policies = init_policies(default_swap_door_every_n)

    fig = plt.figure(figsize=(8, 6))
    ax = plt.subplot(111)

    for policy in policies:
        (success, V_list) = evaluate_policy_dt(policy, n_doors, trials)
        print("Política: ", policy, "\nNúmero de tentativas:{}\nAcertos:{}\nPorcentagem:{}\n".format(trials, success, round(V_list[-1],3)))
        plot(V_list, policy, fig, n_doors)

        if(success > best_policy["success"]):
            best_policy["success"] = success
            best_policy["name"] = policy

    print("The best policy is: ", best_policy["name"])

    ax.legend(loc='lower center')

    filename = generate_filename()
    fig.savefig(filename)
    plt.show()

if __name__ == '__main__':
    main()
