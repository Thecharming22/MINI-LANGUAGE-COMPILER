class Executor:
    def __init__(self, inputs=None):
        self.vars = {}
        self.inputs = inputs or []

    def run(self, node):
        if node[0] == "PROGRAM":
            output = ""
            for stmt in node[1]:
                res = self.run(stmt)
                if res:
                    output += res
            return output

        elif node[0] == "DECL":
            _, type_, name, expr = node
            value = self.eval(expr) if expr else None

            if type_ == "INT":
                value = int(value)
            elif type_ == "FLOAT":
                value = float(value)
            elif type_ == "STRING":
                value = str(value)

            self.vars[name] = value

        elif node[0] == "ASSIGN":
            _, name, expr = node
            self.vars[name] = self.eval(expr)

        elif node[0] == "UPDATE":
            _, name, op = node
            if op == "++":
                self.vars[name] += 1
            else:
                self.vars[name] -= 1

        elif node[0] == "PRINT":
            return str(self.eval(node[1])) + "\n"

        elif node[0] == "IF":
            _, cond, if_block, else_block = node
            if self.eval(cond):
                return self.exec_block(if_block)
            elif else_block:
                return self.exec_block(else_block)

        elif node[0] == "FOR":
            _, init, cond, update, block = node

            self.run(init)
            output = ""

            while self.eval(cond):
                output += self.exec_block(block)
                self.run(update)

            return output

    def exec_block(self, block):
        output = ""
        for stmt in block:
            res = self.run(stmt)
            if res:
                output += res
        return output

    # ---------------- EXPRESSIONS ----------------

    def eval(self, node):
        if node is None:
            return None

        if node[0] == "NUM":
            return node[1]

        elif node[0] == "STR":
            return node[1]

        elif node[0] == "VAR":
            return self.vars.get(node[1], 0)

        elif node[0] == "INPUT":
            return self.inputs.pop(0)

        elif node[0] == "BINOP":
            _, op, left, right = node
            l = self.eval(left)
            r = self.eval(right)

            if op == "+": return l + r
            if op == "-": return l - r
            if op == "*": return l * r
            if op == "/": return l / r
            if op == "%": return l % r

            if op == "==": return l == r
            if op == "!=": return l != r
            if op == "<": return l < r
            if op == ">": return l > r
            if op == "<=": return l <= r
            if op == ">=": return l >= r

            if op == "&&": return l and r
            if op == "||": return l or r
        elif node[0] == "PROP":
            _, obj, prop = node

            value = self.eval(obj)

            if prop == "length":
                if isinstance(value, str):
                    return len(value)
                else:
                    raise Exception(f".length not supported on type {type(value)}")

            else:
                raise Exception(f"Unknown property '{prop}'")
        elif node[0] == "INDEX":
            _, obj, index_node = node

            value = self.eval(obj)
            index = self.eval(index_node)

            try:
                return value[int(index)]
            except:
                raise Exception(f"Invalid index access on {value}")