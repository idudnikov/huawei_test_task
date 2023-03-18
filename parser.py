import unittest


class LowerCaseLetterStartException(Exception):
    """
    Exception for cases when element name starts with lowercase letter.
    """

    def __init__(self, message='Error: element name can not start with lowercase letter'):
        self.message = message
        super().__init__(self.message)


class WrongElementQuantityException(Exception):
    """
    Exception for cases when wrong element quantity provided.
    """

    def __init__(self, message='Error: element quantity can not be below "1"'):
        self.message = message
        super().__init__(self.message)


class WrongElementQuantityPlacementException(Exception):
    """
    Exception for cases when quantity placed before element name.
    """

    def __init__(self, message='Error: element quantity can not be placed before element'):
        self.message = message
        super().__init__(self.message)


def parse_main(data):
    """
    Main logic, that parses input string with chemical formula.
    """

    result = []
    if '*' in data:
        split = data.split(' * ')
        for item in split:
            result.append(parse_chemical_formula(item))
    else:
        return parse_chemical_formula(data)
    return result


def add_element_to_result(name, quantity, result):
    """
    Function, that takes element name and quantity to add them to result data.
    """

    if result.get(name) is None:
        result[name] = int(quantity) if quantity != '' else 1
    else:
        result[name] += int(quantity) if quantity != '' else 1
    return result


def calculate_bracket_expression(data, multiplier, result):
    """
    Function, that calculates expression inside brackets and adds in to final result data.
    """

    brackets_result = parse_chemical_formula(data)
    if multiplier != '':
        brackets_expression_multiplier = int(multiplier)
        for key in brackets_result:
            brackets_result[key] *= brackets_expression_multiplier
    for key in brackets_result:
        if key in result:
            result[key] += brackets_result[key]
        else:
            result[key] = brackets_result[key]


def parse_chemical_formula(string_data: str):
    """
    Function, that parses single chemical element.
    """

    name = ''
    quantity = ''
    result = {}
    single_element = True
    prefix = ''
    inside_brackets = False
    close_bracket = ''
    brackets_expression = ''
    search_brackets_multiplier = False
    brackets_expression_multiplier = ''

    for item in string_data:
        if inside_brackets is True and item != close_bracket:
            brackets_expression += item
        elif inside_brackets is True and item == close_bracket:
            inside_brackets = False
            search_brackets_multiplier = True
        elif search_brackets_multiplier is True and item.isdigit():
            brackets_expression_multiplier += item
        elif search_brackets_multiplier is True and not item.isdigit():
            search_brackets_multiplier = False
            calculate_bracket_expression(brackets_expression, brackets_expression_multiplier, result)
        elif item.isalpha():
            if item.isupper():
                if name == '' and quantity == '':
                    name += item
                elif name != '':
                    single_element = False
                    result = add_element_to_result(name, quantity, result)
                    name = item
                    quantity = ''
            elif item.islower():
                if name == '':
                    raise LowerCaseLetterStartException
                else:
                    name += item
        elif item.isdigit():
            if int(item) < 1:
                raise WrongElementQuantityException
            if name == '':
                prefix += item
            elif name != '':
                quantity += item
        elif name != '' and item == '-':
            raise WrongElementQuantityException
        elif item in ('(', '['):
            inside_brackets = True
            close_bracket = ')' if item == '(' else ']'

    if name != '' or quantity != '':
        result = add_element_to_result(name, quantity, result)

    if brackets_expression != '':
        calculate_bracket_expression(brackets_expression, brackets_expression_multiplier, result)

    if prefix != '' and single_element is True:
        raise WrongElementQuantityPlacementException
    elif prefix != '':
        prefix = int(prefix)
        for key in result:
            result[key] *= prefix

    return result


class TestsPart1(unittest.TestCase):
    """
    Test cases from "Part 1" of the test task.
    """

    def test_1(self):
        self.input = 'Fe'
        self.output = {'Fe': 1}
        self.assertEqual(parse_main(self.input), self.output)

    def test_2(self):
        self.input = 'Fe2'
        self.output = {'Fe': 2}
        self.assertEqual(parse_main(self.input), self.output)

    def test_3(self):
        self.input = 'Ag12'
        self.output = {'Ag': 12}
        self.assertEqual(parse_main(self.input), self.output)

    def test_4(self):
        self.input = 'N0'
        with self.assertRaises(WrongElementQuantityException):
            parse_main(self.input)

    def test_5(self):
        self.input = 'N-1'
        with self.assertRaises(WrongElementQuantityException):
            parse_main(self.input)

    def test_6(self):
        self.input = 'cl'
        with self.assertRaises(LowerCaseLetterStartException):
            parse_main(self.input)

    def test_7(self):
        self.input = '2F'
        with self.assertRaises(WrongElementQuantityPlacementException):
            parse_main(self.input)


class TestsPart2(unittest.TestCase):
    """
    Test cases from "Part 2" of the test task.
    """

    def test_1(self):
        self.input = 'Fe2O3'
        self.output = {'Fe': 2, 'O': 3}
        self.assertEqual(parse_main(self.input), self.output)

    def test_2(self):
        self.input = 'H2SO4'
        self.output = {'H': 2, 'S': 1, 'O': 4}
        self.assertEqual(parse_main(self.input), self.output)

    def test_3(self):
        self.input = 'HOH'
        self.output = {'H': 2, 'O': 1}
        self.assertEqual(parse_main(self.input), self.output)


class TestsPart3(unittest.TestCase):
    """
    Test cases from "Part 3" of the test task.
    """

    def test_1(self):
        self.input = 'Fe2(SO4)3'
        self.output = {'Fe': 2, 'S': 3, 'O': 12}
        self.assertEqual(parse_main(self.input), self.output)

    def test_2(self):
        self.input = 'K[Fe(NO3)2]4'
        self.output = {'K': 1, 'Fe': 4, 'N': 8, 'O': 24}
        self.assertEqual(parse_main(self.input), self.output)


class TestsPart4(unittest.TestCase):
    """
    Test cases from "Part 4" of the test task.
    """

    def test_1(self):
        self.input = 'CuSO4 * 5H2O'
        self.output = [{'Cu': 1, 'S': 1, 'O': 4}, {'H': 10, 'O': 5}]
        self.assertEqual(parse_main(self.input), self.output)


if __name__ == '__main__':
    unittest.main()
