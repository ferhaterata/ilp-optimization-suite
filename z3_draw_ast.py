import z3
from typing import Dict, List
import graphviz

import logging
l = logging.getLogger('infer')
l.setLevel(logging.DEBUG)
l.handlers.clear()
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
formatter = logging.Formatter('{levelname:<8s} | {module:<11s} | {name} | {message}', style='{')
sh.setFormatter(formatter)
l.addHandler(sh)


def draw_ast(fml: z3.ExprRef):
    graph = graphviz.Digraph('G', filename='ast.gv',
                             edge_attr={
                                 'fontname': "Helvetica,Arial,sans-serif",
                                 'color': 'black',
                                 'style': 'filled'},
                             graph_attr={
                                 'fontname': "Helvetica,Arial,sans-serif",
                                 'fixedsize': 'false',
                                 'bgcolor': 'transparent'},
                             node_attr={
                                 'fontname': "Helvetica,Arial,sans-serif",
                                 'fontsize': '12',
                                 'fixedsize': 'false',
                                 'margin': '0.01',
                                 'shape': 'ellipse',
                                 'color': 'black',
                                 'style': 'filled',
                                 'fillcolor': 'lightsteelblue3'})
    counter = 0

    def id():
        nonlocal counter
        counter += 1
        return str(counter)

    def visit(e: z3.ExprRef):
        if z3.is_app(e):

            if z3.is_false(e):  # Z3_OP_TRUE:
                return True

            if z3.is_true(e):  # Z3_OP_FALSE:
                return False

            if z3.is_eq(e):
                top = id()
                graph.node(top, label="=")
                left = visit(e.arg(0))
                graph.edge(top, left[0])
                right = visit(e.arg(1))
                graph.edge(top, right[0])
                return top

            if z3.is_distinct(e):
                top = id()
                graph.node(top, label="distinct")
                args = [visit(arg) for arg in e.children()]
                for arg in args:
                    graph.edge(top, arg[0])
                return top

            if e.decl().kind() == z3.Z3_OP_ITE:
                top = id()
                graph.node(top, label="ite")
                left = visit(e.arg(0))
                graph.edge(top, left, label="cond")
                middle = visit(e.arg(1))
                graph.edge(top, middle, label="then")
                right = visit(e.arg(2))
                graph.edge(top, right, label="else")
                return top

            # z3.Z3_OP_AND
            if z3.is_and(e):
                top = id()
                graph.node(top, label="and")
                args = [visit(arg) for arg in e.children()]
                for arg in args:
                    graph.edge(top, arg[0])
                return top

            # z3.Z3_OP_OR:
            if z3.is_or(e):  
                top = id()
                graph.node(top, label="or")
                args = [visit(arg) for arg in e.children()]
                for arg in args:
                    graph.edge(top, arg[0])
                return top

            # z3.Z3_OP_IFF = 263
            # z3.Z3_OP_XOR = 264

            # z3.Z3_OP_NOT:
            if z3.is_not(e):  
                top = id()
                graph.node(top, label="not")
                arg = visit(e.arg(0))
                graph.edge(top, arg[0])
                return top

            # z3.Z3_OP_IMPLIES:
            if z3.is_implies(e):  
                top = id()
                graph.node(top, label="=>")
                left = visit(e.arg(0))
                graph.edge(top, left[0])
                right = visit(e.arg(1))
                graph.edge(top, right[0])
                return top

            # z3.Z3_OP_OEQ = 267
            # z3.Z3_OP_ANUM = 512
            # z3.Z3_OP_AGNUM = 513

            # z3.Z3_OP_LE = 514
            if e.decl().kind() == z3.Z3_OP_LE:
                top = id()
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                graph.node(top, label="<=")
                graph.edge(top, left[0])
                graph.edge(top, right[0])
                return top

            # z3.Z3_OP_GE = 515
            if e.decl().kind() == z3.Z3_OP_GE:
                top = id()
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                graph.node(top, label=">=")
                graph.edge(top, left[0])
                graph.edge(top, right[0])
                return top

            # z3.Z3_OP_LT = 516
            if e.decl().kind() == z3.Z3_OP_LT:
                top = id()
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                graph.node(top, label="<")
                graph.edge(top, left[0])
                graph.edge(top, right[0])
                return top

            # z3.Z3_OP_GT = 517
            if e.decl().kind() == z3.Z3_OP_GT:
                top = id()
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                graph.node(top, label=">")
                graph.edge(top, left[0])
                graph.edge(top, right[0])
                return top

            # z3.Z3_OP_ADD = 518
            if e.decl().kind() == z3.Z3_OP_ADD:
                top = id()
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                graph.node(top, label="+")
                graph.edge(top, left[0])
                graph.edge(top, right[0])
                return top

            # z3.Z3_OP_SUB = 519
            if e.decl().kind() == z3.Z3_OP_SUB:
                top = id()
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                graph.node(top, label="-")
                graph.edge(top, left[0])
                graph.edge(top, right[0])
                return top

            # z3.Z3_OP_UMINUS = 520
            if e.decl().kind() == z3.Z3_OP_UMINUS:
                top = id()
                graph.node(top, label="-")
                arg = visit(e.arg(0))
                graph.edge(top, arg[0])
                return top

            # z3.Z3_OP_MUL = 521
            if e.decl().kind() == z3.Z3_OP_MUL:
                top = id()
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                graph.node(top, label="*")
                graph.edge(top, left[0])
                graph.edge(top, right[0])
                return top

            # z3.Z3_OP_DIV = 522
            if e.decl().kind() == z3.Z3_OP_DIV:
                top = id()
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                graph.node(top, label="/")
                graph.edge(top, left[0])
                graph.edge(top, right[0])
                return top

            # z3.Z3_OP_IDIV = 523
            if e.decl().kind() == z3.Z3_OP_IDIV:
                top = id()
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                graph.node(top, label="//")
                graph.edge(top, left[0])
                graph.edge(top, right[0])
                return top

            # z3.Z3_OP_REM = 524
            if e.decl().kind() == z3.Z3_OP_REM:
                top = id()
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                graph.node(top, label="%")
                graph.edge(top, left[0])
                graph.edge(top, right[0])
                return top

            # z3.Z3_OP_MOD = 525
            if e.decl().kind() == z3.Z3_OP_MOD:
                top = id()
                left = visit(e.arg(0))
                right = visit(e.arg(1))
                graph.node(top, label="mod")
                graph.edge(top, left[0])
                graph.edge(top, right[0])
                return top

            if z3.is_const(e) and e.decl().kind() == z3.Z3_OP_UNINTERPRETED:
                top = id()
                graph.node(top, label=f"{e.decl().name()}", shape="circle", fillcolor="steelblue1")
                return top

            if z3.is_int_value(e):
                top = id()
                graph.node(top, label=f"{e.as_long()}", shape="circle", fillcolor="steelblue1")
                return top

            if z3.is_app(e):
                raise Exception("Unknown function: {}".format(str(e)))

            else:
                raise Exception("Unknown operator: {}".format(e.decl().kind()))

    visit(fml)
    graph.view()

    return graph


x, y, z = z3.Ints('x y z')
# graph = draw_ast(z == x * y * z) 
# graph = draw_ast(z == x * y + z) 
graph = draw_ast(z == x * y + z + 1) 
