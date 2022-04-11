from mip import *


def createModel():
    name = ['x_12',  # 0
            'x_16',  # 1
            'x_17',  # 2
            'x_21',  # 3
            'x_23',  # 4
            'x_27',  # 5
            'x_34',  # 6
            'x_38',  # 7
            'x_45',  # 8
            'x_54',  # 9
            'x_65',  # 10
            'x_67',  # 11
            'x_78',  # 12
            'x_84']  # 13
    costs = [7, 5, 4, 7, 5, 6, 7, 4, 5, 5, 6, 4, 3, 4]
    model = Model(sense=MINIMIZE, solver_name=CBC, name='Army Network Flow Problem')

    variables = [model.add_var(var_type=CONTINUOUS, lb=0.0, name=str(i)) for i in name]

    model.objective = xsum(costs[i] * variables[i] for i in range(0, len(costs)))


    model += variables[3] - (variables[0] + variables[1] + variables[2]) == -20, 'Post1'
    model += variables[0] - (variables[3] + variables[4] + variables[5]) == -15, 'Post2'
    model += variables[4] - (variables[6] + variables[7]) == 10, 'Post3'
    model += (variables[6] + variables[13] + variables[9]) - variables[8] == 13, 'Posto4'
    model += (variables[8] + variables[10]) - variables[9] == 15, 'Post5'
    model += variables[1] - (variables[10] + variables[11]) == -3, 'Post6'
    model += (variables[2] + variables[5] + variables[11]) - variables[12] == 0, 'Post7'
    model += (variables[7] + variables[12]) - variables[13] == 0, 'Post8'

    model += variables[0] >= 0
    model += variables[0] <= 8

    model += variables[1] >= 0
    model += variables[1] <= 10

    model += variables[2] >= 2
    model += variables[2] <= 15

    model += variables[3] >= 5
    model += variables[3] <= 15

    model += variables[4] >= 0
    model += variables[4] <= 15

    model += variables[5] >= 0
    model += variables[5] <= 10

    model += variables[6] >= 0
    model += variables[6] <= 8

    model += variables[7] >= 2
    model += variables[7] <= 5

    model += variables[8] >= 0
    model += variables[8] <= 8

    model += variables[9] >= 1
    model += variables[9] <= 5

    model += variables[10] >= 0
    model += variables[10] <= 8

    model += variables[11] >= 3
    model += variables[11] <= 5

    model += variables[12] >= 5
    model += variables[12] <= 20

    model += variables[13] >= 0
    model += variables[13] <= 20

    return model


def main():
    model = createModel()
    status = model.optimize()

    print("Status = ", status)
    print("Solution value  = ", model.objective_value)

    model.write("probArmy_NF.lp")

    print("Solution:")

    for v in model.vars:
        if v.x > 0.00001:
            print(v.name, " = ", v.x)


if __name__ == '__main__':
    main()
