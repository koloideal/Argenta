from argenta.app import AutoCompleter


if __name__ == "__main__":
    test_commands: set[str] = {"start", "qwertyu", "stop", "exit"}
    hist_file: str = "history.txt"

    ac: AutoCompleter = AutoCompleter(autocomplete_button='tab')
    ac.initial_setup(test_commands)

    while True:
        inp: str = ac.prompt(">>> ").strip()
        if inp == "exit":
            break
