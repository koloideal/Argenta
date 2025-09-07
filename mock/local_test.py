from argenta.command import InputCommand


parsed = InputCommand.parse('prt ---port --host 22')


print(f'trigger: {parsed.trigger}\n')
for flag in parsed.input_flags:
    print(f'flag: {flag}')
