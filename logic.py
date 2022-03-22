from logging import getLogger

logger = getLogger(__name__)
from enum import Enum
from random import choice, randint
from typing import Optional, List

from pydantic import BaseModel


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class CellStatus(str, Enum):
    win = 1
    lose = -1
    wait = 0


class Animal(BaseModel):
    name: str
    stronger_then: List[str] = []  # this animal stronger_then this list of animal names

    def __str__(self):
        return self.name[0].upper()

    def attack(self, animal: "self") -> CellStatus:
        if animal.name in self.stronger_then:
            return CellStatus.win
        return CellStatus.lose


class Cell(BaseModel):
    x: int
    y: int
    animal: Optional[Animal]
    defeated: bool = False
    status: CellStatus = CellStatus.wait

    def __str__(self):
        return "-" if self.status == CellStatus.win else str(self.animal)

    def set_win_status(self):
        self.status = CellStatus.win

    def full_print(self):
        print(self.x, self.y, self.animal, self.defeated, self.status)

    def attack(self, cell: "self") -> CellStatus:
        return self.animal.attack(cell.animal)


class Board(BaseModel):
    cells: List[Cell]
    width: int
    height: int

    def __str__(self):
        result = ""
        for i, cell in enumerate(self.cells, 1):
            result += f"{str(cell)} "
            if not i % self.width:
                result += "\n"
        return result

    def get_cell(self, x: int, y: int) -> Cell:
        position = (y - 1) * self.width + x - 1
        return self.cells[position]

    def get_random_cell(self) -> Cell:
        x = randint(1, self.width)
        y = randint(1, self.height)
        return self.get_cell(x, y)

    def get_next_cells(self, x: int, y: int, status: Optional[CellStatus]) -> List[Cell]:
        """
        Select nearest cells for the cell with x, y.
        :param status: If status is set, then will return cells only with this status.
        :return:
        """
        cells = []
        for y_shift in [-1, 0, 1]:
            for x_shift in [-1, 0, 1]:
                if x_shift == 0 and y_shift == 0:
                    continue
                new_cell_x = x + x_shift
                new_cell_y = y + y_shift
                if 1 <= new_cell_x <= self.width and 1 <= new_cell_y <= self.height:
                    cell = self.get_cell(new_cell_x, new_cell_y)
                    cells.append(cell)

        # If status is set, then will return cells only with this status.
        if status:
            cells = [c for c in cells if c.status == status]

        return cells


class AnimalBuilder(BaseModel):
    rules: dict = {}

    def create_random_animal(self) -> Animal:
        animal_name = choice(list(self.rules.keys()))
        return Animal(name=animal_name, stronger_then=self.rules[animal_name])

    def create_animal_by_symbol(self, symbol: str) -> Animal:
        animals = {a[0]: a for a in list(self.rules.keys())}
        animal_name = animals.get(symbol)
        return Animal(name=animal_name, stronger_then=self.rules[animal_name])


class BoardBuilder(BaseModel):
    rules: dict

    def build_board(self, *args, **kwargs) -> Board:
        raise NotImplemented


class DefinedBoardBuilder(BoardBuilder):
    board_data: str

    def build_board(self) -> Board:
        animal_builder = AnimalBuilder(rules=self.rules)
        board_data = self.board_data.strip().replace(" ", "").split("\n")
        board = Board(cells=[], width=len(board_data[0]), height=len(board_data))
        for y, line in enumerate(board_data, 1):
            for x, symbol in enumerate(line, 1):
                animal = animal_builder.create_animal_by_symbol(symbol)
                board.cells.append(Cell(x=x, y=y, animal=animal))
        return board


class RandomBoardBuilder(BoardBuilder):
    width: int
    height: int

    def build_board(self) -> Board:
        animal_builder = AnimalBuilder(rules=self.rules)
        board = Board(cells=[], width=self.width, height=self.height)
        for y in range(1, self.height + 1):
            for x in range(1, self.width + 1):
                animal = animal_builder.create_random_animal()
                board.cells.append(Cell(x=x, y=y, animal=animal))
        return board


class Battle(BaseModel):
    def attack_from_cell(self, board: Board, attacker_cell: Cell) -> Board:
        after_cells = []

        cells = board.get_next_cells(attacker_cell.x, attacker_cell.y, CellStatus.wait)
        for cell in cells:
            cell.status = attacker_cell.attack(cell)

            if cell.status == CellStatus.win:
                cell.animal = attacker_cell.animal
                after_cells.append(cell)

        # attack from cells, where attacker_cell win
        for cell in after_cells:
            self.attack_from_cell(board, cell)
        return board
