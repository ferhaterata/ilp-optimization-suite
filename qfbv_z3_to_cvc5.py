import z3
import cvc5.pythonic as cvc5

def z3_to_cvc5(fml: z3.ExprRef) -> cvc5.ExprRef:

    def find_constants(fml: z3.ExprRef):
        symbols = {}

        def visitor(e, seen):
            if e in seen:
                return
            seen[e] = True
            yield e
            if z3.is_app(e):
                for ch in e.children():
                    for e in visitor(ch, seen):
                        yield e
                return

        for e in visitor(fml, seen={}):
            if z3.is_const(e) and e.decl().kind() == z3.Z3_OP_UNINTERPRETED:
                # print("Variable", e)
                symbols[e.decl().name()] = cvc5.BitVec(e.decl().name(), e.size())

        return symbols


    def visit(e: z3.ExprRef):
        if z3.is_app(e):

            if z3.is_false(e):  # Z3_OP_TRUE:
                return True

            if z3.is_true(e):  # Z3_OP_FALSE:
                return False

            if z3.is_eq(e):
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return left == right

            if z3.is_distinct(e):
                args = [visit(arg) for arg in e.children()]
                return cvc5.Distinct(args)

            if e.decl().kind() == z3.Z3_OP_ITE:
                a = visit(e.arg(0))
                b = visit(e.arg(1))
                c = visit(e.arg(2))
                return cvc5.If(a, b, c)

            if z3.is_and(e):  # z3.Z3_OP_AND
                args = [visit(arg) for arg in e.children()]
                return cvc5.And(args)

            if z3.is_or(e):  # z3.Z3_OP_OR:
                args = [visit(arg) for arg in e.children()]
                return cvc5.Or(args)

            #z3.Z3_OP_IFF = 263
            #z3.Z3_OP_XOR = 264

            if z3.is_not(e):  # z3.Z3_OP_NOT:
                arg = visit(e.arg(0))
                return cvc5.Not(arg)

            if z3.is_implies(e):  # z3.Z3_OP_IMPLIES:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return cvc5.Implies(left, right)

            #z3.Z3_OP_OEQ = 267
            #z3.Z3_OP_ANUM = 512
            #z3.Z3_OP_AGNUM = 513
            #z3.Z3_OP_LE = 514
            #z3.Z3_OP_GE = 515
            #z3.Z3_OP_LT = 516
            #z3.Z3_OP_GT = 517
            #z3.Z3_OP_ADD = 518
            #z3.Z3_OP_SUB = 519
            #z3.Z3_OP_UMINUS = 520
            #z3.Z3_OP_MUL = 521
            #z3.Z3_OP_DIV = 522
            #z3.Z3_OP_IDIV = 523
            #z3.Z3_OP_REM = 524
            #z3.Z3_OP_MOD = 525

            if e.decl().kind() == z3.Z3_OP_BNEG:
                arg = visit(e.arg(0))
                return -arg

            if e.decl().kind() == z3.Z3_OP_BADD:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return left + right

            if e.decl().kind() == z3.Z3_OP_BSUB:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return left - right

            if e.decl().kind() == z3.Z3_OP_BMUL:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return left * right

            if e.decl().kind() == z3.Z3_OP_BSDIV:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return cvc5.SDiv(left, right)

            if e.decl().kind() == z3.Z3_OP_BUDIV:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return cvc5.UDiv(left, right)

            if e.decl().kind() == z3.Z3_OP_BSREM:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return cvc5.SRem(left, right)

            if e.decl().kind() == z3.Z3_OP_BUREM:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return cvc5.URem(left, right)

            if e.decl().kind() == z3.Z3_OP_BSMOD:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return cvc5.SMod(left, right)

            if e.decl().kind() == z3.Z3_OP_ULEQ:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return cvc5.ULE(left, right)

            if e.decl().kind() == z3.Z3_OP_SLEQ:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return left <= right

            if e.decl().kind() == z3.Z3_OP_UGEQ:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return cvc5.UGE(left, right)

            if e.decl().kind() == z3.Z3_OP_SGEQ:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return left >= right

            if e.decl().kind() == z3.Z3_OP_ULT:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return cvc5.ULT(left, right)

            if e.decl().kind() == z3.Z3_OP_SLT:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return left < right

            if e.decl().kind() == z3.Z3_OP_UGT:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return cvc5.UGT(left, right)

            if e.decl().kind() == z3.Z3_OP_SGT:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return left > right

            if e.decl().kind() == z3.Z3_OP_BAND:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return left & right

            if e.decl().kind() == z3.Z3_OP_BOR:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return left | right

            if e.decl().kind() == z3.Z3_OP_BNOT:
                arg = visit(e.arg(0))
                return ~arg

            if e.decl().kind() == z3.Z3_OP_BXOR:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return left ^ right

            if e.decl().kind() == z3.Z3_OP_BXNOR:
                raise Exception("Unknown operator:z3.Z3_OP_BXNOR")

            if e.decl().kind() == z3.Z3_OP_BNAND:
                raise Exception("Unknown operator:z3.Z3_OP_BNAND")

            if e.decl().kind() == z3.Z3_OP_BNOR:
                raise Exception("Unknown operator:z3.Z3_OP_BNOR")

            if e.decl().kind() == z3.Z3_OP_BXNOR:
                raise Exception("Unknown operator:z3.Z3_OP_BXNOR")

            if e.decl().kind() == z3.Z3_OP_CONCAT:
                args = [visit(arg) for arg in e.children()]
                return cvc5.Concat(args)

            if e.decl().kind() == z3.Z3_OP_SIGN_EXT:
                n = e.params()[0]
                a = visit(e.arg(0))
                return cvc5.SignExt(n, a)

            if e.decl().kind() == z3.Z3_OP_ZERO_EXT:
                n = e.params()[0]
                a = visit(e.arg(0))
                return cvc5.ZeroExt(n, a)

            if e.decl().kind() == z3.Z3_OP_EXTRACT:
                a = visit(e.arg(0))
                high = e.params()[0]
                low = e.params()[1]
                return cvc5.Extract(high, low, a)

            #z3.Z3_OP_REPEAT = 1060
            #z3.Z3_OP_BREDOR = 1061
            #z3.Z3_OP_BREDAND = 1062
            #z3.Z3_OP_BCOMP = 1063

            if e.decl().kind() == z3.Z3_OP_BSHL:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return left << right

            if e.decl().kind() == z3.Z3_OP_BLSHR:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return cvc5.LShR(left, right)

            if e.decl().kind() == z3.Z3_OP_BASHR:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return left >> right

            if e.decl().kind() == z3.Z3_OP_ROTATE_LEFT:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return cvc5.RotateLeft(left, right)

            if e.decl().kind() == z3.Z3_OP_ROTATE_RIGHT:
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                return cvc5.RotateRight(left, right)

            if z3.is_const(e) and e.decl().kind() == z3.Z3_OP_UNINTERPRETED:
                return symbols[e.decl().name()]

            if z3.is_bv_value(e):
                return cvc5.BitVecVal(e.as_long(), e.size())

            if z3.is_app(e):
                raise Exception("Unknown function: {}".format(str(e)))

            else:
                raise Exception("Unknown operator: {}".format(e.decl().kind()))

    symbols = find_constants(fml)
    return visit(fml)

if __name__ == "__main__":
    a1 = z3.BitVec('a!1', 32)
    a2 = z3.BitVec('a!2', 8)
    eax = z3.BitVec('eax', 32)
    fml_z3 = (z3.LShR(a1, z3.Concat(z3.BitVecVal(0, 24), a2)) ^ 1 ) & 1  == eax
    print(fml_z3.sexpr())
    fml_cvc5 = z3_to_cvc5(fml_z3)
    solver = cvc5.Solver()
    solver.add(fml_cvc5)
    result = solver.check()
    if result == cvc5.sat:
        print("sat")
        print(solver.model())
    elif result == cvc5.unsat:
        print("unsat")
    else:
        print("unknown")
