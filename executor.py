class Executor:
    def __init__(self):
        self.variables = {}

    def execute(self, tokens):
        i = 0
        output = ""

        while i < len(tokens):
            token = tokens[i]

            # 🔹 VARIABLE DECLARATION
            if token.type in ["INT", "FLOAT", "STRING_TYPE"]:
                i += 1
                var_name = tokens[i].value

                i += 2  # skip =

                value = self.evaluate_expression(tokens, i)

                if token.type == "INT":
                    self.variables[var_name] = int(float(value))
                elif token.type == "FLOAT":
                    self.variables[var_name] = float(value)
                else:
                    self.variables[var_name] = str(value)

                while i < len(tokens) and tokens[i].value != ";":
                    i += 1

            # 🔹 PRINT
            elif token.type == "PRINT":
                i += 1
                value = tokens[i]

                if value.type == "IDENTIFIER":
                    output += str(self.variables.get(value.value, 0)) + "\n"
                elif value.type == "NUMBER":
                    output += value.value + "\n"
                elif value.type == "STRING":
                    output += value.value.strip('"') + "\n"

                while i < len(tokens) and tokens[i].value != ";":
                    i += 1

            i += 1

        return output

    # 🔥 EXPRESSION
    def evaluate_expression(self, tokens, i):
        result = None
        op = "+"

        while i < len(tokens) and tokens[i].value != ";":
            token = tokens[i]

            if token.type == "NUMBER":
                val = float(token.value)

            elif token.type == "IDENTIFIER":
                val = self.variables.get(token.value, 0)

            elif token.type == "INPUT":
                if not hasattr(self, "input_values") or len(self.input_values) == 0:
                    raise Exception("Not enough input values for tea ☕")

                val = self.input_values.pop(0)

                try:
                    val = float(val)
                except:
                    pass

            elif token.type == "STRING":
                val = token.value.strip('"')

            elif token.type == "OPERATOR":
                op = token.value
                i += 1
                continue

            if result is None:
                result = val
            elif op == "+":
                result += val
            elif op == "-":
                result -= val
            elif op == "*":
                result *= val
            elif op == "/":
                result = result / val

            i += 1

        return result