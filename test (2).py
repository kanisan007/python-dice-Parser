from dice_notation import Parser
from dice import Random

class Test:
    passed = 0
    failed = 0
    @staticmethod
    def init():
        Test.passed = 0
        Test.faild = 0
    @staticmethod
    def test(tester: any, name: str, src: str, result: list) -> bool:
        tester(name, src, result)
    @staticmethod
    def print_result():
        print(f'Passed: {Test.passed}, Failed: {Test.faild}')
    @staticmethod
    def parse_test(name: str, src: str, result: list) -> bool:
        parser = Parser()
        parsed = str(parser.parse(src))
        if result[0] == parsed:
            print(f'\t{name}\t: passed')
            Test.passed += 1
        else:
            print(f'\t{name}\t: failed {parsed}')
            Test.faild += 1
    @staticmethod
    def execute_test(name: str, src: str, result: list) -> bool:
        parser = Parser()
        random = Random()
        if len(result) == 1:
            executed = random.execute(parser.parse(src))
            if result[0] == executed:
                print(f'\t{name}\t: passed')
                Test.passed += 1
            else:
                print(f'\t{name}\t: failed {executed}')
                Test.faild += 1
        else:
            executed = random.execute(parser.parse(src))
            print(executed)
            if result[0] <= executed and executed <= result[1]:
                print(f'\t{name}\t: passed')
                Test.passed += 1
            else:
                print(f'\t{name}\t: failed {executed}')
                Test.faild += 1

