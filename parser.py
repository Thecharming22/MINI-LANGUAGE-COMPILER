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

    # 🔹 STATEMENT
    def statement(self):
        if self.current.type in ["INT", "STRING", "FLOAT"]:
            self.declaration()
            self.eat("SEPARATOR", ";")   # semicolon only in normal declaration

        elif self.current.type == "IDENTIFIER":
            self.assignment()

        elif self.current.type == "PRINT":
            self.print_stmt()

        elif self.current.type == "IF":
            self.if_stmt()

        elif self.current.type == "FOR":
            self.for_stmt()

        else:
            self.error(f"Invalid statement {self.current.type}")

    # 🔹 DECLARATION (no semicolon here)
    def declaration(self):
        self.advance()  # consume INT/FLOAT/STRING
        self.eat("IDENTIFIER")

        if self.current.value == "=":
            self.eat("OPERATOR", "=")
            self.expr()

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

    # 🔹 IF ELSE
    def if_stmt(self):
        self.eat("IF")
        self.eat("SEPARATOR", "(")
        self.expr()
        self.eat("SEPARATOR", ")")
        self.block()

        if self.current.type == "ELSE":
            self.eat("ELSE")
            self.block()

    # 🔹 FOR LOOP
    def for_stmt(self):
        self.eat("FOR")
        self.eat("SEPARATOR", "(")

        # init declaration (semicolon required here)
        self.declaration()
        self.eat("SEPARATOR", ";")

        # condition
        self.expr()
        self.eat("SEPARATOR", ";")

        # update assignment
        self.assignment()

        self.eat("SEPARATOR", ")")
        self.block()

    # 🔹 BLOCK
    def block(self):
        self.eat("SEPARATOR", "{")
        while self.current.value != "}":
            self.statement()
        self.eat("SEPARATOR", "}")

    # 🔹 EXPRESSION
    def expr(self):
        self.term()
        while self.current.type == "OPERATOR":
            self.advance()
            self.term()

    # 🔹 TERM
    def term(self):
        if self.current.type in ["NUMBER", "IDENTIFIER", "INPUT", "STRING_LITERAL"]:
            self.advance()
        else:
            self.error("Invalid expression")
