class Executor:
    def __init__(self, input_values=None):
        self.variables = {}
        self.input_values = input_values or []

    def safe(self, tokens, i):
        return i < len(tokens)

    def execute(self, tokens):
        i = 0
        output = ""

        while i < len(tokens):
            token = tokens[i]

            # 🔹 DECLARATION
            if token.type in ["INT", "FLOAT", "STRING"] and self.safe(tokens, i+1):
                var_name = tokens[i+1].value
                value = self.evaluate_expression(tokens, i+3)

                if token.type == "INT":
                    self.variables[var_name] = int(value)
                elif token.type == "FLOAT":
                    self.variables[var_name] = float(value)
                else:
                    self.variables[var_name] = str(value)

                while self.safe(tokens, i) and tokens[i].value != ";":
                    i += 1

            # 🔹 ASSIGNMENT
            elif token.type == "IDENTIFIER" and self.safe(tokens, i+1) and tokens[i+1].value == "=":
                var_name = token.value
                value = self.evaluate_expression(tokens, i+2)
                self.variables[var_name] = value

                while self.safe(tokens, i) and tokens[i].value != ";":
                    i += 1

            # 🔹 ++ / --
            elif token.type == "IDENTIFIER" and self.safe(tokens, i+1) and tokens[i+1].value in ["++", "--"]:
                var_name = token.value
                if tokens[i+1].value == "++":
                    self.variables[var_name] = self.variables.get(var_name, 0) + 1
                else:
                    self.variables[var_name] = self.variables.get(var_name, 0) - 1

                while self.safe(tokens, i) and tokens[i].value != ";":
                    i += 1

            # 🔹 PRINT
            elif token.type == "PRINT":
                val = self.evaluate_expression(tokens, i+1)
                output += str(val) + "\n"

                while self.safe(tokens, i) and tokens[i].value != ";":
                    i += 1

            # 🔹 IF / ELSE
            elif token.type == "IF":

                i += 1
                while self.safe(tokens, i) and tokens[i].value != "(":
                    i += 1
                i += 1

                cond_start = i
                while self.safe(tokens, i) and tokens[i].value != ")":
                    i += 1
                cond_end = i

                condition = self.evaluate_expression(tokens, cond_start, cond_end)
                i += 1

                while self.safe(tokens, i) and tokens[i].value != "{":
                    i += 1

                if_start = i + 1
                brace = 1
                i += 1

                while brace > 0 and self.safe(tokens, i):
                    if tokens[i].value == "{":
                        brace += 1
                    elif tokens[i].value == "}":
                        brace -= 1
                    i += 1

                if_end = i - 1

                has_else = False
                else_start = else_end = None

                if self.safe(tokens, i) and tokens[i].type == "ELSE":
                    has_else = True
                    i += 1

                    while self.safe(tokens, i) and tokens[i].value != "{":
                        i += 1

                    else_start = i + 1
                    brace = 1
                    i += 1

                    while brace > 0 and self.safe(tokens, i):
                        if tokens[i].value == "{":
                            brace += 1
                        elif tokens[i].value == "}":
                            brace -= 1
                        i += 1

                    else_end = i - 1

                if condition:
                    output += self.execute(tokens[if_start:if_end])
                elif has_else:
                    output += self.execute(tokens[else_start:else_end])

                continue

            # 🔹 FOR LOOP
            elif token.type == "FOR":
                i += 2

                init_start = i
                while self.safe(tokens, i) and tokens[i].value != ";":
                    i += 1
                self.execute(tokens[init_start:i+1])

                i += 1
                cond_start = i
                while self.safe(tokens, i) and tokens[i].value != ";":
                    i += 1
                cond_end = i

                i += 1
                update_start = i
                while self.safe(tokens, i) and tokens[i].value != ")":
                    i += 1
                update_end = i

                i += 1
                while self.safe(tokens, i) and tokens[i].value != "{":
                    i += 1

                block_start = i + 1
                brace = 1
                i += 1

                while brace > 0 and self.safe(tokens, i):
                    if tokens[i].value == "{":
                        brace += 1
                    elif tokens[i].value == "}":
                        brace -= 1
                    i += 1

                block_end = i - 1

                while self.evaluate_expression(tokens, cond_start, cond_end):
                    output += self.execute(tokens[block_start:block_end])
                    self.execute(tokens[update_start:update_end])

                continue

            i += 1

        return output

    def evaluate_expression(self, tokens, i, end=None):
        expr_parts = []

        while self.safe(tokens, i) and (end is None or i < end) and tokens[i].value not in [";", ")", "}"]:
            tok = tokens[i]

            # 🔹 IDENTIFIER
            if tok.type == "IDENTIFIER":
                val = self.variables.get(tok.value, tok.value)
                expr_parts.append(repr(val) if isinstance(val, str) else str(val))

            # 🔹 STRING
            elif tok.type == "STRING_LITERAL":
                expr_parts.append(f"'{tok.value}'")

            # 🔹 NUMBER
            elif tok.type == "NUMBER":
                expr_parts.append(tok.value)

            # 🔹 INPUT
            elif tok.type == "INPUT":
                val = self.input_values.pop(0)
                expr_parts.append(repr(val))

            # 🔹 OPERATORS
            elif tok.type == "OPERATOR":
                if tok.value == "||":
                    expr_parts.append("or")
                elif tok.value == "&&":
                    expr_parts.append("and")
                else:
                    expr_parts.append(tok.value)

            # 🔹 DOT (length)
            elif tok.type == "SEPARATOR" and tok.value == ".":
                if self.safe(tokens, i+1) and tokens[i+1].value == "length":
                    prev = expr_parts.pop()
                    expr_parts.append(f"len({prev})")
                    i += 1

            # 🔹 ARRAY INDEXING (FIXED)
            elif tok.type == "SEPARATOR" and tok.value == "[":
                i += 1
                index_parts = []

                while self.safe(tokens, i) and tokens[i].value != "]":
                    if tokens[i].type == "IDENTIFIER":
                        index_parts.append(str(self.variables.get(tokens[i].value, tokens[i].value)))
                    else:
                        index_parts.append(tokens[i].value)
                    i += 1

                index_expr = "".join(index_parts)
                prev = expr_parts.pop()

                expr_parts.append(f"({prev})[{index_expr}]")

            else:
                expr_parts.append(tok.value)

            i += 1

        try:
            return eval(" ".join(expr_parts))
        except:
            return False