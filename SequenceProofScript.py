
from sympy import symbols, solve, Eq

# Define variables for each type of piece and their count
x1, x2, x3, x4, x5, x6, x7, x8 = symbols('x1 x2 x3 x4 x5 x6 x7 x8', integer=True)

# Equation representing total length of the sequence using pieces
total_length_equation = Eq(4*x1 + 3*x2 + 3*x3 + 3*x4 + 2*x5 + 2*x6 + 2*x7 + 1*x8, 576)

# Attempt to solve the equation for non-negative integer solutions with practical constraints
def find_feasible_solution(max_single_piece_usage):
    solutions = []
    for val in range(100):  # Check different values to find a solution
        result = solve(total_length_equation.subs(x8, val), (x1, x2, x3, x4, x5, x6, x7), dict=True)
        if result and all(res[x] >= 0 for x in (x1, x2, x3, x4, x5, x6, x7) for res in result):
            solutions.extend(result)
            if len(solutions) > 5:  # Limit the number of solutions for simplicity
                break
    return solutions

solutions = find_feasible_solution(50)  # Call the function with a maximum usage limit for the piece [4]

# Choose one solution and analyze the distribution of numbers
if solutions:
    chosen_solution = solutions[0]  # Choose the first feasible solution
    # Calculate the number of each digit (1, 2, 3, 4) in the sequence
    numbers_count = {
        1: 4*chosen_solution[x1] + 2*chosen_solution[x2] + 2*chosen_solution[x3] + 2*chosen_solution[x4] + chosen_solution[x5] + chosen_solution[x6],
        2: chosen_solution[x2] + chosen_solution[x3] + chosen_solution[x4] + 2*chosen_solution[x7],
        3: chosen_solution[x5] + chosen_solution[x6],
        4: chosen_solution[x8]
    }
    total_numbers = sum(numbers_count.values())
    frequency = {key: value / total_numbers for key, value in numbers_count.items()}
    
    print("Solution:", chosen_solution)
    print("Number Counts:", numbers_count)
    print("Frequencies:", frequency)
else:
    print("No feasible solution found within the constraints.")
