def reduce(callback: callable, reduce_list: list, initial_value: dict = None) -> dict:
    # callback(acc,cur)
    if initial_value is not None:
        reduce_list.insert(0, initial_value)
    acc = reduce_list[0]
    for cur in reduce_list[1:]:
        acc = callback(acc, cur)
    return acc

#トークンの種類を定義
class TokenType:
    DIGITS = 'DIGITS'
    DAMAGE_BONUS = 'DAMAGE_BONUS'
    DICE = 'DICE'
    EXPR_OPERATOR = 'EXPR_OPERATOR'
    TERM_OPERATOR = 'TERM_OPERATOR'

# トークンの種類と値を合わせてもっとく
class Token:
    def __init__(self, token_type: TokenType, value: str):
        self.type = token_type
        self.value = value

# すべてのトークンのクラスをつくる

class DigitsToken(Token):
    def __init__(self, value: str):
        super().__init__(TokenType.DIGITS, value)

class DamageBonusToken(Token):
    def __init__(self):
        super().__init__(TokenType.DAMAGE_BONUS, 'DB')

class DiceToken(Token):
    def __init__(self, value: str):
        super().__init__(TokenType.DICE, value)

class ExprOperatorToken(Token):
    def __init__(self, value: str):
        super().__init__(TokenType.EXPR_OPERATOR, value)

class TermOperatorToken(Token):
    def __init__(self, value: str):
        super().__init__(TokenType.TERM_OPERATOR, value)

# とーくないざーをつくる
class Tokenizer:
    def __init__(self):
        self.statement = ''

    def get(self, n: int = 1) -> str:
        ch = None
        for _ in range(n):
            ch = self.statement[0]
            self.statement = self.statement[1:]
        return ch

    def unget(self, ch: str):
        self.statement = ch + self.statement

    def peek(self, n: int = 1) -> str:
        tnp = []
        for _ in range(n):
            tnp.append(self.get())
        top = tnp[n - 1]
        for _ in range(n):
            self.unget(tnp.pop())
        return top

    def can_peek(self, n: int = 1) -> bool:
        return len(self.statement) >= n

    def is_digits(self) -> bool:
        return self.can_peek() and self.peek() in [str(x) for x in range(10)]

    def is_damage_bonus(self) -> bool:
        return self.can_peek(2) and self.peek() + self.peek(2) in ['DB', 'db', 'Db', 'dB']

    def is_dice(self) -> bool:
        count = 1
        flag = False
        while self.can_peek(count) and self.peek(count) in [str(x) for x in range(10)]:
            count += 1
            flag = True
        if self.can_peek(count) and self.peek(count) not in ['d', 'D']:
            return False
        count += 1
        return self.can_peek(count) and self.peek(count) in [str(x) for x in range(10)] and flag

    def is_expr_operator(self) -> bool:
        return self.can_peek() and self.peek() in ['+', '-']

    def is_term_operator(self) -> bool:
        return self.can_peek() and self.peek() in ['*', '/']


    def get_digits(self) -> DigitsToken:
        value = ''
        while self.can_peek() and self.peek() in [str(x) for x in range(10)]:
            value += self.get()
        return DigitsToken(value)

    def get_damage_bonus(self) -> DamageBonusToken:
        self.get(2)
        return DamageBonusToken()

    def get_dice(self) -> DiceToken:
        value = self.get_digits().value
        value += 'd'
        self.get()
        value += self.get_digits().value
        return DiceToken(value)

    def get_expr_operator(self) -> ExprOperatorToken:
        value = self.get()
        return ExprOperatorToken(value)

    def get_term_operator(self) -> TermOperatorToken:
        value = self.get()
        return TermOperatorToken(value)

    def tokenize(self, statement: str) -> list:
        self.statement = statement
        result = []
        while len(self.statement) > 0:
            while self.can_peek() and self.peek() in [' ']:
                self.get()
            if self.is_dice():
                result.append(self.get_dice())
            elif self.is_damage_bonus():
                result.append(self.get_damage_bonus())
            elif self.is_digits():
                result.append(self.get_digits())
            elif self.is_expr_operator():
                result.append(self.get_expr_operator())
            elif self.is_term_operator():
                result.append(self.get_term_operator())
            else:
                raise SyntaxError('Token mismatch')
        return result

# ぱーさーをつくる

class NodeType:
    DAMAGE_BONUS = 'damage_bonus'
    DICE = 'dice'
    INT = 'int'
    TERM = 'term'
    EXPR = 'expr'
    STMT = 'stmt'
    TERM_OPERATOR = 'term_operator'
    EXPR_OPERATOR = 'expr_operator'
    FACTOR = 'factor'

class Environment:
    def __init__(self, token_list: list):
        self.token_list = token_list

    def get(self, n: int = 1) -> Token:
        if n <= 0:
            raise ValueError ('nは1以上でなくてはなりません')
        token = self.token_list[n - 1]
        self.token_list = self.token_list[n:]
        return token

    def unget(self, token: Token) -> None:
        self.token_list[0:0] = [token]

    def peek(self, n: int = 1) -> Token:
        tmp = []
        top = None
        for _ in range(n):
            tmp.append(self.get())
        top = tmp[len(tmp) - 1]
        for _ in range(n):
            self.unget(tmp.pop())
        return top

    def can_peek(self, n: int = 1) -> bool:
        return len(self.token_list) >= n

class Node:
    def __init__(self, node_type: NodeType, env: Environment):
        self.type = node_type
        self.env = env

    @staticmethod
    def is_first(token: Token) -> bool:
        return False

    def parse(self) -> dict:
        return None

