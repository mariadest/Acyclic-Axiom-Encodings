from dd.autoref import BDD

bdd = BDD()

bdd.declare('x', 'a', 'b', 
            'ws_1_a', 'ws_2_a', 'ws_3_a', 'ws_1_b', 'ws_2_b', 'ws_3_b', 'ws_1_x', 'ws_2_x', 'ws_3_x', 
            'dep_a_b', 'dep_b_a', 'dep_a_x', 'dep_x_a', 'dep_b_x', 'dep_x_b', 
            'dep_a_a', 'dep_b_b', 'dep_x_x', 'axiom_1', 'axiom_2', 'axiom_3')

# clauses for computing primary representation of derived variable 'a' (i.e. we have 'a' as goal)
clauses = [
    # (12)
    "~a | ws_1_a | ws_3_a",
    "~b | ws_2_b",

    # (13)
    "~ws_1_a | dep_a_x",
    "~ws_3_a | dep_a_b",
    "~ws_2_b | dep_b_a",

    # (14)
    "~ws_1_a | axiom_1",
    "~ws_3_a | axiom_3",
    "~ws_2_b | axiom_2",

    # (15)
    "~axiom_1 | x",
    "~axiom_3 | b",
    "~axiom_2 | a",

    # (16) goals (here the derived variable whos primary representation we want)
    "b",

    # (17)
    "~dep_a_x | ~dep_b_a | dep_b_x",
    "~dep_b_x | ~dep_a_b | dep_a_x",
    "~dep_b_a | ~dep_x_b | dep_x_a",
    "~dep_a_b | ~dep_x_a | dep_x_b",
    "~dep_x_a | ~dep_b_x | dep_b_a",
    "~dep_x_b | ~dep_a_x | dep_a_b",

    # forbidding self-cycles and cycles length two
    "~dep_a_a",
    "~dep_b_b",
    "~dep_x_x",
    "~dep_a_b | ~dep_b_a",
    "~dep_a_x | ~dep_x_a",
    "~dep_b_x | ~dep_x_b",
]


F = bdd.true
# add all clauses together
for clause in clauses:
    F = F & bdd.add_expr(clause)

# remove all variables except for 'x' and 'a'
to_remove = [v for v in bdd.vars if v not in {"x", "b"}]
tmp = bdd.exist(to_remove, F)
result = bdd.let({"b": True}, tmp)

print(bdd.to_expr(result))
print(bdd.to_expr(tmp))
models = list(bdd.pick_iter(tmp))
print(models)
