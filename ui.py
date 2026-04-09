from flask import Flask, render_template, request
from lexer import Lexer

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    code = ""  

    if request.method == "POST":
        code = request.form["code"]

        lex = Lexer(code)
        tokens = lex.tokenize()

        output = "\n".join(str(t) for t in tokens)

    return render_template("index.html", output=output, code=code)

if __name__ == "__main__":
    app.run(debug=True)