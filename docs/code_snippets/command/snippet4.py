from argenta.command import InputCommand

# Parse command without flags
cmd1 = InputCommand.parse("hello")
print(cmd1.trigger)  # "hello"
print(len(cmd1.input_flags))  # 0

# Parse command with flags
cmd2 = InputCommand.parse("deploy --env prod --force")
print(cmd2.trigger)  # "deploy"
print(len(cmd2.input_flags))  # 2
