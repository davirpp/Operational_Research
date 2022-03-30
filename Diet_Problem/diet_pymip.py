import sys
from mip import *


def readInstance(filePath):
    f = open(filePath, "r")  # Abertura de arquivo usando sys.argv[1] no objeto f

    l = f.readline()  # Pega primeira linha
    nb_foods, nb_nutrients = int(l.split()[0]), int(l.split()[1])  # Recebe 2 variáveis e as armazena

    l = f.readline()  # Pega a segunda linha
    costs = [float(c) for c in l.split()]  # Cria uma lista iterando o conteúdo da linha

    l = f.readline()  # Pega a terceira linha
    min_levels = [float(m) for m in l.split()]  # Cria uma lista iterando o conteúdo da linha

    food_nutr_levels = []  # Cria a lista vazia
    for i in range(nb_foods):  # Utiliza até o range(0, nb_foods - 1), nesse caso(instance2.txt) nb_foods=4
        l = f.readline()  # Pega as linhas faltantes por meio da iteração do for
        levels = [float(level) for level in l.split()]  # Cria uma lista iterando o conteúdo da linha
        food_nutr_levels.append(levels)  # Coloca a lista que acabou de ser 'criada' dentro da lista vazia
        # Assim, food_nutr_levels é uma lista de listas
    f.close()  # Encerra a leitura do objeto f

    return nb_foods, nb_nutrients, costs, min_levels, food_nutr_levels  # Retorna os valores determinados


def createModel(nb_foods, nb_nutrients, costs, min_levels, food_nutr_levels):
    model = Model(sense=MINIMIZE, solver_name=CBC)  # Cria o objeto model no construtor padrão, com o parâmetro
    # sense=MINIMIZE para minimizar o modelo e determina o solver CBC

    x = [model.add_var(var_type="CONTINUOUS", lb=0.0, name='x' + str(i))
         for i in range(nb_foods)]  # Cria uma lista de objetos do tipo variável
    # Adiciona as variáveis ao modelo, sempre do tipo "CONTINUOUS", determina o limite inferior(lb=0.0)
    # Nomeia as variáveis com x(iteração sobre os números(servindo apenas de label) contidos na lista nb_foods)

    model.objective = xsum(costs[i] * x[i] for i in range(nb_foods))  # Cria a função objetivo do modelo
    # Utiliza a função xsum, propria do MIP (Somatório)
    # Na função ele mostra que a função objetivo faz:
    # Faça uma combinação linear dos custos multiplicados pelas variáveis respectivas
    # para saber a quantidade de cada nutriente

    for j in range(nb_nutrients):  # for para iterar sobre o nb_nutrients(em instance2.txt =2) e criar cada restrição
        model += xsum(food_nutr_levels[i][j] * x[i]
                      for i in range(nb_foods)) >= min_levels[j], "NUTRI_" + str(j)
        # O '+=' adicionando ao model é uma sintaxe da biblioteca para adicionar restrições,
        # que como tem no problema é Vitamina A ≥ 3,000 UI e Vitamina C ≥ 50 mg
        # Ele adiciona como restrições, uma combinação linear primeiro iterando o j para pegar o nutriente1
        # E faz uma combinação linear multiplicando pelas variáveis respectivas em x sendo o RHS a parte do
        # ">= min_levels[j]", e após isso, nomeia cada restrição

    return model  # Retorna o modelo ja pronto


def main():  # Define a main exclusiva para isso
    nb_foods, nb_nutrients, costs, min_levels, food_nutr_levels = readInstance(
        sys.argv[1])  # Preenche cada variável lendo o arquivo usando a função criada readInstance

    model = createModel(nb_foods, nb_nutrients, costs,
                        min_levels, food_nutr_levels)
    # 'Cria'/Inicializa o modelo na variável model

    status = model.optimize()  # Retorna o status da otimização

    print("Status = ", status)
    print("Solution value  = ", model.objective_value)

    model.write("model_diet.lp")  # Cria um arquivo .lp com a Programação Linear do problema

    print("Solution:")
    for v in model.vars:  # Iteração sobre o model.vars que são as variáveis criadas na linha 32
        if v.x > 0.00001:  # Caso o valor da variável (v.x) seja maior que 0, significa que a variável foi utilizada
            print(v.name, " = ", v.x)


if __name__ == "__main__":
    main()
