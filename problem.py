base_vars = {"not_x", "y"}
derived_vars = {"a", "b", "c", "not_a", "not_b"}
layer = [{"a", "b"}, {"c"}]

axioms = [
    {"id": "axiom1", "body": ["b"], "head": "a"},
    {"id": "axiom2", "body": ["not_x"], "head": "b"},
    {"id": "axiom3", "body": ["y"], "head": "b"},
    {"id": "axiom4", "body": ["not_a", "not_b"], "head": "c"},
]