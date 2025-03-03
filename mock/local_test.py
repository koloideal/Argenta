import re


def set_description_message_pattern(pattern: str) -> None:
    first_check = re.match(r'.*command.*', pattern)
    second_check = re.match(r'.*{description}.*', pattern)


set_description_message_pattern('Invalid des{ommand}cription pattern')