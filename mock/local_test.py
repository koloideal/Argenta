from argenta.orchestrator.argparser import ArgSpace, BooleanArgument, ValueArgument
from argenta.orchestrator.argparser.arguments import InputArgument

argspace = ArgSpace([
    InputArgument(name="arg1", value="val1", founder_class=ValueArgument),
    InputArgument(name="arg2", value=True, founder_class=BooleanArgument),
    InputArgument(name="arg3", value="val3", founder_class=ValueArgument),
])

print(argspace._name_object_paired_args)
print(argspace.get_by_type(ValueArgument))