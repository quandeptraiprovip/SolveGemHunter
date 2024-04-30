from pysat.formula import CNF
from pysat.solvers import Solver
import numpy as np
from itertools import combinations

def read_matrix_from_file(filename):
    matrix = np.loadtxt(filename, delimiter=",", dtype=int)
    return matrix

def save_matrix_to_file(matrix, solution, filename):
    rows, cols = matrix.shape
    mine = []
    for i in solution:
        if i > 0:
            mine.append(i)
    
    new_matrix = matrix.astype(str)
            
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 0 and solution[i * cols + j] < 0:
                new_matrix[i][j] = 'G'
            if variable((i, j), cols) in mine:
                new_matrix[i][j] = 'T'

    np.savetxt(filename, new_matrix, delimiter=',', fmt='%s')
    

def variable(cell, cols):
    i = int(cell[0])
    j = int(cell[1])
    return (i * cols) + j + 1

def get_unassigned_neighbor(matrix, cell):
    rows, cols = matrix.shape
    row, col = cell
    neighbors = []
    
    for i in [row - 1, row, row + 1]:
        if i < 0 or i >= rows:  # Kiểm tra nếu chỉ số hàng vượt ra ngoài biên ma trận
            continue
        for j in [col - 1, col, col + 1]:
            if j < 0 or j >= cols or (i == row and j == col):  # Kiểm tra nếu chỉ số cột vượt ra ngoài biên ma trận hoặc là ô được chỉ định
                continue
            if matrix[i][j] == 0:  # Kiểm tra nếu ô lân cận chưa được gán giá trị
                neighbors.append((i, j))
                
    return neighbors


def generate_cnf(matrix):
    clauses = []
    
    rows, cols = matrix.shape

    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value > 0:
                clauses.append([-int(variable((i, j), cols))])
                neighbors = get_unassigned_neighbor(matrix, (i, j))
                
                if len(neighbors) == value:
                    for cell in neighbors:
                        clauses.append([int(variable(cell, cols))])
                
                elif len(neighbors) > value:
                    # temp = []
                    
                    # for i in range(len(neighbors)):
                    #     temp.append(int(variable(neighbors[i], cols)))
                        
                    # clauses.append(temp)
                    
                    negative_combinations = combinations(neighbors, value+1)
                    for clause in negative_combinations:
                        clauses.append([-int(variable(liter, cols))
                            for liter in clause])
                            
                    positive_combinations = combinations(neighbors, len(neighbors)-value+1)
                    for clause in positive_combinations:
                        clauses.append([int(variable(liter, cols))
                               for liter in clause])

    return clauses
    #return positive_combinations



def solve_by_pysat(clauses):
    cnf = CNF(from_clauses=clauses)
    with Solver(bootstrap_with=cnf) as solver:
        satisfy = solver.solve()

        if satisfy:
            solution = solver.get_model()
            return solution
        else:
            return None
    
        
if __name__ == '__main__':
    matrix = read_matrix_from_file('input3x3.txt')
    neighbors = get_unassigned_neighbor(matrix, (0,1))
    print(neighbors)
    clauses = generate_cnf(matrix)
    print (clauses)
    #print(type(clauses))
    solution = solve_by_pysat(clauses)
    print(solution)
    save_matrix_to_file(matrix, solution, 'output3x3.txt')
    