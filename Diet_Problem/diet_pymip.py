import sys
from mip import *


def readInstance(filePath):
    f = open(filePath, "r")  # Opening the file with sys.argv[1] on the object f

    l = f.readline()  # Takes first row
    nb_foods, nb_nutrients = int(l.split()[0]), int(l.split()[1])  # Get 2 variables

    l = f.readline()  # Takes second row
    costs = [float(c) for c in l.split()]  # Creates a list iterating over the content of the row

    l = f.readline()  # Takes third row
    min_levels = [float(m) for m in l.split()]  # Creates a list iterating over the content of the row

    food_nutr_levels = []  # Creates an empty list
    for i in range(nb_foods):  # Range(0, nb_foods - 1), on main case(instance.txt) nb_foods=4
        l = f.readline()  # Takes the missing rows
        levels = [float(level) for level in l.split()]  # Creates a list iterating over the content of the row
        food_nutr_levels.append(levels)  # Put the list inside of the empty list
        # So food_nutr_levels is a list of lists
    f.close()  # Finishes the reading of object f

    return nb_foods, nb_nutrients, costs, min_levels, food_nutr_levels  # Returns the read data


def createModel(nb_foods, nb_nutrients, costs, min_levels, food_nutr_levels):
    model = Model(sense=MINIMIZE, solver_name=CBC)  # Creates the Model object in the default constructor, with the parameters
    # sense=MINIMIZE to minimize the model and determinate the solver CBC

    x = [model.add_var(var_type="CONTINUOUS", lb=0.0, name='x' + str(i))
         for i in range(nb_foods)]  # Creates a list of objects from Var type
    # Add variables to the model, in Linear Programming, the type will always be "CONTINUOUS", and determinates the lower bound(lb) = 0
    # Name tha variables with x(iterating over the numbers(just like a label) inside the list nb_foods)

    model.objective = xsum(costs[i] * x[i] for i in range(nb_foods))  # Creates the objective function of the model
    # Uses the 'xsum' function, from MIP
    # On that function it shows that the objective function does:
    # Make a linear combination of the costs multiplied by the respective variables
    # to know the quantity of each nutrient

    for j in range(nb_nutrients):  # for to iterate over nb_nutrients(in instance.txt =2) and create each constraint
        model += xsum(food_nutr_levels[i][j] * x[i]
                      for i in range(nb_foods)) >= min_levels[j], "NUTRI_" + str(j)
        # The '+=' adding to the model is a library syntax to add constraints,
        # that like is on the problem, Vitamin A ≥ 3000 UI and Vitamin C ≥ 50 mg
        # It adds like the constraints, a linear combination iterating the j to catch the nutrient 1
        # And does a linear combination multiplying its respective variables in x, being the RHS part of
        # ">= min_levels[j]", and after that, names every constraints

    return model  # Returns the finished model


def main():  # Defines the main function
    nb_foods, nb_nutrients, costs, min_levels, food_nutr_levels = readInstance(
        sys.argv[1])  # Fills every variable reading the file using the created function readInstance

    model = createModel(nb_foods, nb_nutrients, costs,
                        min_levels, food_nutr_levels)
    # 'Creates'/Initializes the model

    status = model.optimize()  # Returns the optimization status

    print("Status = ", status)
    print("Solution value  = ", model.objective_value)

    model.write("model_diet.lp")  # Create a .lp file with the Linear Programming of the problem

    print("Solution:")
    for v in model.vars:  # Iterating over model.vars that are the variables created on row 32
        if v.x > 0.00001:  # If the value of the variable (v.x) is bigger than 0, it means that the variable was used
            print(v.name, " = ", v.x)


if __name__ == "__main__":
    main()
