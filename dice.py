import random

from dice_notation import Parser

class Random:
    def __init__(self, config: dict = {'damage_bonus': '1d4'}) -> None:
        self.config = config
        self.set_damage_bonus()

    def set_damage_bonus(self, damage_bonus: str = None):
        self.damage_bonus = self.config['damage_bonus']
        if damage_bonus is not None:
            self.damage_bonus = damage_bonus

    def roll(self, dice_notation: str, damage_bonus: str = None) -> float:
        self.set_damage_bonus(damage_bonus)
        parser = Parser()
        ast = parser.parse(dice_notation)
        return self.execute(ast)

    def roll_damage_bonus(self, damage_bonus: str = None) -> float:
        self.set_damage_bonus(damage_bonus)
        return self.roll(self.damage_bonus)

    def execute(self, ast: dict, damage_bonus: str = None) -> float:
        if ast['type'] == 'stmt':
            return self.execute(ast['expression'], damage_bonus)

        elif ast['type'] == 'expr':
            left = self.execute(ast['left'], damage_bonus)
            right = self.execute(ast['right'], damage_bonus)
            if ast['operator']['operator'] == '+':
                return left + right
            elif ast['operator']['operator'] == '-':
                return left - right

        elif ast['type'] == 'term':
            left = self.execute(ast['left'], damage_bonus)
            right = self.execute(ast['right'], damage_bonus)
            if ast['operator']['operator'] == '*':
                return left * right
            elif ast['operator']['operator'] == '/':
                return left / right

        elif ast['type'] == 'dice':
            dice = Dice(ast['notation'])
            return dice.roll()

        elif ast['type'] == 'int':
            return ast['value']

        elif ast['type'] == 'damage_bonus':
            return self.roll_damage_bonus(damage_bonus)

        else:
            raise SyntaxError('kiekienokie')

class Dice:
    def __init__(self, dice_notation: str):
        dice_notation.replace('D', 'd')
        dice_data_list = dice_notation.split('d')

        self.times = int(dice_data_list[0])
        if len(dice_data_list) < 2:
            self.faces = 1
        else:
            self.faces = int(dice_data_list[1])

    def roll(self) -> int:
        result = 0
        for _ in range(self.times):
            result += random.randint(1, self.faces)
        return result
