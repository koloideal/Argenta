config_arg = argspace.get_by_name("config")
if config_arg:
    print(f"Config path: {config_arg.value}")

verbose_arg = argspace.get_by_name("verbose")
if verbose_arg and verbose_arg.value:
    print("Verbose mode enabled")

unknown_arg = argspace.get_by_name("nonexistent")
if unknown_arg is None:
    print("Argument not found")
