from thetokens import Token 

KEYWORDS = {
    "sigma": "INT",
    "drip": "FLOAT",
    "dm": "STRING",
    "vibeCheck": "IF",
    "vibeFlop": "ELSE",
    "spill": "PRINT",
    "tea": "INPUT",
    "spam": "FOR"
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

            # STRING
            if current == '"':
                self.pos += 1
                start = self.pos
                while self.text[self.pos] != '"':
                    self.pos += 1
                value = self.text[start:self.pos]
                tokens.append(Token("STRING_LITERAL", value, self.line))
                self.pos += 1
                continue

            # IDENTIFIER / KEYWORD
            if current.isalpha():
                start = self.pos
                while self.pos < len(self.text) and self.text[self.pos].isalnum():
                    self.pos += 1
                word = self.text[start:self.pos]
                tokens.append(Token(KEYWORDS.get(word, "IDENTIFIER"), word, self.line))
                continue

            # NUMBER (float supported)
            if current.isdigit():
                start = self.pos
                while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == "."):
                    self.pos += 1
                tokens.append(Token("NUMBER", self.text[start:self.pos], self.line))
                continue

            # OPERATORS
            if current in "+-*/%":
                tokens.append(Token("OPERATOR", current, self.line))
                self.pos += 1
                continue

            if current in "=<>!":
                if self.pos+1 < len(self.text) and self.text[self.pos+1] == "=":
                    tokens.append(Token("OPERATOR", self.text[self.pos:self.pos+2], self.line))
                    self.pos += 2
                else:
                    tokens.append(Token("OPERATOR", current, self.line))
                    self.pos += 1
                continue

            if current == "|" and self.pos+1 < len(self.text) and self.text[self.pos+1] == "|":
                tokens.append(Token("OPERATOR", "||", self.line))
                self.pos += 2
                continue

            if current in "(){};,":
                tokens.append(Token("SEPARATOR", current, self.line))
                self.pos += 1
                continue

            tokens.append(Token("UNKNOWN", current, self.line))
            self.pos += 1

        tokens.append(Token("EOF", None, self.line))
        return tokens