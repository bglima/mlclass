'''
Created on 21 de mai de 2018

Objetivo: Provar a solução do problema de Monty Hall utilizando Monte Carlo

@authors: Bruno Gabriel Lima
          João Paulo Clarindo
          Nilson Sales
'''


import random as rand
import matplotlib.pyplot as plt

# Plota os valores de y na imagem img_name
def plot(y, name, fig):
    plt.plot(y, label=name)
    plt.ylabel('Success rate')
    plt.xlabel('Iterations')
  
# Inicializa as portas. Retorna um array com as portas e o índice da porta correta
def init_doors(n_doors):
    correct_door = rand.randint(1, n_doors)
    player_door = rand.randint(1, n_doors)
    return (correct_door, player_door)

# Deixa apenas duas portas abertas: a inicial do jogador e mais uma. Uma delas deve conter o prêmio
def open_doors(player_door, correct_door, n_doors):
        # Criando lista com as outras portas disponíveis
        other_doors = list(range(1, n_doors+1))
        # Abre outra(s) porta(s) e deixa uma fechada
        # Se a porta do jogador for a correta, oferece uma porta aleatória pra trocar
        if player_door == correct_door:
            keep_closed = rand.choice(other_doors)
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

# Política de alternar (OPEN_EVERY_N_TRIALS)
def alternate_each_n(player_door, another_door, each_n, trial_index):
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
        if policy == 'ALWAYS_CHANGE':
            (player_door, montys_door) = change_doors(player_door, montys_door, True)
        elif policy == 'CHANGE_EVERY_2':
            (player_door, montys_door) = alternate_each_n(player_door, montys_door, 2, i)
        elif policy == 'CHANGE_EVERY_5':
            (player_door, montys_door) = alternate_each_n(player_door, montys_door, 5, i)
        elif policy == 'CHANGE_EVERY_10':
            (player_door, montys_door) = alternate_each_n(player_door, montys_door, 10, i)
        elif policy == 'NEVER_CHANGE':            
            (player_door, montys_door) = change_doors(player_door, montys_door, False)
        elif policy == 'RANDOM_POLICY':
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
    n_doors = 3     # Número de portas
    trials = 10000  # Número de tentativas
    highest_success = 0

    policies = ['ALWAYS_CHANGE', 'CHANGE_EVERY_2', 'CHANGE_EVERY_5', 'CHANGE_EVERY_10', 'NEVER_CHANGE', 'RANDOM_POLICY']

    fig = plt.figure(figsize=(8, 6))
    ax = plt.subplot(111)
    
    for policy in policies:
        (success, V_list) = evaluate_policy_dt( policy, n_doors, trials )
        print("Política: ", policy, "\nNúmero de tentativas:{}\nAcertos:{}\nPorcentagem:{}\n".format(trials, success, V_list[-1]))
        plot(V_list, policy, fig)

        if(success > highest_success):
            highest_success = success
            best_policy = policy

    print("The best policy is: ", best_policy)
    
    ax.legend(loc='lower center')
    plt.show()
    fig.savefig('V_plot.png')


if __name__ == '__main__':
    main()


