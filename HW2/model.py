from pulp import *

def model(MinQ, MaxQ):
    #Create a dictionary of the profits per unit for the 2 products
    Profits = {"A" : 470, "B" : 420}
    
    #Create a dictionary of availability of the 3 machines
    MachinesAvailability = {"M1" : 336, "M2" : 336, "M3" : 336}
    
    #Create a dictionary of usage of the 3 machines for each one of the 2 products 
    CapacityUsed = {"A": {"M1": 2, "M2": 0, "M3": 2},
                  "B":{"M1": 0, "M2": 2.5, "M3": 1.5}
                 }
    
    #Create a variable with fixed cost of production
    fixed_cost = 50000
    
    #Create a list of all the products
    Products = ["A","B"]
    
    #Create a list of all the machines
    Machines = ["M1","M2","M3"]
    
    #MAKE SURE THAT THIS PROBLEM HAS A SOLUTION
    min_usage_M1 = CapacityUsed['A']['M1']*MinQ['A'] + CapacityUsed['B']['M1']*MinQ['B']
    min_usage_M2 = CapacityUsed['A']['M2']*MinQ['A'] + CapacityUsed['B']['M2']*MinQ['B']
    min_usage_M3 = CapacityUsed['A']['M3']*MinQ['A'] + CapacityUsed['B']['M3']*MinQ['B']
    
    if min_usage_M1 >  MachinesAvailability['M1']:
        print('Machine 1 cannot produce enough to meet the minimum demand. The problem has no solution.')
    elif min_usage_M2 >  MachinesAvailability['M2']:
        print('Machine 2 cannot produce enough to meet the minimum demand. The problem has no solution.')
    elif min_usage_M3 >  MachinesAvailability['M3']:
        print('Machine 3 cannot produce enough to meet the minimum demand. The problem has no solution.')
    else:
        # Create the 'prob' variable to contain the problem data
        prob = LpProblem("2 products 3 machines", LpMaximize)
        
        # Create the Variables
        product_vars = {p:LpVariable("Product_{}".format(p),lowBound=MinQ[p],upBound=MaxQ[p],cat=LpContinuous) for p in Products}
        
        # The objective function is added to 'prob' first
        prob += lpSum([Profits[i]*product_vars[i] for i in Products]) - fixed_cost, "Total Revenue of Production Plan"
        
        # We can enter the constraints that relate to limited amount of material
        for r in Machines:
            prob += lpSum([product_vars[i]*CapacityUsed[i][r] for i in Products]) <= MachinesAvailability[r], r
        
        # The problem data is written to an .lp file
        prob.writeLP("MachinesProducts.lp")
        
        # The problem is solved using PuLP's choice of Solver
        prob.solve()
        
        # The status of the solution is printed to the screen
        print("Status:", LpStatus[prob.status])
        
        # Each of the variables is printed with it's resolved optimum value
        for v in prob.variables():
            print(v.name, "=", v.varValue)
        
        # The optimised objective function value is printed to the screen
        print("Total Profit of Plan = ", value(prob.objective))
        
        for constraint in prob.constraints:
            m = prob.constraints[constraint].name
            availability = int(-prob.constraints[constraint].constant)
            usage = availability + round(prob.constraints[constraint].value(), 1)
            print('Total usage of machine {}: {} hours'.format(m, usage))
            print('Total availability of machine {}: {} hours'.format(m, availability))