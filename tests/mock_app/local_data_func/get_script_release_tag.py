import json


def get_script_tag() -> str:
    with open("tests/mock_app/local_data/script_release_tag.json", "r", encoding="utf-8") as file:
        script_release_tag: str = json.load(file)['tag']

    return script_release_tag
