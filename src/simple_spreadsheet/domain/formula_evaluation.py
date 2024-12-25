class Tokenizer:
    def __init__(self) -> None:
        self.__tokens = []

    def _preprocess(self, expression) -> None:
        expression = expression.replace(' ', '')
        return expression

    def tokenize(self, expression) -> list[str]:
        self.__tokens = []
        expression = self._preprocess(expression)
        n = len(expression)
        i = 0
        while i < n:
            if expression[i].isdigit():
                num = ''
                while i < n and expression[i].isdigit():
                    num += expression[i]
                    i += 1
                self.__tokens.append(num)
            elif expression[i].isalpha():
                var = ''
                while i < n and expression[i].isalpha() or expression[i].isdigit():
                    var += expression[i]
                    i += 1
                self.__tokens.append(var)
            elif expression[i] in ['+', '-', '*', '/', '(', ')', ':', ';']:
                self.__tokens.append(expression[i])
                i += 1
            else:
                raise ValueError('Invalid character')
        return self.__tokens

    def get_tokens(self) -> list[str]:
        return self.__tokens


tk = Tokenizer()
tk.tokenize('A1 + 2 * 3')