Test.init()
Test.test(Test.parse_test, '1', '1', ["{'type': 'stmt', 'expression': {'type': 'int', 'value': 1}}"])
Test.test(Test.parse_test, '10', '10', ["{'type': 'stmt', 'expression': {'type': 'int', 'value': 10}}"])
Test.test(Test.parse_test, '1d20', '1d20', ["{'type': 'stmt', 'expression': {'type': 'dice', 'notation': '1d20'}}"])
Test.test(Test.parse_test, '1D20', '1D20', ["{'type': 'stmt', 'expression': {'type': 'dice', 'notation': '1d20'}}"])
Test.test(Test.parse_test, 'DB', 'DB', ["{'type': 'stmt', 'expression': {'type': 'damage_bonus'}}"])
Test.test(Test.parse_test, 'db', 'db', ["{'type': 'stmt', 'expression': {'type': 'damage_bonus'}}"])
Test.test(Test.parse_test, '1+1', '1+1', ["{'type': 'stmt', 'expression': {'type': 'expr', 'left': {'type': 'int', 'value': 1}, 'right': {'type': 'int', 'value': 1}, 'operator': {'type': 'expr_operator', 'operator': '+'}}}"])
Test.test(Test.parse_test, '1+1d20', '1+1d20', ["{'type': 'stmt', 'expression': {'type': 'expr', 'left': {'type': 'int', 'value': 1}, 'right': {'type': 'dice', 'notation': '1d20'}, 'operator': {'type': 'expr_operator', 'operator': '+'}}}"])
Test.test(Test.parse_test, '1+DB', '1+DB', ["{'type': 'stmt', 'expression': {'type': 'expr', 'left': {'type': 'int', 'value': 1}, 'right': {'type': 'damage_bonus'}, 'operator': {'type': 'expr_operator', 'operator': '+'}}}"])
Test.test(Test.parse_test, '1d20+1', '1d20+1', ["{'type': 'stmt', 'expression': {'type': 'expr', 'left': {'type': 'dice', 'notation': '1d20'}, 'right': {'type': 'int', 'value': 1}, 'operator': {'type': 'expr_operator', 'operator': '+'}}}"])
Test.test(Test.parse_test, '1d20+1d20', '1d20+1d20', ["{'type': 'stmt', 'expression': {'type': 'expr', 'left': {'type': 'dice', 'notation': '1d20'}, 'right': {'type': 'dice', 'notation': '1d20'}, 'operator': {'type': 'expr_operator', 'operator': '+'}}}"])
Test.test(Test.parse_test, '1d20+DB', '1d20+DB', ["{'type': 'stmt', 'expression': {'type': 'expr', 'left': {'type': 'dice', 'notation': '1d20'}, 'right': {'type': 'damage_bonus'}, 'operator': {'type': 'expr_operator', 'operator': '+'}}}"])
Test.test(Test.parse_test, 'DB+1', 'DB+1', ["{'type': 'stmt', 'expression': {'type': 'expr', 'left': {'type': 'damage_bonus'}, 'right': {'type': 'int', 'value': 1}, 'operator': {'type': 'expr_operator', 'operator': '+'}}}"])
Test.test(Test.parse_test, 'DB+1d20', 'DB+1d20', ["{'type': 'stmt', 'expression': {'type': 'expr', 'left': {'type': 'damage_bonus'}, 'right': {'type': 'dice', 'notation': '1d20'}, 'operator': {'type': 'expr_operator', 'operator': '+'}}}"])
Test.test(Test.parse_test, 'DB+DB', 'DB+DB', ["{'type': 'stmt', 'expression': {'type': 'expr', 'left': {'type': 'damage_bonus'}, 'right': {'type': 'damage_bonus'}, 'operator': {'type': 'expr_operator', 'operator': '+'}}}"])
Test.test(Test.parse_test, '1d20+1+DB', '1d20+1+DB', ["{'type': 'stmt', 'expression': {'type': 'expr', 'left': {'type': 'expr', 'left': {'type': 'dice', 'notation': '1d20'}, 'right': {'type': 'int', 'value': 1}, 'operator': {'type': 'expr_operator', 'operator': '+'}}, 'right': {'type': 'damage_bonus'}, 'operator': {'type': 'expr_operator', 'operator': '+'}}}"])
Test.test(Test.parse_test, '1+1+1+1+1+1+1+1', '1+1+1+1+1+1+1+1', ["{'type': 'stmt', 'expression': {'type': 'expr', 'left': {'type': 'expr', 'left': {'type': 'expr', 'left': {'type': 'expr', 'left': {'type': 'expr', 'left': {'type': 'expr', 'left': {'type': 'expr', 'left': {'type': 'int', 'value': 1}, 'right': {'type': 'int', 'value': 1}, 'operator': {'type': 'expr_operator', 'operator': '+'}}, 'right': {'type': 'int', 'value': 1}, 'operator': {'type': 'expr_operator', 'operator': '+'}}, 'right': {'type': 'int', 'value': 1}, 'operator': {'type': 'expr_operator', 'operator': '+'}}, 'right': {'type': 'int', 'value': 1}, 'operator': {'type': 'expr_operator', 'operator': '+'}}, 'right': {'type': 'int', 'value': 1}, 'operator': {'type': 'expr_operator', 'operator': '+'}}, 'right': {'type': 'int', 'value': 1}, 'operator': {'type': 'expr_operator', 'operator': '+'}}, 'right': {'type': 'int', 'value': 1}, 'operator': {'type': 'expr_operator', 'operator': '+'}}}"])
Test.test(Test.parse_test, '1*1/1', '1*1/1', ["{'type': 'stmt', 'expression': {'type': 'term', 'left': {'type': 'term', 'left': {'type': 'int', 'value': 1}, 'right': {'type': 'int', 'value': 1}, 'operator': {'type': 'term_operator', 'operator': '*'}}, 'right': {'type': 'int', 'value': 1}, 'operator': {'type': 'term_operator', 'operator': '/'}}}"])
Test.test(Test.parse_test, '1*1', '1*1', ["{'type': 'stmt', 'expression': {'type': 'term', 'left': {'type': 'int', 'value': 1}, 'right': {'type': 'int', 'value': 1}, 'operator': {'type': 'term_operator', 'operator': '*'}}}"])
Test.test(Test.parse_test, '1+2*3', '1+2*3', ["{'type': 'stmt', 'expression': {'type': 'expr', 'left': {'type': 'int', 'value': 1}, 'right': {'type': 'term', 'left': {'type': 'int', 'value': 2}, 'right': {'type': 'int', 'value': 3}, 'operator': {'type': 'term_operator', 'operator': '*'}}, 'operator': {'type': 'expr_operator', 'operator': '+'}}}"])
Test.test(Test.execute_test, '1', '1', [1])
Test.test(Test.execute_test, '1d20', '1d20', [1, 20])
Test.test(Test.execute_test, 'DB', 'DB', [1, 4])
Test.test(Test.execute_test, '1+1', '1+1', [2])
Test.test(Test.execute_test, '1+1d20', '1+1d20', [1, 21])
Test.test(Test.execute_test, '1+DB', '1+DB', [1, 5])
Test.test(Test.execute_test, '2-1', '2-1', [1])
Test.test(Test.execute_test, '20-1d20', '20-1d20', [0, 19])
Test.test(Test.execute_test, '4-DB', '4-DB', [0, 3])
Test.test(Test.execute_test, '2*2', '2*2', [4])
Test.test(Test.execute_test, '20*1d20', '20*1d20', [20, 400])
Test.test(Test.execute_test, '4*DB', '4*DB', [4, 16])
Test.test(Test.execute_test, '2/2', '2/2', [1])
Test.test(Test.execute_test, '20/1d20', '20/1d20', [1, 20])
Test.test(Test.execute_test, '1+2*4', '1+2*4', [9])
Test.test(Test.execute_test, '2*4+1', '2*4+1', [9])
Test.test(Test.execute_test, '1+2+3+4+5+6', '1+2+3+4+5+6', [21])
Test.test(Test.execute_test, '2*2*2*2*2*2', '2*2*2*2*2*2', [64])
Test.test(Test.execute_test, '2*2+2*2+2*2', '2*2+2*2+2*2', [12])
Test.test(Test.execute_test, '100-90-5', '100-90-5', [5])
Test.test(Test.execute_test, '100/10/2', '100/10/2', [5])
Test.test(Test.execute_test, '100-50/2', '100-50/2', [75])
Test.test(Test.execute_test, '100*50/2+10-10', '100*50/2+10-10', [2500])
Test.test(Test.execute_test, '100+200*300/200-100', '100+200*300/200-100', [300])
Test.test(Test.execute_test, '1+2*3-4/5*6+7*8-9', '1+2*3-4/5*6+7*8-9', [1+2*3-4/5*6+7*8-9])
Test.test(Test.execute_test, '1-2/3+4*5+6-7/8+9', '1-2/3+4*5+6-7/8+9', [1-2/3+4*5+6-7/8+9])
Test.test(Test.execute_test, '1000000000*2000000/30-10+30', '1000000000*2000000/30-10+30', [1000000000*2000000/30-10+30])
Test.print_result()
