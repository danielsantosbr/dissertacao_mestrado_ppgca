# Laboratório

Esta pasta contêm diversos scripts relacionados no trabalho com a criação dos conjuntos de dados de laboratório e DARPA 2009, assim como, a sua "tradução" por meio das fórmulas mencionadas no trabalho, e verifica se está ocorrendo um ataque ou não no sistema (predição).

- 1_ryu_control.py: Relaciona-se à inicialização do sistema através do controlador SDN Ryu na sua versão 4.3.4.
- 2_mininet_topology.py: Inicia a topologia da rede através do Mininet sendo 6 switches com 20 hosts (podendo ser adaptado).
- 3_collect.sh: Considerado o principal script do sistema, ele faz a extração das 5 características do fluxo do OpenFlow (dump), grava em arquivos, e posteriormente faz a aplicação das fórmulas, e em fim, a checagem se há um ataque ou não.
- 4_computeTuples.py: Faz a tradução da coleta dos fluxos nas fórmulas mencionadas no trabalho.
- 5_inspector.py: Script relacionado com a predição em si do sistema se há um ataque ou não.

> Como mencionado no trabalho, parte destes scripts foram adaptados do trabalho de Ye et al. (2018a).