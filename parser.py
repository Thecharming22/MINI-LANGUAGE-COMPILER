from thetokens import Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = tokens[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]

    def eat(self, type_, value=None):
        if self.current.type == type_ and (value is None or self.current.value == value):
            self.advance()
        else:
            raise Exception(f"Unexpected token {self.current.type}:{self.current.value}")

    def parse(self):
        statements = []
        while self.current.type != "EOF":
            statements.append(self.statement())
        return ("PROGRAM", statements)

    # ---------------- STATEMENTS ----------------

    def statement(self):
        if self.current.type in ["INT", "FLOAT", "STRING"]:
            node = self.declaration()
            self.eat("SEPARATOR", ";")
            return node

        elif self.current.type == "IDENTIFIER":
            node = self.assignment()
            self.eat("SEPARATOR", ";")
            return node

        elif self.current.type == "PRINT":
            node = self.print_stmt()
            self.eat("SEPARATOR", ";")
            return node

        elif self.current.type == "IF":
            return self.if_stmt()

        elif self.current.type == "FOR":
            return self.for_stmt()

        else:
            raise Exception("Invalid statement")

    def declaration(self):
        type_ = self.current.type
        self.advance()

        name = self.current.value
        self.eat("IDENTIFIER")

        value = None
        if self.current.value == "=":
            self.eat("OPERATOR", "=")
            value = self.expr()

        return ("DECL", type_, name, value)

    def assignment(self):
        name = self.current.value
        self.eat("IDENTIFIER")

        if self.current.value == "=":
            self.eat("OPERATOR", "=")
            return ("ASSIGN", name, self.expr())

        elif self.current.value in ["++", "--"]:
            op = self.current.value
            self.advance()
            return ("UPDATE", name, op)

    def print_stmt(self):
        self.eat("PRINT")
        return ("PRINT", self.expr())

    def if_stmt(self):
        self.eat("IF")
        self.eat("SEPARATOR", "(")
        cond = self.expr()
        self.eat("SEPARATOR", ")")

        if_block = self.block()
        else_block = None

        if self.current.type == "ELSE":
            self.eat("ELSE")
            else_block = self.block()

        return ("IF", cond, if_block, else_block)

    def for_stmt(self):
        self.eat("FOR")
        self.eat("SEPARATOR", "(")

        init = self.statement()
        cond = self.expr()
        self.eat("SEPARATOR", ";")
        update = self.assignment()

        self.eat("SEPARATOR", ")")
        block = self.block()

        return ("FOR", init, cond, update, block)

    def block(self):
        self.eat("SEPARATOR", "{")
        statements = []
        while self.current.value != "}":
            statements.append(self.statement())
        self.eat("SEPARATOR", "}")
        return statements

    # ---------------- EXPRESSIONS ----------------

    def expr(self):
        return self.logical_or()

    def logical_or(self):
        node = self.logical_and()
        while self.current.value == "||":
            op = self.current.value
            self.advance()
            node = ("BINOP", op, node, self.logical_and())
        return node

    def logical_and(self):
        node = self.comparison()
        while self.current.value == "&&":
            op = self.current.value
            self.advance()
            node = ("BINOP", op, node, self.comparison())
        return node

    def comparison(self):
        node = self.addition()
        while self.current.value in ["==", "!=", "<", ">", "<=", ">="]:
            op = self.current.value
            self.advance()
            node = ("BINOP", op, node, self.addition())
        return node

    def addition(self):
        node = self.term()
        while self.current.value in ["+", "-"]:
            op = self.current.value
            self.advance()
            node = ("BINOP", op, node, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current.value in ["*", "/", "%"]:
            op = self.current.value
            self.advance()
            node = ("BINOP", op, node, self.factor())
        return node

    def factor(self):
        tok = self.current

        if tok.type == "NUMBER":
            self.advance()
            return ("NUM", float(tok.value))

        elif tok.type == "STRING_LITERAL":
            self.advance()
            return ("STR", tok.value)

        elif tok.type == "IDENTIFIER":
            self.advance()
            node = ("VAR", tok.value)

            while True:
                # 🔹 PROPERTY: text.length
                if self.current.type == "SEPARATOR" and self.current.value == ".":
                    self.eat("SEPARATOR", ".")
                    prop = self.current.value
                    self.eat("IDENTIFIER")
                    node = ("PROP", node, prop)

                # 🔹 INDEXING: text[1]
                elif self.current.type == "SEPARATOR" and self.current.value == "[":
                    self.eat("SEPARATOR", "[")
                    index = self.expr()
                    self.eat("SEPARATOR", "]")
                    node = ("INDEX", node, index)

                else:
                    break

            return node

        elif tok.type == "INPUT":
            self.advance()
            return ("INPUT",)

        elif tok.value == "(":
            self.eat("SEPARATOR", "(")
            node = self.expr()
            self.eat("SEPARATOR", ")")
            return node

        else:
            raise Exception("Invalid expression")