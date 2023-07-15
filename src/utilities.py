def read_opt(prompt, options):
    
    opts = "/".join(options.keys())

    while True:
        key = input(f'{prompt} [{opts}]: ').casefold()
        if key in options:
            return options[key]
        else:
            print(f'"{key}" is not a valid option.')

def read_yn(prompt):
    return read_opt(prompt, {"yes": True, "no": False})

def read_num(prompt):
    while True:
        try:
            text = input(f'{prompt}: ')
            return float(text)
        except ValueError:
            print(f'"{text}" is not a valid number.')

def read_enum(prompt, enum):
    opts = "/".join([e.name for e in enum])

    while True:
        try:
            name = input(f'{prompt} [{opts}]: ')
            return enum[name.casefold()]
        except KeyError:
            print(f'"{name}" is not a valid option.')
        