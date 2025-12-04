from argenta.command import Flag, PossibleValues

# Creating flags without values
help_flag = Flag(name="help", possible_values=PossibleValues.NEITHER)
verbose_flag = Flag(name="verbose", possible_values=PossibleValues.NEITHER)
force_flag = Flag(name="force", possible_values=PossibleValues.NEITHER)
