from base import Generator, Generators
from pyomo.environ import *
from pyomo.contrib.appsi.solvers.highs import Highs


opt = Highs()

gens_id = {id:Generator(
    id = id,
    pmin = 10,
    pmax =100
) for id in range(4)}

from pyomo.environ import *
from pyomo.contrib.appsi.solvers.highs import Highs


opt = Highs()

m = AbstractModel()
m.i = RangeSet(3)
m.x = Var(m.i, bounds=(0, 1000))
def rule_c1(m):
    return sum(m.x[i] for i in m.i) >= 300
m.C1 = Constraint(rule= rule_c1)


def rule_c2(m, i):
    return m.x[i] <= gens_id[i].pmax
m.C2 = Constraint(m.i, rule= rule_c2)


def rule_of(m):
    return sum(i*m.x[i] for i in m.i)
m.of = Objective(rule=rule_of, sense=minimize)
instance = m.create_instance()
resulte = opt.solve(instance)

for i in instance.i:
    print(i, value(instance.x[i]))




