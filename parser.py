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

    # 🔹 MAIN
    def parse(self):
        while self.current.type != "EOF":
            self.statement()

        print("Parsing successful ✅")

    # 🔹 STATEMENTS
    def statement(self):
        if self.current.type in ["INT", "STRING", "FLOAT"]:
            self.declaration()
        elif self.current.type == "IDENTIFIER":
            self.assignment()
        elif self.current.type == "PRINT":
            self.print_stmt()
        elif self.current.type == "IF":
            self.if_stmt()
        elif self.current.type == "FOR":
            self.for_stmt()
        else:
            self.error(f"Invalid statement starting with {self.current.type}")

    # 🔹 DECLARATION
    def declaration(self):
        self.advance()
        self.eat("IDENTIFIER")

        if self.current.value == "=":
            self.eat("OPERATOR", "=")
            self.expr()

        self.eat("SEPARATOR", ";")

    # 🔹 ASSIGNMENT
    def assignment(self):
        self.eat("IDENTIFIER")
        self.eat("OPERATOR", "=")
        self.expr()
        self.eat("SEPARATOR", ";")

    # 🔹 PRINT
    def print_stmt(self):
        self.eat("PRINT")
        self.expr()
        self.eat("SEPARATOR", ";")

    # 🔹 IF + ELSE
    def if_stmt(self):
        self.eat("IF")
        self.eat("SEPARATOR", "(")
        self.expr()
        self.eat("SEPARATOR", ")")

        self.block()

        if self.current.type == "ELSE":
            self.eat("ELSE")
            self.block()

    # 🔹 FOR
    def for_stmt(self):
        self.eat("FOR")
        self.eat("SEPARATOR", "(")

        if self.current.type in ["INT", "STRING", "FLOAT"]:
            self.declaration()
        else:
            self.assignment()

        self.expr()
        self.eat("SEPARATOR", ";")

        self.simple_assignment()

        self.eat("SEPARATOR", ")")
        self.block()

    # 🔹 BLOCK
    def block(self):
        self.eat("SEPARATOR", "{")

        while self.current.value != "}":
            self.statement()

        self.eat("SEPARATOR", "}")

    # 🔹 Increment helper
    def simple_assignment(self):
        self.eat("IDENTIFIER")
        self.eat("OPERATOR", "=")
        self.expr()

    # 🔹 EXPRESSION
    def expr(self):
        self.term()

        while self.current.type == "OPERATOR":
            self.advance()
            self.term()

    # 🔹 TERM ✅ FIXED INDENTATION
    def term(self):
        if self.current.type in ["NUMBER", "IDENTIFIER", "INPUT", "STRING_LITERAL"]:
            self.advance()
        else:
            self.error("Invalid expression")