import sys
from mip import *


def readInstance(filePath):
    f = open(filePath, 'r')

    l = f.readline()
    nb_grains = int(l.split()[0])

    l = f.readline()
    g_name = l.split()

    l = f.readline()
    prod = [float(p) for p in l.split()]

    l = f.readline()
    profit = [float(p) for p in l.split()]

    l = f.readline()
    min_g_area = [float(m) for m in l.split()]

    l = f.readline()
    max_area, max_prod = float(l.split()[0]), float(l.split()[1])

    f.close()
    return nb_grains, g_name, prod, profit, min_g_area, max_area, max_prod


def createModel(nb_grains, g_name, prod, profit, min_g_area, max_area, max_prod):
    model = Model(sense=MAXIMIZE, solver_name=CBC, name='Max Grain Profit')

    x = [model.add_var(var_type='CONTINUOUS', lb=0.0, name='x_' + str(i)) for i in g_name]

    model.objective = xsum(x[i] * profit[i] * prod[i] for i in range(nb_grains))

    for i in range(nb_grains):
        model += x[i] >= min_g_area[i], 'min_area_' + g_name[i]

    model += xsum(x[i] * prod[i] for i in range(nb_grains)) <= max_prod, 'max_prod'

    model += xsum(x[i] for i in range(nb_grains)) <= max_area, 'max_area'

    return model


def main():
    nb_grains, g_name, prod, profit, min_g_area, max_area, max_prod = readInstance('instance.txt')

    model = createModel(nb_grains, g_name, prod, profit, min_g_area, max_area, max_prod)

    status = model.optimize()

    print("Status = ", status)
    print("Solution value  = ", model.objective_value)

    model.write("prob1-1.lp")

    print("Solution:")
    it = 0
    for v in model.vars: 
        if v.x > 0.00001: 
            print(v.name, "area = ", v.x)
            print(v.name, "kgs = ", v.x * prod[it])
            print()
            it += 1


if __name__ == "__main__":
    main()
