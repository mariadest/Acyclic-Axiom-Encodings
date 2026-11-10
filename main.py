from problem import base_vars, derived_vars, axioms, layer

from dd.autoref import BDD

"""
IDEA:
1. set up formula ONLY with axioms in the first layer 
    (ignoring derived variables that appear in higher layers)
2. set up formula with axioms in second layer 
    (derived variables from first layer are replaced by their primary representation; 
    we ignore derived variables in higher layers)
3. repeat until all layers are done 
"""

bdd = BDD()
# used to store the primary representations we already know
# we store positive and negative values (if needed) separately
# e.g. we have "a" and "not_a" as two separate entries
prim_reps = {}  

for i in range (len(layer)):
    # derived vars & axioms in the layer we want to look at 
    current_derived_vars = layer[i]
    current_axioms = []
    for a in axioms:
        if a["head"] in current_derived_vars:
            current_axioms.append(a)


    # replace body of axioms with prim rep we already have
    for a in current_axioms:
        new_body = []
        for q in a["body"]:
            if q in prim_reps:
                new_body.append(f"({bdd.to_expr(prim_reps[q])})")
            else:
                new_body.append(q)
        a["body"] = new_body
    

    all_vars = base_vars | current_derived_vars

    # declare variables
    for v in all_vars:
        bdd.declare(v)

    for u in all_vars:  # dep variables
        for v in all_vars: 
            bdd.declare(f"dep_{u}_{v}")
            bdd.declare(f"dep_{v}_{u}")

    for a in current_axioms:    # ws variables
        bdd.declare(a["id"])
        bdd.declare(f"ws_{a["id"]}_{a["head"]}")

    clauses = []
    # 12
    # we either DON'T have d included or an axiom justifies it
    for d in current_derived_vars:
        tmp = [f"~{d}"] # collects all axioms which can have d as head 
        for a in axioms:
            if a["head"] == d:
                tmp.append(f"ws_{a["id"]}_{d}")

        clauses.append(" | ".join(tmp))

    # 13
    # we have axiom 'a' which has 'q' in its body and 'd' as head (p in paper)
    # either 'a' does NOT justify 'd' or or 'd' depends on q
    for d in current_derived_vars:
        for a in current_axioms:
            if d == a["head"]:
                for q in a["body"]: 
                    if q in current_derived_vars:
                        clauses.append(f"~ws_{a["id"]}_{d} | dep_{d}_{q}")

    # 14
    # we have axiom 'a' with head 'p'
    # either 'a' does not justify 'p' or we have 'a'
    for a in current_axioms:
        clauses.append(f"~ws_{a["id"]}_{a["head"]} | {a["id"]}")

    # 15 
    # we have axiom 'a' which has 'q' in its body
    # either we don't have 'a' or we have 'q' 
    for a in current_axioms:
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

    for d in current_derived_vars:
        rest_vars = [v for v in current_derived_vars if v != d]
        F_d = bdd.exist(rest_vars, F_without_aux)
        result = bdd.let({d: True}, F_d)
        prim_reps[d] = result
        prim_reps[f"not_{d}"] = ~result



for d, result in prim_reps.items():
    print(d + ": " + bdd.to_expr(result))