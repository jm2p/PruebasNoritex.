def evaluate(m):
    def parse_formula(formula, cell_dict):
        if formula.isdigit():
            return int(formula)
        if formula.startswith('='):
            expression = formula[1:]
            expression = expression.replace(' ', '')
            return eval_expression(expression, cell_dict)
        return formula

    def eval_expression(expression, cell_dict):
        if '+' in expression:
            operands = expression.split('+')
            return parse_formula(operands[0], cell_dict) + parse_formula(operands[1], cell_dict)
        elif '-' in expression:
            operands = expression.split('-')
            return parse_formula(operands[0], cell_dict) - parse_formula(operands[1], cell_dict)
        elif '*' in expression:
            operands = expression.split('*')
            return parse_formula(operands[0], cell_dict) * parse_formula(operands[1], cell_dict)
        elif '/' in expression:
            operands = expression.split('/')
            return parse_formula(operands[0], cell_dict) / parse_formula(operands[1], cell_dict)
        else:
            return parse_formula(expression, cell_dict)

    def get_cell_coordinates(cell_name):
        col_name, row_number = '', ''
        for char in cell_name:
            if char.isalpha():
                col_name += char.upper()
            elif char.isdigit():
                row_number += char
        return col_name, int(row_number) - 1

    def is_valid_cell(cell_name, num_rows, num_cols):
        col_name, row_number = get_cell_coordinates(cell_name)
        if row_number >= 0 and row_number < num_rows and col_name >= 'A' and col_name < chr(ord('A') + num_cols):
            return True
        return False

    def evaluate_matrix(matrix):
        num_rows = len(matrix)
        num_cols = len(matrix[0])
        cell_dict = {}
        result_matrix = [[0] * num_cols for _ in range(num_rows)]
        for i in range(num_rows):
            for j in range(num_cols):
                cell_value = matrix[i][j]
                if isinstance(cell_value, str) and cell_value.startswith('='):
                    cell_name = cell_value[1:]
                    if not is_valid_cell(cell_name, num_rows, num_cols):
                        raise ReferenceError(f"Invalid cell reference: {cell_name}")
                    if cell_name in cell_dict:
                        raise ValueError("Circular reference detected")
                    cell_dict[cell_name] = (i, j)
        for i in range(num_rows):
            for j in range(num_cols):
                cell_value = matrix[i][j]
                if isinstance(cell_value, str) and cell_value.startswith('='):
                    cell_name = cell_value[1:]
                    result_matrix[i][j] = eval_expression(cell_name, cell_dict)
                else:
                    result_matrix[i][j] = cell_value
        return result_matrix

    try:
        return evaluate_matrix(m)
    except (ReferenceError, ValueError, ZeroDivisionError) as e:
        return type(e)

# Ejemplo de uso:
matrix = [
    [1, "=A1+1"],
    [3, "=A2+1"]
]
result = evaluate(matrix)
print(result)
