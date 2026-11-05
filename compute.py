from problem import base_vars, derived_vars, axioms

from dd.autoref import BDD

bdd = BDD()

# declare variables
for v in base_vars:
    bdd.declare(v)

for d in derived_vars:
    bdd.declare(d)

for u in base_vars | derived_vars:  # dep variables
    for v in base_vars | derived_vars: 
        bdd.declare(f"dep_{u}_{v}")
        bdd.declare(f"dep_{v}_{u}")

for a in axioms:    # ws variables
    bdd.declare(a["id"])
    bdd.declare(f"ws_{a["id"]}_{a["head"]}")
