class Token:
    def __init__(self, type, value):
        self.type = type  # INTEGER, FLOAT, PLUS, EOF
        self.value = value  # valor concreto: 2, 3.5, '+', None
    
    def __str__(self):
        """Representação em string do token para debug"""
        return f'Token({self.type}, {repr(self.value)})'
    
    def __repr__(self):
        return self.__str__()


class Interpreter:
    def __init__(self, text):
        self.text = text  # expressão de entrada
        self.pos = 0  # posição atual na string
        self.current_char = self.text[self.pos] if self.text else None
        self.current_token = None  # token atual sendo processado
    
    def error(self):
        raise Exception('Erro de interpretação')
    
    def advance(self):
        """Avança para o próximo caractere da entrada"""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self):
        """Pula todos os espaços em branco"""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def get_number(self):
        """Obtém um número inteiro ou float consecutivo da entrada"""
        result = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        
        # Verifica se é float ou integer
        if '.' in result:
            return Token('FLOAT', float(result))
        else:
            return Token('INTEGER', int(result))
    
    def get_next_token(self):
        """Analisador léxico (tokenizador)"""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit() or self.current_char == '.':
                return self.get_number()
            
            if self.current_char == '+':
                self.advance()
                return Token('PLUS', '+')
            
            self.error()
        
        return Token('EOF', None)
    
    def eat(self, token_type):
        """Verifica se o token atual é do tipo esperado e avança para o próximo"""
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()
    
    def expr(self):
        """Analisador sintático/interpretador que calcula o resultado"""
        # Inicia com o primeiro token
        self.current_token = self.get_next_token()
        
        # O primeiro token deve ser um número
        left = self.current_token
        if left.type in ('INTEGER', 'FLOAT'):
            self.eat(left.type)
        else:
            self.error()
        
        result = left.value
        
        # Processa todas as operações de soma subsequentes
        while self.current_token.type == 'PLUS':
            op = self.current_token
            self.eat('PLUS')
            
            right = self.current_token
            if right.type in ('INTEGER', 'FLOAT'):
                self.eat(right.type)
            else:
                self.error()
            
            # Realiza a operação de soma
            result += right.value
        
        return result


def main():
    while True:
        try:
            text = input('calc> ').strip()
            
            # Verifica se o usuário quer sair
            if text.lower() in ('sair', 'exit', 'quit'):
                print("Saindo do programa...")
                break
                
            if not text:
                continue
            
            interpreter = Interpreter(text)
            result = interpreter.expr()
            print('Resultado:', result)
            
        except Exception as e:
            print(f"Erro: {e}")


if __name__ == '__main__':
    main()