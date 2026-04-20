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
            self.eat("SEPARATOR", ";")
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

    def declaration(self):
        self.advance()
        self.eat("IDENTIFIER")
        if self.current.type == "OPERATOR" and self.current.value == "=":
            self.eat("OPERATOR", "=")
            self.expr()

    def assignment(self):
        self.eat("IDENTIFIER")
        if self.current.type == "OPERATOR" and self.current.value == "=":
            self.eat("OPERATOR", "=")
            self.expr()
        elif self.current.type == "OPERATOR" and self.current.value in ["++", "--"]:
            self.advance()
        else:
            self.error("Invalid assignment/update")
        if self.current.type == "SEPARATOR" and self.current.value == ";":
            self.eat("SEPARATOR", ";")

    def print_stmt(self):
        self.eat("PRINT")
        self.expr()
        self.eat("SEPARATOR", ";")

    def if_stmt(self):
        self.eat("IF")
        self.eat("SEPARATOR", "(")
        self.expr()
        self.eat("SEPARATOR", ")")
        self.block()
        if self.current.type == "ELSE":
            self.eat("ELSE")
            self.block()

    def for_stmt(self):
        self.eat("FOR")
        self.eat("SEPARATOR", "(")
        self.declaration()
        self.eat("SEPARATOR", ";")
        self.expr()
        self.eat("SEPARATOR", ";")
        self.assignment()
        self.eat("SEPARATOR", ")")
        self.block()

    def block(self):
        self.eat("SEPARATOR", "{")
        while not (self.current.type == "SEPARATOR" and self.current.value == "}"):
            self.statement()
        self.eat("SEPARATOR", "}")

    # -------------------------
    # Expression Parsing (with precedence)
    # -------------------------

    def expr(self):
        return self.logical_or()

    def logical_or(self):
        node = self.logical_and()
        while self.current.type == "OPERATOR" and self.current.value == "||":
            op = self.current.value
            self.advance()
            right = self.logical_and()
            node = ("BINOP", op, node, right)
        return node

    def logical_and(self):
        node = self.comparison()
        while self.current.type == "OPERATOR" and self.current.value == "&&":
            op = self.current.value
            self.advance()
            right = self.comparison()
            node = ("BINOP", op, node, right)
        return node

    def comparison(self):
        node = self.addition()
        while self.current.type == "OPERATOR" and self.current.value in ["==", "!=", "<", ">", "<=", ">="]:
            op = self.current.value
            self.advance()
            right = self.addition()
            node = ("BINOP", op, node, right)
        return node

    def addition(self):
        node = self.term()
        while self.current.type == "OPERATOR" and self.current.value in ["+", "-"]:
            op = self.current.value
            self.advance()
            right = self.term()
            node = ("BINOP", op, node, right)
        return node

    def term(self):
        node = self.factor()
        while self.current.type == "OPERATOR" and self.current.value in ["*", "/", "%"]:
            op = self.current.value
            self.advance()
            right = self.factor()
            node = ("BINOP", op, node, right)
        return node

    def factor(self):
        if self.current.type in ["NUMBER", "IDENTIFIER", "INPUT", "STRING_LITERAL"]:
            node = ("ATOM", self.current.value)
            self.advance()
            while self.current.type == "SEPARATOR" and self.current.value == ".":
                self.eat("SEPARATOR", ".")
                prop = self.current.value
                self.eat("IDENTIFIER")
                node = ("PROP", node, prop)
            while self.current.type == "SEPARATOR" and self.current.value == "[":
                self.eat("SEPARATOR", "[")
                index = self.expr()
                self.eat("SEPARATOR", "]")
                node = ("INDEX", node, index)
            return node
        elif self.current.type == "SEPARATOR" and self.current.value == "(":
            self.eat("SEPARATOR", "(")
            node = self.expr()
            self.eat("SEPARATOR", ")")
            return node
        else:
            self.error("Invalid expression")
