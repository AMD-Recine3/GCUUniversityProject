import math
from sympy import (symbols, Eq, solve, Function, S, Matrix, solveset, rsolve, mod_inverse)
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication, convert_xor, rationalize)

TRANSFORMS = standard_transformations + (implicit_multiplication, convert_xor, rationalize)


def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")

def get_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if math.isfinite(value):
                return value
            print("Please enter a finite number.")
        except ValueError:
            print("Please enter a number.")

def parse_side(text, local_dict=None):
    return parse_expr(text, transformations=TRANSFORMS, local_dict=local_dict)

def check_trivial(statement):
    if statement == True:
        raise ValueError("that is true for every value, so there is nothing to solve")
    if statement == False:
        raise ValueError("that is never true, so there is no solution")
    return statement

def parse_equation(text, local_dict=None):
    text = text.replace("==", "=")
    if text.count("=") != 1:
        raise ValueError("enter exactly one '=' sign")
    lhs, rhs = text.split("=")
    return check_trivial(Eq(parse_side(lhs, local_dict), parse_side(rhs, local_dict)))

def parse_inequality(text):
    for operator in (">=", "<=", ">", "<"):
        if operator in text:
            lhs, rhs = text.split(operator, 1)
            lhs = parse_side(lhs)
            rhs = parse_side(rhs)
            if operator == ">=":
                return check_trivial(lhs >= rhs)
            elif operator == "<=":
                return check_trivial(lhs <= rhs)
            elif operator == ">":
                return check_trivial(lhs > rhs)
            else:
                return check_trivial(lhs < rhs)
    raise ValueError("use one of >, <, >=, <=")

def find_variables(*expressions):
    found = set()
    for expression in expressions:
        found |= expression.free_symbols
    if not found:
        raise ValueError("no variable found")
    return sorted(found, key=str)

def format_solution(variable, solution):
    if not solution:
        return "No solution found."
    return f"{variable} = " + ", ".join(str(value) for value in solution)

def direction_angle(component, magnitude):
    return math.degrees(math.acos(max(-1, min(1, component / magnitude))))

