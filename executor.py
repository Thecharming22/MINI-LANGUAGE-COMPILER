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
                    self.variables[var_name] = int(float(value))
                elif token.type == "FLOAT":
                    self.variables[var_name] = float(value)
                else:
                    self.variables[var_name] = str(value)

                while tokens[i].value != ";":
                    i += 1

            # 🔹 ASSIGNMENT
            elif token.type == "IDENTIFIER" and tokens[i+1].value == "=":
                var_name = token.value
                value = self.evaluate_expression(tokens, i+2)
                self.variables[var_name] = value
                while tokens[i].value != ";":
                    i += 1

            # 🔹 PRINT
            elif token.type == "PRINT":
                val = tokens[i+1]
                if val.type == "IDENTIFIER":
                    output += str(self.variables.get(val.value, 0)) + "\n"
                elif val.type == "NUMBER":
                    output += val.value + "\n"
                elif val.type == "STRING_LITERAL":
                    output += val.value + "\n"
                while tokens[i].value != ";":
                    i += 1

            # 🔥 FOR LOOP
            elif token.type == "FOR":
                # skip "FOR ("
                i += 2

                # init statement
                self.execute([tokens[i], tokens[i+1], tokens[i+2], tokens[i+3], tokens[i+4]])
                while tokens[i].value != ";":
                    i += 1
                i += 1

                # condition start
                cond_start = i
                while tokens[i].value != ";":
                    i += 1
                cond_end = i
                i += 1

                # update start
                update_start = i
                while tokens[i].value != ")":
                    i += 1
                update_end = i
                i += 1

                # block start
                while tokens[i].value != "{":
                    i += 1
                block_start = i+1

                brace = 1
                i += 1
                while brace > 0:
                    if tokens[i].value == "{":
                        brace += 1
                    elif tokens[i].value == "}":
                        brace -= 1
                    i += 1
                block_end = i-1

                # loop execution
                while self.evaluate_expression(tokens, cond_start, cond_end):
                    self.execute(tokens[block_start:block_end])
                    self.execute(tokens[update_start:update_end])

                continue

            i += 1

        return output

    def evaluate_expression(self, tokens, i, end=None):
        # Shunting-yard style simple precedence
        def get_val(tok):
            if tok.type == "NUMBER":
                return float(tok.value)
            elif tok.type == "IDENTIFIER":
                return self.variables.get(tok.value, 0)
            elif tok.type == "INPUT":
                val = self.input_values.pop(0)
                try:
                    return float(val)
                except:
                    return val
            elif tok.type == "STRING_LITERAL":
                return tok.value
            return None

        values = []
        ops = []

        while i < len(tokens) and (end is None or i < end) and tokens[i].value not in [";", ")", "}"]:
            tok = tokens[i]
            if tok.type in ["NUMBER", "IDENTIFIER", "INPUT", "STRING_LITERAL"]:
                values.append(get_val(tok))
            elif tok.type == "OPERATOR":
                ops.append(tok.value)
            i += 1

        # naive left-to-right evaluation with precedence for */%
        j = 0
        while j < len(ops):
            if ops[j] in ["*", "/", "%"]:
                a = values[j]
                b = values[j+1]
                if ops[j] == "*": values[j] = a * b
                elif ops[j] == "/": values[j] = a / b
                elif ops[j] == "%": values[j] = a % b
                values.pop(j+1)
                ops.pop(j)
            else:
                j += 1

        # now handle +, -
        result = values[0]
        for k, op in enumerate(ops):
            if op == "+": result += values[k+1]
            elif op == "-": result -= values[k+1]
            elif op == "==": result = (result == values[k+1])
            elif op == "!=": result = (result != values[k+1])
            elif op == "<": result = (result < values[k+1])
            elif op == ">": result = (result > values[k+1])
            elif op == "<=": result = (result <= values[k+1])
            elif op == ">=": result = (result >= values[k+1])

        return result
