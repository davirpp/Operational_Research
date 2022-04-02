from mip import *


def createModel():
    names = ['13',   # 0
             '14',   # 1
             '23',   # 2
             '25',   # 3
             '36',   # 4
             '45',   # 5
             '54',   # 6
             '64',   # 7
             '65']   # 8
    costs = [1, 13, 1, 9, 5, 5, 3, 1, 2]

    model = Model(sense=MINIMIZE, solver_name=CBC, name='Network Flow Model')

    variables = [model.add_var(var_type=CONTINUOUS, lb=0.0, name='x_' + str(i)) for i in names]

    model.objective = xsum(costs[i] * variables[i] for i in range(len(variables)))

    model += 0 - (variables[0] + variables[1]) == -8
    model += 0 - (variables[2] + variables[3]) == -6
    model += (variables[0] + variables[2]) - variables[4] == 0
    model += (variables[1] + variables[6] + variables[7]) - variables[5] == 7
    model += (variables[3] + variables[5] + variables[8]) - variables[6] == 7
    model += variables[4] - (variables[7] + variables[8]) == 0

    model += variables[0] >= 2
    model += variables[0] <= 4

    model += variables[1] >= 0
    model += variables[1] <= 6

    model += variables[2] >= 1
    model += variables[2] <= 4

    model += variables[3] >= 0
    model += variables[3] <= 3

    model += variables[4] >= 0
    model += variables[4] <= 8

    model += variables[5] >= 0
    model += variables[5] <= 3

    model += variables[6] >= 0
    model += variables[6] <= 2

    model += variables[7] >= 0
    model += variables[7] <= 5

    model += variables[8] >= 0
    model += variables[8] <= 5

    return model


def main():
    model = createModel()
    status = model.optimize()
    print("Status = ", status)
    print("Solution value  = ", model.objective_value)

    model.write("probNF.lp")

    print("Solution:")

    for v in model.vars:
        if v.x > 0.00001:
            print(v.name, " = ", v.x)


if __name__ == "__main__":
    main()
