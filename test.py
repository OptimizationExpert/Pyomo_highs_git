

from pyomo.environ import *
from pyomo.contrib.appsi.solvers.highs import Highs


opt = Highs()

m = ConcreteModel()
m.x = Var(bounds=(-10, 10))
m.y = Var()

m.p1 = Param(mutable=True)
m.p2 = Param(mutable=True)

m.obj = Objective(expr=m.y)
m.c1 = Constraint(expr=m.y >= m.x + m.p1)
m.c2 = Constraint(expr=m.y >= -m.x + m.p2)
m.p1.value = 1
m.p2.value = 1

opt = Highs()
res = opt.solve(m)
print(m.x.value, m.y.value)