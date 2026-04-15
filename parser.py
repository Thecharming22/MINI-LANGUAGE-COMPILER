from thetokens import Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = self.tokens[self.pos]

    def error(self, msg):
        raise Exception(f"Syntax Error at line {self.current.line}: {msg}")

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]

    def eat(self, token_type, value=None):
        if self.current.type == token_type:
            if value is None or self.current.value == value:
                self.advance()
            else:
                self.error(f"Expected {value}, got {self.current.value}")
        else:
            self.error(f"Expected {token_type}, got {self.current.type}")

    def parse(self):
        while self.current.type != "EOF":
            self.statement()

    def statement(self):
        if self.current.type in ["INT", "STRING", "FLOAT"]:
            self.declaration()
        elif self.current.type == "IDENTIFIER":
            self.assignment()
        elif self.current.type == "PRINT":
            self.print_stmt()
        else:
            self.error(f"Invalid statement {self.current.type}")

    def declaration(self):
        self.advance()
        self.eat("IDENTIFIER")

        if self.current.value == "=":
            self.eat("OPERATOR", "=")
            self.expr()

        self.eat("SEPARATOR", ";")

    def assignment(self):
        self.eat("IDENTIFIER")
        self.eat("OPERATOR", "=")
        self.expr()
        self.eat("SEPARATOR", ";")

    def print_stmt(self):
        self.eat("PRINT")
        self.expr()
        self.eat("SEPARATOR", ";")

    def expr(self):
        self.term()
        while self.current.type == "OPERATOR":
            self.advance()
            self.term()

    def term(self):
        if self.current.type in ["NUMBER", "IDENTIFIER", "INPUT", "STRING"]:
            self.advance()
        else:
            self.error("Invalid expression")