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
assigned_variables = set()

