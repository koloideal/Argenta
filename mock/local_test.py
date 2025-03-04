import re


def set_description_message_pattern(pattern: str) -> None:
    first_check = re.match(r'.*command.*', pattern)
    second_check = re.match(r'.*{description}.*', pattern)
    if bool(first_check) and bool(second_check):
        print('Success')


set_description_message_pattern('Invalid des{ommand}cription pattern')