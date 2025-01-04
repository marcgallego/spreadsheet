from usecase.controller import Controller
from domain.contents import Number
from domain.coordinates import Coordinates
from domain.cell_range import CellRange
from domain.formula_evaluation.tokenizer import Tokenizer
from domain.formula_evaluation.parser import Parser


def main() -> None:
    print('Simple Spreadsheet')
    controller = Controller()
    controller.spreadsheet.edit_cell('A3', Number(10))
    controller.spreadsheet.edit_cell('B4', Number(30))

    tk = Tokenizer()
    p = Parser()
    tokenization = tk.tokenize(
        '1 + A1*((SUMA(A2:B5;PROMEDIO(B6:D8);C1;27)/4)+(D6-D8))')
    p.has_syntax_error(tokenization)
    print('Done!')

    range_ = CellRange(start=Coordinates(1, 2), end=Coordinates(3, 3))
    print(range_)
    print(range_.get_coords())
    print(controller.spreadsheet.get_values(range_))


if __name__ == '__main__':
    main()
