from pyomo.environ import *
from pyomo.contrib.appsi.solvers.highs import Highs


opt = Highs()

m = AbstractModel()
m.i = RangeSet(3)
m.x = Var(m.i, bounds=(0, 10))
def rule_c1(m):
    return sum(m.x[i] for i in m.i) >= 13
m.C1 = Constraint(rule= rule_c1)

def rule_of(m):
    return sum(i*m.x[i] for i in m.i)
m.of = Objective(rule=rule_of, sense=minimize)
instance = m.create_instance()
resulte = opt.solve(instance)

for i in instance.i:
    print(i, value(instance.x[i]))

