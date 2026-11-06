from problem import base_vars, derived_vars, axioms

from dd.autoref import BDD

bdd = BDD()

all_vars = base_vars | derived_vars

# declare variables
for v in all_vars:
    bdd.declare(v)

for u in all_vars:  # dep variables
    for v in all_vars: 
        bdd.declare(f"dep_{u}_{v}")
        bdd.declare(f"dep_{v}_{u}")

for a in axioms:    # ws variables
    bdd.declare(a["id"])
    bdd.declare(f"ws_{a["id"]}_{a["head"]}")

clauses = []
# 12
# we either DON'T have d included or an axiom justifies it
for d in derived_vars:
    tmp = [f"~{d}"] # collects all axioms which can have d as head 
    for a in axioms:
        if a["head"] == d:
            tmp.append(f"ws_{a["id"]}_{d}")

    clauses.append(" | ".join(tmp))

# 13
# we have axiom 'a' which has 'q' in its body and 'd' as head (p in paper)
# either 'a' does NOT justify 'd' or or 'd' depends on q
for d in derived_vars:
    for a in axioms:
        if d == a["head"]:
            for q in a["body"]: 
                clauses.append(f"~ws_{a["id"]}_{d} | dep_{d}_{q}")

# 14
# we have axiom 'a' with head 'p'
# either 'a' does not justify 'p' or we have 'a'
for a in axioms:
    clauses.append(f"~ws_{a["id"]}_{a["head"]} | {a["id"]}")

# 15 
# we have axiom 'a' which has 'q' in its body
# either we don't have 'a' or we have 'q' 
for a in axioms:
    for q in a["body"]:
        clauses.append(f"~{a["id"]} | {q}")

# ensuring acyclictiy with transitive closure
# add transitive closure 
for x in all_vars:
    for y in all_vars:
        for z in all_vars:
            clauses.append(f"~dep_{y}_{x} | ~dep_{z}_{y} | dep_{z}_{x}")

# forbid all dependencies of length 1 and 2 (i.e. a_a as well as a_b b_a)
for v in all_vars:
    clauses.append(f"~dep_{v}_{v}")

# add everything together 
F = bdd.true
for clause in clauses:
    F = F & bdd.add_expr(clause)

# quantify out auxiliary vars
aux_vars = [v for v in bdd.vars if v not in all_vars]
F_without_aux = bdd.exist(aux_vars, F)

# go through all derived vars and compute primary representation
# we need to set derived var 'd' we want to compute primary rep of as goal and then 
# quantify out all other derived vars 
prim_reps = []
for d in derived_vars:
    rest_vars = [v for v in derived_vars if v != d]
    F_d = bdd.exist(rest_vars, F_without_aux)
    result = bdd.let({d: True}, F_d)
    prim_reps.append([d, result])

for d, result in prim_reps:
    print(d + ": " + bdd.to_expr(result))