import re


def set_description_message_pattern(pattern: str) -> None:
    first_check = re.fullmatch(r'.*{commmand}.*', pattern)
    second_check = re.fullmatch(r'.*{description}.*', pattern)
    print(bool(first_check))
    print(second_check)


set_description_message_pattern('Invalid des{command}cription pattern')