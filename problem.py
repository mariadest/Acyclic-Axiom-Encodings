base_vars = {"x"}
derived_vars = {"a", "b"}

axioms = [
    {"id": "axiom1", "body": ["x"], "head": "a"},
    {"id": "axiom2", "body": ["a"], "head": "b"},
    {"id": "axiom3", "body": ["b"], "head": "a"},
]