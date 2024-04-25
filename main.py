import copy
import itertools
from pysat.solvers import Glucose3
from pysat.formula import CNF

def read_file(filename):
  grid = []

  with open("input.txt", "r") as file:
    for line in file:
      row = [int(x.strip()) if x.strip() != '_' else 0 for x in line.split(',')]
      grid.append(row)

  return grid

def get_index(grid):
  blank = []
  index = []
  for i in range(len(grid)):
    for j in range(len(grid[0])):
      if grid[i][j] == 0:
        blank.append((i, j))
      else:
        index.append((i, j))

  return blank, index

def get_neighbor(x, y, indexes, grid):
  neighbor = [(1,1), (1,0), (1,-1), (0,1), (0,-1), (-1,1), (-1,0), (-1,-1)]
  literals = []
  n = len(grid)
  m = len(grid[0])

  for dx, dy in neighbor:
    newx = x + dx
    newy = y + dy
    if (newx, newy) not in indexes and 0 <= newx and newx < n and 0 <= newy and newy < m:
      literals.append((newx, newy))
  
  return literals

def solve(grid, map):

  def at_least_one(literals):
    clauses = [grid[e1[0]][e1[1]] for e1 in literals]
    return clauses
  
  def at_most_one(literals):
    clauses = [[-grid[e1[0]][e1[1]], -grid[e2[0]][e2[1]]] for e1, e2 in itertools.combinations(literals, 2)]
    return clauses
  
  def at_most_two(literals):
    clauses = [[-grid[e1[0]][e1[1]], -grid[e2[0]][e2[1]], -grid[e3[0]][e3[1]]] for e1, e2, e3 in itertools.combinations(literals, 3)]
    return clauses

  def at_most_three(literals):
    clauses = [[-grid[e1[0]][e1[1]], -grid[e2[0]][e2[1]], -grid[e3[0]][e3[1]], -grid[e4[0]][e4[1]]] for e1, e2, e3, e4 in itertools.combinations(literals, 4)]
    return clauses

  def at_most_four(literals):
    clauses = [[-grid[e1[0]][e1[1]], -grid[e2[0]][e2[1]], -grid[e3[0]][e3[1]], -grid[e4[0]][e4[1]], -grid[e5[0]][e5[1]]] for e1, e2, e3, e4, e5 in itertools.combinations(literals, 5)]
    return clauses

  def at_most_five(literals):
    clauses = [[-grid[e1[0]][e1[1]], -grid[e2[0]][e2[1]], -grid[e3[0]][e3[1]], -grid[e4[0]][e4[1]], -grid[e5[0]][e5[1]], -grid[e6[0]][e6[1]]] for e1, e2, e3, e4, e5, e6 in itertools.combinations(literals, 6)]
    return clauses

  def at_most_six(literals):
    clauses = [[-grid[e1[0]][e1[1]], -grid[e2[0]][e2[1]], -grid[e3[0]][e3[1]], -grid[e4[0]][e4[1]], -grid[e5[0]][e5[1]], -grid[e6[0]][e6[1]], -grid[e7[0]][e7[1]]] for e1, e2, e3, e4, e5, e6, e7 in itertools.combinations(literals, 7)]
    return clauses

  def at_most_seven(literals):
    clauses = [[-grid[e1[0]][e1[1]], -grid[e2[0]][e2[1]], -grid[e3[0]][e3[1]], -grid[e4[0]][e4[1]], -grid[e5[0]][e5[1]], -grid[e6[0]][e6[1]], -grid[e7[0]][e7[1]], -grid[e8[0]][e8[1]]] for e1, e2, e3, e4, e5, e6, e7, e8 in itertools.combinations(literals, 8)]
    return clauses
  
  def exact_one(literals):
    if len(literals) == 1:
      return [[grid[literals[0][0]][literals[0][1]]]]
    else:
      return [item for sublist in [[at_least_one(literals)],at_most_one(literals)] for item in sublist]
  
  def exact_eight(literals):
    return [[grid[e[0]][e[1]]] for e in literals]
  
  def exact_seven(literals, a):
    if a == 0:
      return [[e] for sub in [[abs(num) for num in sublist] for sublist in at_most_six(literals)] for e in sub]
    res = [[[abs(num) for num in sublist] for sublist in provide_arr(a, literals)], at_most_seven(literals)]
    return [item for sublist in res for item in sublist]
  
  def exact_six(literals, a):
    if a == 0:
      return [[e] for sub in [[abs(num) for num in sublist] for sublist in at_most_five(literals)] for e in sub]
    res = [[[abs(num) for num in sublist] for sublist in provide_arr(a, literals)], at_most_six(literals)]
    return [item for sublist in res for item in sublist]
  
  def exact_five(literals, a):
    if a == 0:
      return [[e] for sub in [[abs(num) for num in sublist] for sublist in at_most_four(literals)] for e in sub]
    res = [[[abs(num) for num in sublist] for sublist in provide_arr(a, literals)], at_most_five(literals)]
    return [item for sublist in res for item in sublist]
  
  def exact_four(literals, a):
    if a == 0:
      return [[e] for sub in [[abs(num) for num in sublist] for sublist in at_most_three(literals)] for e in sub]
    res = [[[abs(num) for num in sublist] for sublist in provide_arr(a, literals)], at_most_four(literals)]
    return [item for sublist in res for item in sublist]
  
  def exact_three(literals, a):
    if a == 0:
      return [[e] for sub in [[abs(num) for num in sublist] for sublist in at_most_two(literals)] for e in sub]
    res = [[[abs(num) for num in sublist] for sublist in provide_arr(a, literals)], at_most_three(literals)]
    return [item for sublist in res for item in sublist]
  
  def exact_two(literals, a):
    if a == 0:
      return [[e] for sub in [[abs(num) for num in sublist] for sublist in at_most_one(literals)] for e in sub]
    res = [[[abs(num) for num in sublist] for sublist in provide_arr(a, literals)], at_most_two(literals)]
    return [item for sublist in res for item in sublist]
  
  def provide_arr(num, literals):
    res = []
    if num == 1:
      res = at_most_one(literals)
    elif num == 2:
      res = at_most_two(literals)
    elif num == 3:
      res = at_most_three(literals)
    elif num == 4:
      res = at_most_four(literals)
    elif num == 5:
      res = at_most_five(literals)
    elif num == 6:
      res = at_most_six(literals)
    elif num == 7:
      res = at_most_seven(literals)


    return res
  
  
  blanks, indexes = get_index(map)
  # literals = get_neighbor(0, 0, indexes, map)
  # clause = exact_three(literals, 0)

  clause = []
  for index in indexes:
    literals = get_neighbor(index[0], index[1], indexes, map)
    num = map[index[0]][index[1]]
    a = len(literals) - num
    res = []
    print(a)
    if num == 1:
      res = exact_one(literals)
    elif num == 2:
      res = exact_two(literals, a)
    elif num == 3:
      res = exact_three(literals, a)
    elif num == 4:
      res = exact_four(literals, a)
    elif num == 5:
      res = exact_five(literals, a)
    elif num == 6:
      res = exact_six(literals, a)
    elif num == 7:
      res = exact_seven(literals, a)
    elif num == 8:
      res = exact_eight(literals, a)

    for r in res:
      clause.append(r)


  return clause


