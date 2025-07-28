from pyomo.environ import Set, Var, Constraint, ConcreteModel, Param, Objective, minimize, NonNegativeReals
from pyomo.contrib.appsi.solvers.highs import Highs
opt = Highs()

class TransportationModel:
    def __init__(self, supply, demand, cost):
        self.model = ConcreteModel()

        self.supply = supply
        self.demand = demand
        self.cost = cost

        self.origins = list(supply.keys())
        self.destinations = list(demand.keys())

        self._build_model()

    def _build_model(self):
        m = self.model
        m.O = Set(initialize=self.origins)
        m.D = Set(initialize=self.destinations)
        m.x = Var(m.O, m.D, domain=NonNegativeReals)

        # Objective
        m.cost = Param(m.O, m.D, initialize=self.cost)
        m.obj = Objective(expr=sum(m.cost[o, d] * m.x[o, d] for o in m.O for d in m.D), sense=minimize)

        # Supply constraints
        m.supply = Param(m.O, initialize=self.supply)
        m.supply_con = Constraint(m.O, rule=lambda m, o: sum(m.x[o, d] for d in m.D) <= m.supply[o])

        # Demand constraints
        m.demand = Param(m.D, initialize=self.demand)
        m.demand_con = Constraint(m.D, rule=lambda m, d: sum(m.x[o, d] for o in m.O) >= m.demand[d])

    def solve(self):
        solver = opt
        result = solver.solve(self.model)
        return result

    def get_solution(self):
        return {(o, d): self.model.x[o, d].value for o in self.model.O for d in self.model.D if self.model.x[o, d].value > 0}

# Example data
supply = {'Seattle': 350, 'San Diego': 600}
demand = {'New York': 325, 'Chicago': 300, 'Topeka': 275}
cost = {
    ('Seattle', 'New York'): 2.5, ('Seattle', 'Chicago'): 1.7, ('Seattle', 'Topeka'): 1.8,
    ('San Diego', 'New York'): 2.5, ('San Diego', 'Chicago'): 1.8, ('San Diego', 'Topeka'): 1.4
}

# Run the model
model = TransportationModel(supply, demand, cost)
model.solve()
solution = model.get_solution()
print("Optimal Shipments:")
for key, val in solution.items():
    print(f"{key}: {val}")
