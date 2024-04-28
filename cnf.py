def dpll_satisfiable(formula):
    valuation = {}
    if dpll(formula, valuation):
        return valuation
    else:
        return None

def dpll(formula, valuation):
    if not formula:
        return True
    if [] in formula:
        return False
    
    unit_clauses = [clause[0] for clause in formula if len(clause) == 1]
    while unit_clauses:
        literal = unit_clauses[0]
        unit_clauses = unit_clauses[1:]
        if literal < 0:
            valuation[-literal] = 0
        else:
            valuation[literal] = 1
        formula = simplify_formula(formula, literal)
    
    pure_literals = find_pure_literals(formula)
    for literal in pure_literals:
        valuation[abs(literal)] = 1
        formula = simplify_formula(formula, literal)
    
    if not formula:
        return True
    
    variable = formula[0][0]
    formula_copy = formula[:]
    formula_copy.append([variable])
    valuation_copy = valuation.copy()
    if dpll(formula_copy, valuation_copy):
        valuation.update(valuation_copy)
        return True
    
    formula_copy = formula[:]
    formula_copy.append([-variable])
    valuation_copy = valuation.copy()
    if dpll(formula_copy, valuation_copy):
        valuation.update(valuation_copy)
        return True
    
    return False

def simplify_formula(formula, literal):
    simplified_formula = [clause for clause in formula if literal not in clause and -literal not in clause]
    simplified_formula = [[l for l in clause if l != -literal] for clause in simplified_formula]
    return simplified_formula

def find_pure_literals(formula):
    literals = [literal for clause in formula for literal in clause]
    pure_literals = []
    for literal in literals:
        if -literal not in literals:
            pure_literals.append(literal)
    return pure_literals

# Example usage:
formula = [[4], [3], [1], [6, 5, 4], [6, 5, 2], [6, 5, 1], [6, 4, 2], [6, 4, 1], [6, 2, 1], [5, 4, 2], [5, 4, 1], [5, 2, 1], [4, 2, 1], [-6, -5, -4, -2], [-6, -5, -4, -1], [-6, -5, -2, -1], [-6, -4, -2, -1], [-5, -4, -2, -1], [7], [4], [3], [8, 7, 6], [8, 7, 5], [8, 7, 4], [8, 6, 5], [8, 6, 4], [8, 5, 4], [7, 6, 5], [7, 6, 4], [7, 5, 4], [6, 5, 4], [-8, -7, -6, -5], [-8, -7, -6, -4], [-8, -7, -5, -4], [-8, -6, -5, -4], [-7, -6, -5, -4]]
valuation = dpll_satisfiable(formula)
print(valuation)