def main():
  grid = read_file("input.txt")
  grid_copy = copy.deepcopy(grid)
  cnf = CNF()
  g = Glucose3()


  count = 1
  for i in range(len(grid_copy)):
    for j in range(len(grid_copy[0])):
      if grid_copy[i][j] == 0:
        grid_copy[i][j] = count
        count += 1

  
  blanks, indexes = get_index(grid)

  # literals = get_neighbor(0, 0, indexes, grid)
  # cnf.clauses = [[-grid_copy[e1[0]][e1[1]], -grid_copy[e2[0]][e2[1]]] for e1, e2 in itertools.combinations(literals, 2)]
  # cnf.clauses.append([4, 3, 1])
  # print(cnf.clauses)
  # g.append_formula(cnf.clauses)
  cnf.clauses = solve(grid_copy, grid)

  print(cnf.clauses)
  g.append_formula(cnf.clauses)
  print(g.solve())
  print(g.get_model())
  result = g.get_model()

  for b in blanks:
    if result[grid_copy[b[0]][b[1]] - 1] > 0:
      grid_copy[b[0]][b[1]] = 'G'
    else:
      grid_copy[b[0]][b[1]] = 'T'

  for row in grid_copy:
    print(row)

  # Define the lists

  with open('output.txt', 'w') as file:
    for row in grid_copy:
      file.write(', '.join(map(str, row)) + '\n')


if __name__ == '__main__':
  main()