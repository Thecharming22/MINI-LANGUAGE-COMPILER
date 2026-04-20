class Executor:
    def __init__(self, input_values=None):
        self.variables = {}
        self.input_values = input_values or []

    def execute(self, tokens):
        i = 0
        output = ""
        print("EXECUTOR STARTED")

        while i < len(tokens):
            token = tokens[i]

            # 🔹 DECLARATION
            if token.type in ["INT", "FLOAT", "STRING"]:
                var_name = tokens[i+1].value
                value = self.evaluate_expression(tokens, i+3)
                if token.type == "INT":
                    self.variables[var_name] = int(value)
                elif token.type == "FLOAT":
                    self.variables[var_name] = float(value)
                else:
                    self.variables[var_name] = str(value)
                while i < len(tokens) and tokens[i].value != ";":
                    i += 1

            # 🔹 ASSIGNMENT
            elif token.type == "IDENTIFIER" and i+1 < len(tokens) and tokens[i+1].value == "=":
                var_name = token.value
                value = self.evaluate_expression(tokens, i+2)
                self.variables[var_name] = value
                while i < len(tokens) and tokens[i].value != ";":
                    i += 1

            # 🔹 Increment/Decrement
            elif token.type == "IDENTIFIER" and i+1 < len(tokens) and tokens[i+1].type == "OPERATOR" and tokens[i+1].value in ["++", "--"]:
                var_name = token.value
                if tokens[i+1].value == "++":
                    self.variables[var_name] = self.variables.get(var_name, 0) + 1
                else:
                    self.variables[var_name] = self.variables.get(var_name, 0) - 1
                while i < len(tokens) and tokens[i].value != ";":
                    i += 1

            # 🔹 PRINT
            elif token.type == "PRINT":
                val = self.evaluate_expression(tokens, i+1)
                output += str(val) + "\n"
                while i < len(tokens) and tokens[i].value != ";":
                    i += 1

            # 🔹 IF / ELSE
            elif token.type == "IF":
                i += 1
                while tokens[i].value != "(":
                    i += 1
                i += 1
                cond_start = i
                while tokens[i].value != ")":
                    i += 1
                cond_end = i
                condition = self.evaluate_expression(tokens, cond_start, cond_end)
                i += 1

                # find IF block
                while tokens[i].value != "{":
                    i += 1
                block_start = i+1
                brace = 1
                i += 1
                while brace > 0 and i < len(tokens):
                    if tokens[i].value == "{":
                        brace += 1
                    elif tokens[i].value == "}":
                        brace -= 1
                    i += 1
                block_end = i-1

                if condition:
                    output += self.execute(tokens[block_start:block_end])
                    # skip ELSE block if present
                    if i < len(tokens) and tokens[i].type == "ELSE":
                        while tokens[i].value != "{":
                            i += 1
                        brace = 1
                        i += 1
                        while brace > 0 and i < len(tokens):
                            if tokens[i].value == "{":
                                brace += 1
                            elif tokens[i].value == "}":
                                brace -= 1
                            i += 1
                else:
                    # execute ELSE block if present
                    if i < len(tokens) and tokens[i].type == "ELSE":
                        i += 1
                        while tokens[i].value != "{":
                            i += 1
                        else_block_start = i+1
                        brace = 1
                        i += 1
                        while brace > 0 and i < len(tokens):
                            if tokens[i].value == "{":
                                brace += 1
                            elif tokens[i].value == "}":
                                brace -= 1
                            i += 1
                        else_block_end = i-1
                        output += self.execute(tokens[else_block_start:else_block_end])
                continue

            # 🔹 FOR LOOP
            elif token.type == "FOR":
                i += 2  # skip FOR (
                # init statement until ;
                init_start = i
                while tokens[i].value != ";":
                    i += 1
                init_end = i
                self.execute(tokens[init_start:init_end+1])
                i += 1
                # condition until ;
                cond_start = i
                while tokens[i].value != ";":
                    i += 1
                cond_end = i
                i += 1
                # update until )
                update_start = i
                while tokens[i].value != ")":
                    i += 1
                update_end = i
                i += 1
                # block
                while tokens[i].value != "{":
                    i += 1
                block_start = i+1
                brace = 1
                i += 1
                while brace > 0 and i < len(tokens):
                    if tokens[i].value == "{":
                        brace += 1
                    elif tokens[i].value == "}":
                        brace -= 1
                    i += 1
                block_end = i-1
                # loop execution
                while self.evaluate_expression(tokens, cond_start, cond_end):
                    output += self.execute(tokens[block_start:block_end])
                    self.execute(tokens[update_start:update_end])
                continue

            i += 1

        return output

    def evaluate_expression(self, tokens, i, end=None):
        expr_parts = []
        while i < len(tokens) and (end is None or i < end) and tokens[i].value not in [";", ")", "}"]:
            tok = tokens[i]
            if tok.type == "IDENTIFIER":
                if tok.value in self.variables:
                    val = self.variables[tok.value]
                    if isinstance(val, str):
                        expr_parts.append(repr(val))
                    else:
                        expr_parts.append(str(val))
                else:
                    expr_parts.append(tok.value)
            elif tok.type == "STRING_LITERAL":
                expr_parts.append(repr(tok.value))
            elif tok.type == "NUMBER":
                if "." in tok.value:
                    expr_parts.append(str(float(tok.value)))
                else:
                    expr_parts.append(str(int(tok.value)))
            elif tok.type == "INPUT":
                val = self.input_values.pop(0)
                if isinstance(val, str) and val.isdigit():
                    expr_parts.append(str(int(val)))
                else:
                    expr_parts.append(repr(val))
            elif tok.type == "OPERATOR":
                if tok.value == "||":
                    expr_parts.append("or")
                elif tok.value == "&&":
                    expr_parts.append("and")
                else:
                    expr_parts.append(tok.value)
            else:
                expr_parts.append(tok.value)
            i += 1

        expr_str = " ".join(expr_parts)
        try:
            return eval(expr_str)
        except Exception:
            return False
