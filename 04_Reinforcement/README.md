## Resolução do Problema de Monty Hall utilizando Monte Carlo

![Plot](https://raw.githubusercontent.com/bglima/mlclass/master/04_Reinforcement/V_plot_2018-05-25%2018%3A15%3A30.png)

### Descrição do Problema

Este é um problema clássico criado por um programa de TV americano chamado "Let's Make a Deal", inicialmente apresentado por Monty Hall.

O problema consiste na seguinte situação: há 3 portas portas a serem escolhidas pelo jogador. Numa delas há um carro e nas outras duas há cabras. O apresentador sabe em qual das portas se encontra o carro.

Após a escolha do jogador, o apresentador abre uma das duas portas restantes que não contém o carro. Então, pergunta ao jogador se ele deseja trocar de porta ou continuar com a escolha inicial.

### Como endereçamos o problema

Através da avaliação de políticas previamente estabelecidas. Considerando que seja possível repetir o game um número T de vezes, as políticas implementadas são:
 - sempre trocar a porta original
 - sempre manter a porta original
 - trocar a porta original a cada C vezes

Para a avaliação, utilizamos o método Monte Carlo de Primeira Visita. Nesse caso, o valor da função Valor-Estado será dado pela média dos retornos obtidos no episódio seguindo a política em questão.

Cada episódio consiste em um jogo. Da forma de modelamos, o jogado escolhe a primeira porta aleatoriamente. Então, uma das portas restantes é aberta (que não contém o prêmio), restando apenas a do jogador e a outra.

Nesse momento, a política em questão é aplicada para que o jogador troque ou não sua porta original. Após executada a ação, um reforço de +1 é obtido caso o jogador ganhe, obtendo 0 caso contrário.

Todas as políticas são avaliadas e então a melhor política (de maior valor-estado) é mostrada ao fim do programa.

Implementamos o programa para um número D de portas, customizável pelo usuário. Além disso, geramos os gráficos das atualizações da função-valor de cada política.

### Parâmetros utilizados

 ```-d``` ou ```--door``` : Número de portas no problema. O padrão é 3 portas.

 ```-t``` ou ```--trials``` : Número de episódios a serem explorados. O padrão é 100000 episódios.
 
 ```-a``` ou ```--alpha```: Taxa de aprendizagem usada para a atualização da dos valores da função-valor. Padrão é 0.05.

 ```-h``` ou ```--help```: Exibe a ajuda.

 ### Exemplo de execução

 ```python3 montecarlo.py --doors 3 --trials 100000 --alpha 0.05```
