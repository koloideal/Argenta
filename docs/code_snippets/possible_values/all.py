from argenta.command import Flag, PossibleValues

# Создание флагов с любыми значениями
output_flag = Flag(name="output", possible_values=PossibleValues.ALL)
message_flag = Flag(name="message", possible_values=PossibleValues.ALL)
name_flag = Flag(name="name", possible_values=PossibleValues.ALL)

# Можно передать любую строку или ничего
# Примеры: 
# --output result.json
# --message "Any text here"
# --name "User Name"
# --message