def Solving_Equations():
    Problem = get_int("0. Exit\n1. Solve a linear equation\n2. Solve a quadratic equation\n3. Polynomial equation\n4. Simultaneous equations\n5. Exponential equation\n6. Logarithmic equation\n7. Trigonometric equation\n8. Matrix equation\n9. Modular Arithmetic equation and Congruences\n10. Reccurence Relation\n11. Inequalities\nEnter your choice: ")
    try:
        if Problem == 1:
            equation = input("Enter the linear equation (e.g., 2*x + 3 = 7): ")
            eq = parse_equation(equation)
            variable = find_variables(eq)[0]
            solution = solve(eq, variable)
            print(f"The solution of the linear equation is: {format_solution(variable, solution)}")
        elif Problem == 2:
            equation = input("Enter the quadratic equation (e.g., x**2 - 5*x + 6 = 0): ")
            eq = parse_equation(equation)
            variable = find_variables(eq)[0]
            solution = solve(eq, variable)
            print(f"The solutions of the quadratic equation are: {format_solution(variable, solution)}")
        elif Problem == 3:
            equation = input("Enter the polynomial equation (e.g., x**3 - 6*x**2 + 11*x - 6 = 0): ")
            eq = parse_equation(equation)
            variable = find_variables(eq)[0]
            solution = solve(eq, variable)
            print(f"The solutions of the polynomial equation are: {format_solution(variable, solution)}")
        elif Problem == 4:
            equation1 = input("Enter the first equation (e.g., 2*x + 3*y = 7): ")
            equation2 = input("Enter the second equation (e.g., x - y = 1): ")
            eq1 = parse_equation(equation1)
            eq2 = parse_equation(equation2)
            variables = find_variables(eq1, eq2)
            solution = solve((eq1, eq2), variables)
            if not solution:
                print("The simultaneous equations have no solution.")
            else:
                print(f"The solution of the simultaneous equations is: {solution}")
        elif Problem == 5:
            equation = input("Enter the exponential equation (e.g., 2**x = 8): ")
            eq = parse_equation(equation)
            variable = find_variables(eq)[0]
            solution = solve(eq, variable)
            print(f"The solution of the exponential equation is: {format_solution(variable, solution)}")
        elif Problem == 6:
            equation = input("Enter the logarithmic equation (e.g., log(x, 2) = 3): ")
            eq = parse_equation(equation)
            variable = find_variables(eq)[0]
            solution = solve(eq, variable)
            print(f"The solution of the logarithmic equation is: {format_solution(variable, solution)}")
        elif Problem == 7:
            equation = input("Enter the trigonometric equation (e.g., sin(x) = 0.5): ")
            eq = parse_equation(equation)
            variable = find_variables(eq)[0]
            solution = solve(eq, variable)
            print(f"The solution of the trigonometric equation is: {format_solution(variable, solution)}")
        elif Problem == 8:
            rows = get_int("Enter the number of rows (equations) in A: ")
            columns = get_int("Enter the number of columns (unknowns) in A: ")
            if rows < 1 or columns < 1:
                raise ValueError("A needs at least one row and one column")
            A_rows = []
            for i in range(rows):
                values = input(f"Enter row {i + 1} of A, separated by spaces (e.g., 2 1): ").split()
                if len(values) != columns:
                    raise ValueError(f"row {i + 1} needs exactly {columns} values")
                A_rows.append([parse_side(value) for value in values])
            values = input(f"Enter B as {rows} values separated by spaces (e.g., 5 10): ").split()
            if len(values) != rows:
                raise ValueError(f"B needs exactly {rows} values")
            A = Matrix(A_rows)
            B = Matrix([parse_side(value) for value in values])
            try:
                solution, parameters = A.gauss_jordan_solve(B)
            except ValueError:
                print("The matrix equation has no solution.")
            else:
                print("The solution of the matrix equation is:")
                for i in range(columns):
                    print(f"x{i + 1} = {solution[i]}")
                if len(parameters) > 0:
                    print(f"There are infinitely many solutions. Free parameters: {', '.join(str(p) for p in parameters)}")
        elif Problem == 9:
            print("Solving a*x ≡ b (mod m)")
            a = get_int("Enter a: ")
            b = get_int("Enter b: ")
            m = get_int("Enter m: ")
            if m <= 0:
                print("The modulus m must be positive.")
            else:
                g = math.gcd(a, m)
                if b % g != 0:
                    print("The congruence has no solution.")
                else:
                    reduced_m = m // g
                    if reduced_m == 1:
                        print("Every integer is a solution of the congruence.")
                    else:
                        x = ((b // g) * mod_inverse(a // g, reduced_m)) % reduced_m
                        print(f"The solution of the congruence is: x ≡ {x} (mod {reduced_m})")
        elif Problem == 10:
            equation = input("Enter the recurrence relation (e.g., a(n) = 2*a(n-1) + 1): ")
            n = symbols('n')
            a = Function('a')
            eq = parse_equation(equation, {'a': a, 'n': n})
            solution = rsolve(eq, a(n))
            if solution is None:
                print("Could not solve that recurrence relation.")
            else:
                print(f"The solution of the recurrence relation is: a(n) = {solution}")
        elif Problem == 11:
            equation = input("Enter the inequality (e.g., 2*x + 3 > 7): ")
            eq = parse_inequality(equation)
            variable = find_variables(eq)[0]
            solution = solveset(eq, variable, domain=S.Reals)
            print(f"The solution of the inequality is: {solution}")
        elif Problem == 0:
            print("Exiting equation solving.")
        else:
            print("Invalid choice. Please try again.")
    except ValueError as error:
        print(f"Could not solve that: {error}")
    except Exception:
        print("Could not understand that input. Check brackets, operators and variable names.")

def Pythagoras():
    a = get_float("Enter first number: ")
    b = get_float("Enter second number: ")
    hypotenuse = (a**2 + b**2)**0.5
    print(f"The length of the hypotenuse is: {hypotenuse}")

def addition(a, b):
    return a + b

def subtraction(a, b):
    return a - b

def multiplication(a, b):
    return a * b

def division(a, b):
    if b == 0:
        return "Error: Division by zero is undefined."
    return a / b

def vector_problems():
    Problem_Dimension = get_int("Enter the dimension of the vectors (2 for 2D, 3 for 3D): ")
    if Problem_Dimension not in [2, 3]:
        print("Invalid dimension. Please enter 2 or 3.")
        return
    elif Problem_Dimension == 2:
        Problem = get_int("0. Exit\n1. Find the magnitude of a vector\n2. Find the direction of a vector\n3. Find the dot product of two vectors\nEnter your choice: ")
        if Problem == 1:
            x = get_float("Enter the x-component of the vector: ")
            y = get_float("Enter the y-component of the vector: ")
            magnitude = (x**2 + y**2)**0.5
            print(f"The magnitude of the vector is: {magnitude}")
        elif Problem == 2:
            x = get_float("Enter the x-component of the vector: ")
            y = get_float("Enter the y-component of the vector: ")
            if x == 0 and y == 0:
                print("The zero vector has no direction.")
            else:
                direction = math.degrees(math.atan2(y, x))
                print(f"The direction of the vector is: {direction} degrees")
        elif Problem == 3:
            x1 = get_float("Enter the x-component of the first vector: ")
            y1 = get_float("Enter the y-component of the first vector: ")
            x2 = get_float("Enter the x-component of the second vector: ")
            y2 = get_float("Enter the y-component of the second vector: ")
            dot_product = x1 * x2 + y1 * y2
            print(f"The dot product of the two vectors is: {dot_product}")
        elif Problem == 0:
            print("Exiting vector problems.")
        else:
            print("Invalid choice. Please try again.")
    elif Problem_Dimension == 3:
        Problem = get_int("0. Exit\n1. Find the magnitude of a vector\n2. Find the direction of a vector\n3. Find the dot product of two vectors\n4. Find the cross product of two vectors\nEnter your choice: ")
        if Problem == 1:
            x = get_float("Enter the x-component of the vector: ")
            y = get_float("Enter the y-component of the vector: ")
            z = get_float("Enter the z-component of the vector: ")
            magnitude = (x**2 + y**2 + z**2)**0.5
            print(f"The magnitude of the vector is: {magnitude}")
        elif Problem == 2:
            x = get_float("Enter the x-component of the vector: ")
            y = get_float("Enter the y-component of the vector: ")
            z = get_float("Enter the z-component of the vector: ")
            magnitude = (x**2 + y**2 + z**2)**0.5
            if magnitude == 0:
                print("The zero vector has no direction.")
            else:
                print(f"The direction angles of the vector are: {direction_angle(x, magnitude)} degrees from the x-axis, {direction_angle(y, magnitude)} degrees from the y-axis, {direction_angle(z, magnitude)} degrees from the z-axis")
        elif Problem == 3:
            x1 = get_float("Enter the x-component of the first vector: ")
            y1 = get_float("Enter the y-component of the first vector: ")
            z1 = get_float("Enter the z-component of the first vector: ")
            x2 = get_float("Enter the x-component of the second vector: ")
            y2 = get_float("Enter the y-component of the second vector: ")
            z2 = get_float("Enter the z-component of the second vector: ")
            dot_product = x1 * x2 + y1 * y2 + z1 * z2
            print(f"The dot product of the two vectors is: {dot_product}")
        elif Problem == 4:
            x1 = get_float("Enter the x-component of the first vector: ")
            y1 = get_float("Enter the y-component of the first vector: ")
            z1 = get_float("Enter the z-component of the first vector: ")
            x2 = get_float("Enter the x-component of the second vector: ")
            y2 = get_float("Enter the y-component of the second vector: ")
            z2 = get_float("Enter the z-component of the second vector: ")
            cross_product = (y1 * z2 - z1 * y2, z1 * x2 - x1 * z2, x1 * y2 - y1 * x2)
            print(f"The cross product of the two vectors is: {cross_product}")
        elif Problem == 0:
            print("Exiting vector problems.")
        else:
            print("Invalid choice. Please try again.")

def Log_problems():
    Problem = get_int("0. Exit\n1. Find the logarithm of a number\n2. Find the antilogarithm of a number\n3. Convert between logarithmic and exponential forms\nEnter your choice: ")
    if Problem == 1:
        base = get_float("Enter the base of the logarithm: ")
        number = get_float("Enter the number: ")
        if base <= 0 or base == 1 or number <= 0:
            print("The base must be positive and not 1, and the number must be positive.")
        else:
            log_result = math.log(number, base)
            print(f"The logarithm of {number} with base {base} is: {log_result}")
    elif Problem == 2:
        base = get_float("Enter the base of the antilogarithm: ")
        exponent = get_float("Enter the exponent: ")
        if base <= 0 or base == 1:
            print("The base must be positive and not 1.")
        else:
            try:
                antilog_result = base ** exponent
                print(f"The antilogarithm of {exponent} with base {base} is: {antilog_result}")
            except OverflowError:
                print("The result is too large to calculate.")
    elif Problem == 3:
        base = get_float("Enter the base: ")
        number = get_float("Enter the number: ")
        if base <= 0 or base == 1 or number <= 0:
            print("The base must be positive and not 1, and the number must be positive.")
        else:
            exponent = math.log(number, base)
            print(f"The logarithmic form is: log_{base:g}({number:g}) = {exponent:g}")
            print(f"The exponential form is: {base:g}^{exponent:g} = {number:g}")
    elif Problem == 0:
        print("Exiting logarithm problems.")
    else:
        print("Invalid choice. Please try again.")

def Advanced_Maths():
    while True:
        print("\nSelect advanced operation:")
        print("0. Exit")
        print("1. Vector Problems")
        print("2. Logarithm Problems")
        print("3. Pythagoras Theorem")
        print("4. Solving Equations")
        advanced_choice = input("Enter choice (0/1/2/3/4): ")
        if advanced_choice == '1':
            vector_problems()
        elif advanced_choice == '2':
            Log_problems()
        elif advanced_choice == '3':
            Pythagoras()
        elif advanced_choice == '4':
            Solving_Equations()
        elif advanced_choice == '0':
            print("Exiting advanced problems.")
            break
        else:
            print("Invalid input. Please try again.")

def main():
    while True:
        print("\nSelect operation:")
        print("0. Exit")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Advanced Maths")

        choice = input("Enter choice (0/1/2/3/4/5): ")

        if choice == '0':
            print("Exiting the calculator.")
            break
        elif choice == '5':
            Advanced_Maths()
        elif choice in ['1', '2', '3', '4']:
            a = get_float("Enter first number: ")
            b = get_float("Enter second number: ")
            if choice == '1':
                print(f"The result of addition is: {addition(a, b)}")
            elif choice == '2':
                print(f"The result of subtraction is: {subtraction(a, b)}")
            elif choice == '3':
                print(f"The result of multiplication is: {multiplication(a, b)}")
            elif choice == '4':
                result = division(a, b)
                print(f"The result of division is: {result}")
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()