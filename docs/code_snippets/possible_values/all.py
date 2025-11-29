from argenta.command import Flag, PossibleValues

# Creating flags with any values
message_flag = Flag(name="message", possible_values=PossibleValues.ALL)
name_flag = Flag(name="name", possible_values=PossibleValues.ALL)
