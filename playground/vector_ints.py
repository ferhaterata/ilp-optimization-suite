from z3 import *

X = IntVector('x', 5)
s = Solver()

for i in range(5):
    s.add(X[i] >= 0)
    s.add(1505 == 215 * X[0] + 275 * X[1] + 335 * X[2] + 420 * X[3] + 580 * X[4])

while s.check() == sat:
    model = s.model()
    print(model)
    s.add(Or([X[i] != model[X[i]] for i in range(5)]))
