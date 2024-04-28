def dpll_solver(formula, assignments):
    if not formula:
        return True, assignments  # All clauses satisfied
    if any(len(clause) == 0 for clause in formula):
        return False, None  # Conflict encountered
    
    # Choose a variable to assign
    variable = choose_variable(formula)
    
    # Try assigning true
    result, assignments_true = dpll_solver(unit_propagate(formula, variable), assignments + [(variable, True)])
    if result:
        return True, assignments_true
        
    # Try assigning false
    result, assignments_false = dpll_solver(unit_propagate(formula, -variable), assignments + [(variable, False)])
    return result, assignments_false

def choose_variable(formula):
    # Choose the next unassigned variable
    for clause in formula:
        for literal in clause:
            if abs(literal) not in assigned_variables:
                return abs(literal)
    return None  # All variables assigned

def unit_propagate(formula, unit_literal):
    propagated_formula = [clause for clause in formula if unit_literal not in clause]
    propagated_formula = [[literal for literal in clause if literal != -unit_literal] for clause in propagated_formula]
    return propagated_formula

# Example usage
formula = [[4], [3], [1], [6, 5, 4], [6, 5, 2], [6, 5, 1], [6, 4, 2], [6, 4, 1], [6, 2, 1], [5, 4, 2], [5, 4, 1], [5, 2, 1], [4, 2, 1], [-6, -5, -4, -2], [-6, -5, -4, -1], [-6, -5, -2, -1], [-6, -4, -2, -1], [-5, -4, -2, -1], [7], [4], [3], [8, 7, 6, 5], [8, 7, 6, 4], [8, 7, 5, 4], [8, 6, 5, 4], [7, 6, 5, 4], [-8, -7, -6], [-8, -7, -5], [-8, -7, -4], [-8, -6, -5], [-8, -6, -4], [-8, -5, -4], [-7, -6, -5], [-7, -6, -4], [-7, -5, -4], [-6, -5, -4]]
assigned_variables = set()
result, assignments = dpll_solver(formula, [])
if result:
    print("Satisfiable")
    print("Variable Assignments:")
    for var, value in assignments:
        print(f"Variable {var} is assigned {'True' if value else 'False'}")
else:
    print("Unsatisfiable")