class DamageBonusNode(Node):
    def __init__(self, env: Environment):
        super().__init__(NodeType.DAMAGE_BONUS, env)

    @staticmethod
    def is_first(token: Token) -> bool:
        return type(token) == DamageBonusToken

    def parse(self) -> dict:
        self.env.get()
        return { 'type': self.type }

class DiceNode(Node):
    def __init__(self, env: Environment):
        super().__init__(NodeType.DICE, env)

    @staticmethod
    def is_first(token: Token) -> bool:
        return type(token) == DiceToken

    def parse(self) -> dict:
        return { 'type': self.type, 'notation': self.env.get().value }

class IntNode(Node):
    def __init__(self, env: Environment):
        super().__init__(NodeType.INT, env)

    @staticmethod
    def is_first(token: Token) -> bool:
        return type(token) == DigitsToken

    def parse(self) -> dict:
        return { 'type': self.type, 'value': int(self.env.get().value) }

class TermOperatorNode(Node):
    def __init__(self, env: Environment):
        super().__init__(NodeType.TERM_OPERATOR, env)

    @staticmethod
    def is_first(token: Token) -> bool:
        return type(token) == TermOperatorToken

    def parse(self) -> dict:
        return { 'type': self.type, 'operator': self.env.get().value }

class ExprOperatorNode(Node):
    def __init__(self, env: Environment):
        super().__init__(NodeType.EXPR_OPERATOR, env)

    @staticmethod
    def is_first(token: Token) -> bool:
        return type(token) == ExprOperatorToken

    def parse(self) -> dict:
        return { 'type': self.type, 'operator': self.env.get().value }

class FactorNode(Node):
    def __init__(self, env: Environment):
        super().__init__(NodeType.FACTOR, env)

    @staticmethod
    def is_first(token: Token) -> bool:
        return type(token) in [DiceToken, DigitsToken, DamageBonusToken]

    def parse(self) -> dict:
        if self.env.can_peek():
            token = self.env.peek()
            node = None
            if DamageBonusNode.is_first(token):
                node = DamageBonusNode(self.env)
            elif DiceNode.is_first(token):
                node = DiceNode(self.env)
            elif IntNode.is_first(token):
                node = IntNode(self.env)
            else:
                raise ValueError('nodeの中身が違うよ')
            return node.parse()

class TermNode(Node):
    def __init__(self, env: Environment):
        super().__init__(NodeType.TERM, env)

    @staticmethod
    def is_first(token: Token) -> bool:
        return FactorNode.is_first(token)

    def parse(self) -> dict:
        if not self.env.can_peek():
            raise SyntaxError('ピークできなかったよ')
        token = self.env.peek()
        if not FactorNode.is_first(token):
            raise SyntaxError('unk')
        left_node = FactorNode(self.env)
        left = left_node.parse()
        right_list = []
        while self.env.can_peek() and TermOperatorNode.is_first(self.env.peek()):
            operator_node = TermOperatorNode(self.env)
            operator = operator_node.parse()
            if not self.env.can_peek():
                raise SyntaxError('unti')
            elif not FactorNode.is_first(self.env.peek()):
                raise SyntaxError('unnti')
            right_node = FactorNode(self.env)
            right = right_node.parse()
            right_list.append({ 'operator': operator, 'right': right })
        return reduce(lambda acc, cur: {
            'type': 'term',
            'left': acc,
            'right': cur['right'],
            'operator': cur['operator'],
        }, right_list, left)

class ExprNode(Node):
    def __init__(self, env: Environment):
        super().__init__(NodeType.EXPR, env)

    @staticmethod
    def is_first(token: Token) -> bool:
        return TermNode.is_first(token)

    def parse(self) -> dict:
        if not self.env.can_peek():
            raise SyntaxError('ピークできなかったよ')
        token = self.env.peek()
        if not TermNode.is_first(token):
            raise SyntaxError('unk')
        left_node = TermNode(self.env)
        left = left_node.parse()
        right_list = []
        while self.env.can_peek() and ExprOperatorNode.is_first(self.env.peek()):
            operator_node = ExprOperatorNode(self.env)
            operator = operator_node.parse()
            if not self.env.can_peek():
                raise SyntaxError('unti')
            elif not TermNode.is_first(self.env.peek()):
                raise SyntaxError('unnti')
            right_node = TermNode(self.env)
            right = right_node.parse()
            right_list.append({ 'operator': operator, 'right': right })
        return reduce(lambda acc, cur: {
            'type': 'expr',
            'left': acc,
            'right': cur['right'],
            'operator': cur['operator'],
        }, right_list, left)

class StmtNode(Node):
    def __init__(self, env: Environment):
        super().__init__(NodeType.STMT, env)

    @staticmethod
    def is_first(token: Token) -> bool:
        return type(token) in [DiceToken, DamageBonusToken, DigitsToken]

    def parse(self) -> dict:
        if not self.env.can_peek():
            raise SyntaxError('ピークできなかったよ')
        token = self.env.peek()
        if ExprNode.is_first(token):
            node = ExprNode(self.env)
            return { 'type': self.type, 'expression': node.parse() }
        else:
            raise SyntaxError('入力が間違っています')

class Parser:
    def __init__(self):
        pass

    def parse(self, src: str) -> dict: # envを呼んできて仕事してもらう
        tokenizer = Tokenizer()
        token_list = tokenizer.tokenize(src)
        env = Environment(token_list)
        if not env.can_peek():
            raise SyntaxError('ピークできなかったよ')
        token = env.peek()
        if StmtNode.is_first(token):
            node = StmtNode(env)
            return node.parse()
        else:
            raise SyntaxError('入力が間違っています')
