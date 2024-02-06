class Integer:
    def __init__(self, value: int) -> None:
        if isinstance(value, str):
            self.value = int(value)
        else:
            self.value = value

    def __str__(self):
        return str(self.value)


class String:
    def __init__(self, value: str) -> None:
        if isinstance(value, str):
            if not value.startswith('"'):
             value = '"' + value + '"'
        elif value.value[-1] != '"':
            value = '"' + value + '"'

        self.value = value

    def __add__(self, other):
        return String('', self.name + other.name)

    def __str__(self):
        return str(self.value)


class Double:
    def __init__(self, value: str) -> None:
        if isinstance(value, str):
            self.value = float(value)
        else:
            self.value = value

    def __str__(self):
        return str(self.value)


class Boolean:
    def __init__(self, value: str) -> None:
        if isinstance(value, str):
            self.value = eval(value.capitalize())
        else:
            self.value = value.value

    def __str__(self):
        return str(self.value)
