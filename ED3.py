
from pyomo.environ import Set, Var, Constraint, ConcreteModel, Param, Objective, minimize, NonNegativeReals
from pyomo.contrib.appsi.solvers.highs import Highs
from base import Generator, Generators
opt = Highs()

class TransportationModel:
    def __init__(self, generators, demand):
        self.model = ConcreteModel()
        self.gens = generators
        self.demand = demand
        self._build_model()
    def _build_model(self):
        m = self.model
        m.i = Set(initialize=[gen for gen in self.gens])

        def bound_lim(m,i:Generator):
            return (i.pmin, i.pmax)
        m.P = Var(m.i, bounds= (0,100))
        def rule_c1(m):
            return sum(m.P[gen] for gen in self.gens) >= self.demand
        m.C10 = Constraint(rule = rule_c1)
        def rule_of(m):
            return sum(m.P[gen] for gen in self.gens)
        m.of = Objective(rule = rule_of , sense= minimize)
    def solve(self):
        solver = opt
        result = solver.solve(self.model)
        return result
    def get_solution(self):
        dic = {g.id:self.model.P[g].value for g in self.model.P}
        return dic


gen_set1 = [Generator(
    id = i,
    pmax= int(100-5*i),
    pmin= int(0+i*5)
) for i in range(4) ]

demand = 150

my_model = TransportationModel(gen_set1, demand)
result1 = my_model.solve()
d = my_model.get_solution()
print(d)



