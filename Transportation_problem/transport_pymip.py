import sys
from mip import *


def readInstance(filePath):
    f = open(filePath, "r")  # Abertura de arquivo usando sys.argv[1] no objeto f

    l = f.readline()  
    nb_industries, nb_cities = int(l.split()[0]), int(l.split()[1]) 

    costs = []
    for i in range(nb_industries):  
        l = f.readline() 
        costs.append([float(c) for c in l.split()]) 

    l = f.readline()
    capacities = [float(c) for c in l.split()]

    l = f.readline()
    demands = [float(d) for d in l.split()] 

    f.close()  

    return nb_industries, nb_cities, costs, capacities, demands 


def createModel(nb_industries, nb_cities, costs, capacities, demands):
    model = Model(sense=MINIMIZE, solver_name=CBC)  
    
    x = [[model.add_var(var_type="CONTINUOUS", lb=0.0,
                        name="x_" + str(i) + "_" + str(j)) for j in range(nb_cities)] for i in range(nb_industries)]

    model.objective = xsum(costs[i][j]*x[i][j]
                           for i in range(nb_industries) for j in range(nb_cities))  

    for i in range(nb_industries):
        model += xsum(x[i][j] for j in range(nb_cities)
                      ) <= capacities[i], "CAP_" + str(i)

    for j in range(nb_cities):
        model += xsum(x[i][j] for i in range(nb_industries)
                      ) >= demands[j], "DEM_" + str(j)

    return model  


def main(): 
    nb_industries, nb_cities, costs, capacities, demands = readInstance(
        sys.argv[1]) 
    model = createModel(nb_industries, nb_cities,
                        costs, capacities, demands)

    status = model.optimize()

    model.write("model_transport.lp") 

    print("Status = ", status)
    print("Solution value  = ", model.objective_value)

    print("Solution:")
    for v in model.vars:
        if v.x > 0.00001:
            print(v.name, " = ", v.x)


if __name__ == "__main__":
    main()
