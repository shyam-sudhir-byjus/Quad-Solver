from sympy import symbols


def side_cases(equation):
    flag = True
    if 'x' in equation:
        var = symbols('x')
        variable = 'x'
        x_index = equation.index('x')
        if equation[x_index+1].isdigit() and equation[x_index+1] != '2':
            flag = False
        elif equation[x_index+2].isdigit() and equation[x_index+2] != '2':
            flag = False
        elif '**' in equation:
            eq_right_num = equation.split('**')[1][0]
            if eq_right_num != '2':
                flag = False
        elif '^' in equation:
            eq_right_num = equation.split('^')[1][0]
            if eq_right_num != '2':
                flag = False
        if equation[0] == 'x':
            number_left = float(1)
        elif equation[0].isdigit():
            coeff = equation.split('x')[0]
            number_left = float(coeff)
    else:
        var = symbols('y')
        variable = 'y'
        y_index = equation.index('y')
        if equation[y_index+1].isdigit() and equation[y_index+1] != '2':
            flag = False
        elif equation[y_index+2].isdigit() and equation[y_index+2] != '2':
            flag = False
        elif '**' in equation:
            eq_right_num = equation.split('**')[1][0]
            if eq_right_num != '2':
                flag = False
        elif '^' in equation:
            eq_right_num = equation.split('^')[1][0]
            if eq_right_num != '2':
                flag = False

        if equation[0] == 'y':
            number_left = float(1)
        elif equation[0].isdigit():
            coeff = equation.split('y')[0]
            number_left = float(coeff)
    return flag,  number_left, var, variable
