from executor import Executor
from flask import Flask, render_template, request, jsonify
from lexer import Lexer
from parser import Parser

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    code = ""
    status = None

    if request.method == "POST":
        code = request.form["code"]

        lex = Lexer(code)
        tokens = lex.tokenize()

        try:
            parser = Parser(tokens)
            parser.parse()

            # Check if 'tea' is present in tokens
            needs_input = any(tok.type == "INPUT" for tok in tokens)

            executor = Executor()

            if needs_input:
                # Agar tea detect hua toh user_input field dikhana
                user_input = request.form.get("user_input")
                if not user_input:
                    return render_template("index.html",
                                           output="Program requires input (tea). Please enter values.",
                                           code=code,
                                           status="input_needed")
                executor.input_values = [x.strip() for x in user_input.split(",")]

            result = executor.execute(tokens)

            output = "Parsing Successful! No syntax errors found.\n\n"
            output += "--- OUTPUT ---\n"
            output += result
            status = "success"

        except Exception as e:
            output = str(e)
            status = "error"

    return render_template("index.html", output=output, code=code, status=status)


if __name__ == "__main__":
    app.run(debug=True)
