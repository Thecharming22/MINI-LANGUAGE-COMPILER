from token import Token 
KEYWORDS= {
    "sigma": "INT",
    "vibeCheck": "IF",
    "vibeFlop": "ELSE",
    "spill": "PRINT",
    "greenFlag": "TRUE",
    "redFlag": "FALSE",
    "holdUp": "BREAK",
    "alsoCheck": "ELSEIF",
    "keepGoin": "CONTINUE",
    "drip": "FLOAT",
    "tea": "INPUT",
    "slayWhile": "WHILE",
    "spam": "FOR",
    "alpha": "CHAR",
    "sus": "BOOLEAN",
    "dm": "STRING"
}
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1

    def tokenize(self):
        tokens = []

        while self.pos < len(self.text):
            current = self.text[self.pos]
            if current == '\n':
                self.line += 1
                self.pos += 1
                continue
            
            if current.isspace():
                self.pos += 1
                continue

            if current.isalpha():
                start = self.pos
                while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == "_"):
                    self.pos += 1
                word = self.text[start:self.pos]
                if word in KEYWORDS:
                    tokens.append(Token(KEYWORDS[word],word,self.line))
                else:
                    tokens.append(Token("IDENTIFIER",word,self.line))
                continue

            if current.isdigit():
                start = self.pos
                while self.pos < len(self.text) and self.text[self.pos].isdigit():
                    self.pos += 1
                number = self.text[start:self.pos]
                tokens.append(Token("NUMBER", number,self.line))
                continue

            if current in "+-*/%":
                tokens.append(Token("OPERATOR", current, self.line))
                self.pos += 1
                continue

            if current in "=<>!":
                if self.pos+1 < len(self.text) and self.text[self.pos+1] == "=":
                    two_char = self.text[self.pos:self.pos+2]
                    tokens.append(Token("OPERATOR", two_char, self.line))
                    self.pos += 2
                else:
                    tokens.append(Token("OPERATOR", current, self.line))
                    self.pos += 1
                continue

            if current in "(){};,":
                tokens.append(Token("SEPARATOR", current, self.line))
                self.pos += 1
                continue

            tokens.append(Token("UNKNOWN", current,self.line))
            self.pos += 1
        tokens.append(Token("EOF", None, self.line))
        return tokens
