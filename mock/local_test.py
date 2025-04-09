import readline


def completer(text, state):
    matches = sorted(cmd for cmd in get_history_items() if cmd.startswith(text))
    if len(matches) > 1:
        common_prefix = matches[0]
        for match in matches[1:]:
            i = 0
            while i < len(common_prefix) and i < len(match) and common_prefix[i] == match[i]:
                i += 1
            common_prefix = common_prefix[:i]
        if state == 0:
            readline.insert_text(common_prefix[len(text):])
            readline.redisplay()
        return None
    elif len(matches) == 1:
        return matches[0] if state == 0 else None
    else:
        return None

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

def get_history_items():
    return [readline.get_history_item(i) for i in range(1, readline.get_current_history_length() + 1)]

while True:
    try:
        line = input('> ')
    except EOFError:
        break