from dice_notation import Parser

class Test:
    passed = 0
    failed = 0
    @staticmethod
    def init():
        Test.passed = 0
        Test.faild = 0
    @staticmethod
    def test(name: str, src: str, result: str) -> bool:
        parser = Parser()
        if result == str(parser.parse(src)):
            print(f'\t{name}\t: passed')
            Test.passed += 1
        else:
            print(f'\t{name}\t: failed')
            Test.faild += 1
    @staticmethod
    def print_result():
        print(f'Passed: {Test.passed}, Failed: {Test.faild}')

Test.init()
Test.test('1', '1', "{'type': 'stmt', 'expresstion': {'type': 'int', 'value': 1}}")
Test.test('10', '10', "{'type': 'stmt', 'expresstion': {'type': 'int', 'value': 10}}")
Test.test('1d20', '1d20', "{'type': 'stmt', 'expresstion': {'type': 'dice', 'notation': '1d20'}}")
Test.test('1D20', '1D20', "{'type': 'stmt', 'expresstion': {'type': 'dice', 'notation': '1d20'}}")
Test.test('DB', 'DB', "{'type': 'stmt', 'expresstion': {'type': 'damage_bonus'}}")
Test.test('db', 'db', "{'type': 'stmt', 'expresstion': {'type': 'damage_bonus'}}")
Test.test('1+1', '1+1', "{'type': 'stmt', 'expresstion': {'type': 'expr', 'operator': {'type': 'operator', 'operator': '+'}, 'left': {'type': 'int', 'value': 1}, 'right': {'type': 'int', 'value': 1}}}")
Test.test('1+1d20', '1+1d20', "{'type': 'stmt', 'expresstion': {'type': 'expr', 'operator': {'type': 'operator', 'operator': '+'}, 'left': {'type': 'int', 'value': 1}, 'right': {'type': 'dice', 'notation': '1d20'}}}")
Test.test('1+DB', '1+DB', "{'type': 'stmt', 'expresstion': {'type': 'expr', 'operator': {'type': 'operator', 'operator': '+'}, 'left': {'type': 'int', 'value': 1}, 'right': {'type': 'damage_bonus'}}}")
Test.test('1d20+1', '1d20+1', "{'type': 'stmt', 'expresstion': {'type': 'expr', 'operator': {'type': 'operator', 'operator': '+'}, 'left': {'type': 'dice', 'notation': '1d20'}, 'right': {'type': 'int', 'value': 1}}}")
Test.test('1d20+1d20', '1d20+1d20', "{'type': 'stmt', 'expresstion': {'type': 'expr', 'operator': {'type': 'operator', 'operator': '+'}, 'left': {'type': 'dice', 'notation': '1d20'}, 'right': {'type': 'dice', 'notation': '1d20'}}}")
Test.test('1d20+DB', '1d20+DB', "{'type': 'stmt', 'expresstion': {'type': 'expr', 'operator': {'type': 'operator', 'operator': '+'}, 'left': {'type': 'dice', 'notation': '1d20'}, 'right': {'type': 'damage_bonus'}}}")
Test.test('DB+1', 'DB+1', "{'type': 'stmt', 'expresstion': {'type': 'expr', 'operator': {'type': 'operator', 'operator': '+'}, 'left': {'type': 'damage_bonus'}, 'right': {'type': 'int', 'value': 1}}}")
Test.test('DB+1d20', 'DB+1d20', "{'type': 'stmt', 'expresstion': {'type': 'expr', 'operator': {'type': 'operator', 'operator': '+'}, 'left': {'type': 'damage_bonus'}, 'right': {'type': 'dice', 'notation': '1d20'}}}")
Test.test('DB+DB', 'DB+DB', "{'type': 'stmt', 'expresstion': {'type': 'expr', 'operator': {'type': 'operator', 'operator': '+'}, 'left': {'type': 'damage_bonus'}, 'right': {'type': 'damage_bonus'}}}")
Test.test('1d20+1+DB', '1d20+1+DB', "{'type': 'stmt', 'expresstion': {'type': 'expr', 'operator': {'type': 'operator', 'operator': '+'}, 'left': {'type': 'dice', 'notation': '1d20'}, 'right': {'type': 'expr', 'operator': {'type': 'operator', 'operator': '+'}, 'left': {'type': 'int', 'value': 1}, 'right': {'type': 'damage_bonus'}}}}")
Test.test('1+1+1+1+1+1+1+1', '1+1+1+1+1+1+1+1', "{'type': 'stmt', 'expresstion': {'type': 'expr', 'operator': {'type': 'operator', 'operator': '+'}, 'left': {'type': 'int', 'value': 1}, 'right': {'type': 'expr', 'operator': {'type': 'operator', 'operator': '+'}, 'left': {'type': 'int', 'value': 1}, 'right': {'type': 'expr', 'operator': {'type': 'operator', 'operator': '+'}, 'left': {'type': 'int', 'value': 1}, 'right': {'type': 'expr', 'operator': {'type': 'operator', 'operator': '+'}, 'left': {'type': 'int', 'value': 1}, 'right': {'type': 'expr', 'operator': {'type': 'operator', 'operator': '+'}, 'left': {'type': 'int', 'value': 1}, 'right': {'type': 'expr', 'operator': {'type': 'operator', 'operator': '+'}, 'left': {'type': 'int', 'value': 1}, 'right': {'type': 'expr', 'operator': {'type': 'operator', 'operator': '+'}, 'left': {'type': 'int', 'value': 1}, 'right': {'type': 'int', 'value': 1}}}}}}}}}")
Test.print_result()
