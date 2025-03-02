from numpy import ndarray
from word2number import w2n
from ..local_data_func.get_operator_synonyms import get_operator_synonyms
import numexpr


def word2num_math(string: str) -> ndarray | ZeroDivisionError | OverflowError:
    operator_synonyms: dict[str, list[str]] = get_operator_synonyms()

    def variables_to_operator(synonym):
        for key in operator_synonyms.keys():
            if synonym in operator_synonyms[key]:
                return key

    action = {
        "plus": '+',
        "minus": '-',
        "divide": '/',
        "multiply": '*',
        "degree": '**',
    }

    result_string: str = ''
    all_variables_of_operators: list[str] = [x for l in operator_synonyms.values() for x in l]
    operators = {}

    while True:
        is_clear = True
        number_of_operator = 1
        for word in string.split():
            try:
                if word in all_variables_of_operators:
                    ope_index = string.index(word)
                    if ope_index in operators.keys():
                        is_clear = True
                        break
                else:
                    raise ValueError
            except ValueError:
                continue
            else:
                is_clear = False
                operators[number_of_operator] = variables_to_operator(word)
                number_of_operator += 1
                string = string.replace(word, "&&", 1)
        if is_clear:
            break

    num_of_ope = 1
    for number in string.split("&&"):
        try:
            int_num = w2n.word_to_num(number.strip())
        except ValueError:
            return ValueError("Invalid input expression")
        if num_of_ope in operators.keys():
            result_string += f'{int_num} {action[operators[num_of_ope]]} '
            num_of_ope += 1
        else:
            result_string += f'{int_num}'

    try:
        result = numexpr.evaluate(result_string)
    except ZeroDivisionError:
        return ZeroDivisionError('Except divide by zero')
    except OverflowError:
        return OverflowError('Too big result')
    else:
        return result
