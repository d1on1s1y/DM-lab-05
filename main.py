def truth_table(boolean_function):
    variables = 3
    table = []
    
    for i in range(2**variables):
        inputs = format(i, f'0{variables}b')
        output = boolean_function(*map(int, inputs))
        table.append((inputs, output))
    
    return table

def dual_function(boolean_function):
    def dual(*args):
        return 1 - boolean_function(*args)
    return dual

def ddnf_dknf(boolean_function):
    ddnf = []
    dknf = []

    for i in range(2**3):
        inputs = format(i, '03b')
        output = boolean_function(*map(int, inputs))

        if output:
            ddnf.append(f"({' & '.join([f'x{j+1}' if int(inputs[j]) else f'~x{j+1}' for j in range(3)])})")
        else:
            dknf.append(f"({' | '.join([f'~x{j+1}' if int(inputs[j]) else f'x{j+1}' for j in range(3)])})")

    return ddnf, dknf

def zhegalkin_polynomial(boolean_function):
    variables = 3
    polynomial = []
    
    for i in range(2**variables):
        inputs = format(i, f'0{variables}b')
        output = boolean_function(*map(int, inputs))
        polynomial.append(output)

    coefficients = []

    for k in range(variables + 1):
        for i in range(2**variables):
            if bin(i).count('1') == k:
                coefficients.append(polynomial[i])

    zhegalkin = []

    for i in range(2**variables):
        inputs = format(i, f'0{variables}b')
        term = coefficients[i]
        for j in range(variables):
            term *= (-1) if inputs[j] == '1' else 1
        zhegalkin.append(term)

    return zhegalkin

def check_properties(boolean_function):
    constant_0 = all(not boolean_function(0, 0, 0) for _ in range(2**3))
    constant_1 = all(boolean_function(1, 1, 1) for _ in range(2**3))
    self_dual = boolean_function == dual_function(boolean_function)
    
    monotonous = all(
        boolean_function(*inputs[:i] + (0,) + inputs[i+1:]) <= boolean_function(*inputs)
        for i in range(3)
        for inputs in [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
    )

    linear = all(
        boolean_function(*inputs[:i] + (0,) + inputs[i+1:]) == boolean_function(*inputs) or
        boolean_function(*inputs[:i] + (1,) + inputs[i+1:]) == boolean_function(*inputs)
        for i in range(3)
        for inputs in [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
    )

    return constant_0, constant_1, self_dual, monotonous, linear

# Задана булева функція
boolean_function = lambda x1, x2, x3: 0b00100001 >> (x3 + 2*x2 + 4*x1) & 1

# a. Таблиця істинності
print("a. Таблиця істинності:")
table = truth_table(boolean_function)
for row in table:
    print(f"{row[0]} -> {row[1]}")

# b. Функція двоїста
dual_boolean_function = dual_function(boolean_function)
print("\nb. Функція двоїста:")
print(f"Двійник: {dual_boolean_function.__name__}")

# c. ДДНФ та ДКНФ
ddnf, dknf = ddnf_dknf(boolean_function)
print("\nc. ДДНФ:")
print(" | ".join(ddnf))
print("\nДКНФ:")
print(" | ".join(dknf))

# d. Поліном Жегалкіна
zhegalkin = zhegalkin_polynomial(boolean_function)
print("\nd. Поліном Жегалкіна:")
print(" + ".join([str(term) for term in zhegalkin]))

# e. Властивості
print("\ne. Властивості:")
constant_0, constant_1, self_dual, monotonous, linear = check_properties(boolean_function)
print(f"Зберігає константу 0: {constant_0}")
print(f"Зберігає константу 1: {constant_1}")
print(f"Самодвоїста: {self_dual}")
print(f"Монотонна: {monotonous}")
print(f"Лінійна: {linear}")