def find_number(equation):

    def find_number_zero_right(equation):
        equation_left = equation.split('=')
        return equation_left[0]

    def check_whether_0(equation):
        if equation[-1] == '0' and equation[-2] == '=':
            return True
        return False

    if check_whether_0(equation):
        equation = find_number_zero_right(equation)
        if '**2' in equation:
            number = equation.split("**2")[1]
        elif '^2' in equation:
            number = equation.split("^")[1]
        elif 'x2' in equation:
            number = equation.split("x2")[1]
        elif 'y2' in equation:
            number = equation.split("y2")[1]
        else:
            return False
        if (number[0] == '-'):
            return float(number[1:])
        else:
            return -float(number[1:])
    else:
        number = equation.split('=')[1]
        return float(number)
