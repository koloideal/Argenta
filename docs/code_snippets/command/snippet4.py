from argenta.command import InputCommand

# Парсинг команды без флагов
cmd1 = InputCommand.parse("hello")
print(cmd1.trigger)  # "hello"
print(len(cmd1.input_flags))  # 0

# Парсинг команды с флагами
cmd2 = InputCommand.parse("deploy --env prod --force")
print(cmd2.trigger)  # "deploy"
print(len(cmd2.input_flags))  # 2