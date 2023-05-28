# Decision Tree Classifier

## Como correr

Executar o código em python com ```python3 DecisionTree.py [dataset]```

O argumento ```[dataset]``` pode ser os seguintes valores:

- iris
- restaurant
- weather

O output será um decision tree classifier para esse dataset.

## Como classificar entradas

Para classificar entradas, basta criar um ficheiro CSV com as entradas necessárias e, quando pedido para testar a classificação, inserir o caminho do ficheiro no input.
Como output será dado um print para cada entrada, seguido da sua classificação.

#### Restrições do ficheiro CSV

Para fins de teste, é necessário remover a coluna ID e a coluna da variável alvo do ficheiro CSV utilizado para testar a àrvore de decisão.

## Packages Necessários

- numpy
- copy
- sys