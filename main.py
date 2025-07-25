#  ___________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright (c) 2008-2025
#  National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________

import pyomo.environ as pyo
from pyomo.contrib.appsi.solvers.highs import Highs


opt = Highs()

m = pyo.ConcreteModel()
m.x = pyo.Var(bounds=(-10, 10))
m.y = pyo.Var()

m.p1 = pyo.Param(mutable=True)
m.p2 = pyo.Param(mutable=True)

m.obj = pyo.Objective(expr=m.y)
m.c1 = pyo.Constraint(expr=m.y >= m.x + m.p1)
m.c2 = pyo.Constraint(expr=m.y >= -m.x + m.p2)

m.p1.value = 1
m.p2.value = 1

opt = Highs()
res = opt.solve(m)
print(m.x.value, m.y.value)
