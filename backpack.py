from ortools.linear_solver import pywraplp
import math

'''
  Week 1 Puzzle - Survival backpack

  Description: In a long and dangerous hiking, you have to select items to bring
  with you in the backpack.
'''


def data_model():
    '''
      DATA MODEL:
      We created items individually regardless of category:
      items[0] is the small food item, with points[0] points and weights[0] weight.
      items[1] is the medium food item, with points[1] points and weights[1] weight.
      etc...
    '''
    data = {}

    data['points'] = [10, 20, 25, 10, 20, 25, 5, 15, 20, 5, 15, 20]
    data['weights'] = [5, 8, 12, 3, 5, 8, 5, 8, 12, 1, 2, 3]
    data['capacity'] = 25
    data['items'] = list(range(len(data['weights'])))
    data['items_per_category'] = 3

    return data


def main():
    # using the SCIP backend (mixed-integer programming)
    solver = pywraplp.Solver.CreateSolver('SCIP')
    data = data_model()

    '''
      Variables:
      - each x[i] is a boolean (0 or 1) where i is the item.
        e.g. If x[3] = 1 it means that item 3 (aka "small water") is in the backpack.
    '''
    x = {}
    for i in data['items']:
        x[i] = solver.IntVar(0, 1, 'x_%i' % (i))

    '''
      Constraints:
      - each item category must be in the backpack: (at least one every 3 items in the data['items'] array)
      - the total weight must be under 25kg.
    '''
    c = data['items_per_category']
    for i in range(int(len(data['items']) / c)):
        solver.Add(sum(x[j] for j in range(i*c, i*c+c)) == 1)
    solver.Add(sum(x[j] * data['weights'][j]
                   for j in data['items']) <= data['capacity'])

    '''
      Objective:
      the goal is to maximize the survival points of the backpack.
    '''
    objective = solver.Objective()
    for i in data['items']:
        objective.SetCoefficient(x[i], data['points'][i])
    objective.SetMaximization()

    '''
      Solve the problem and print the solution.
      To see if an item is in the backpack, just check if x[i].solution_value() > 0.
    '''
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print("Total survival points: ", objective.Value())
        print("Items in the backpack:")
        total_weight = 0
        for i in data['items']:
            if x[i].solution_value() > 0:
                print("Item", i, " - weight: ",
                      data['weights'][i], " - points: ", data['points'][i])
                total_weight += data['weights'][i]
        print("Total weight: ", total_weight, "kg")


if __name__ == "__main__":
    main()
