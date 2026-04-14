from flask import Flask, render_template, request
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

            output = "Parsing Successful! No syntax errors found.\n\n"
            output += "--- TOKENS ---\n"
            output += "\n".join(str(t) for t in tokens)

            status = "success"

        except Exception as e:
            output = str(e)
            status = "error"

    return render_template("index.html", output=output, code=code, status=status)


if __name__ == "__main__":
    app.run(debug=True)