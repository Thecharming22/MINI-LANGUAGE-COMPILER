class Token:
    def __init__(self, type_, value, line=None):
        self.type = type_
        self.value = value
        self.line = line

    def __repr__(self): #testing purself.pose will remove later
        return f"Token({self.type}, {self.value}, {self.line})"