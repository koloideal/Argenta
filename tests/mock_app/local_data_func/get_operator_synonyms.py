import json


def get_operator_synonyms() -> dict[str, list[str]]:
    with open("tests/mock_app/local_data/operator_synonyms.json", "r", encoding="utf-8") as file:
        operator_synonyms: dict = json.load(file)

    return operator_synonyms
