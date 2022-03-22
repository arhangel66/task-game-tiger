`python main.py` - will run the random board and battle from the random cell  
`python rock.py` - same, but changed rules Rock-Paper-Scissors  
`pytest` - run unittests with predefined board and cell  

I decided to do a flexibility in the variants of the creators, and put them as a dict to the separate file (rules).
It allows me to switch them to Rock-Paper-Scissors game, for example.

added simplest unittest to be sure, that result from the documentation is correct.

BoardBuilder - created board and animals, based on passed rules.  
Then you should just pick the cell to start and run   
Battle.attack_board(board, attacker_cell)  

I have added information about animal power to the Animal model for simplify.   
But to speedup it's possible to create a separate class like AttackCalculator and move logic about win-lose there.


Selecting sells like (get_cell, get_random_cell, get_next_cells) can be moved to CellSelector  
Here is the UML schema for created models  
![UML](https://www.plantuml.com/plantuml/png/VLB1Rjim33s7Ny5Z0ZJv01sABjjnfrs7GM1ijX4gAu14emsw_ljiIX6KmVN5WiZtdlYU-PI4eeo3XyvJIlWjk87y1sm23MmmIOHDHy6-kM3mfqloUohzWK_8G3H88jIzRadlfWZiu4xlE3hVS_m0HCGuUau6UzT9rIa0DDX59c4RAVINmMRLxGxtZqNgAq96sjFLfkjmkgnn3eVQA5D-PpzxllS0ctU3BWXihldyX0dNMEwccr5kjNkyKEmdfJVNoxcmp-nUpb8kCoUL96Vc7AMIqE0BYvtxs_pk0-PtrOY-Z2sqH9GP5NE72FoU5LChgMSIaZ4fhPcbTN5BQ-cdtG4C3lJAzZJNjhiYyKk7Qt5hgQoeN-fVB1K0QCHNX_Z1povmtmAp6uNPdeHqnHSS5khA6qjJ70v_7x6jL9rrr7_jqWLmGJW-KyTu917Fa8-wWcKM_PfCUYWjZhRPJzpVD8l2Vg6WKD0bDuOqyod-cd-UqXXTA6ramXE7VXpyFm00
)
```plantuml
class Animal{
	name: str
	can_win: List[str]
}
Animal : attack(animal: Animal)

class AnimalBuilder{
    rules: dict
}
AnimalBuilder : create_random_animal() -> Animal
AnimalBuilder : create_animal_by_symbol() -> Animal
AnimalBuilder ..> Animal

class Cell{
	animal: Animal
	x: int
	y: int
}
Cell : attack(cell: Cell)

class Board{
	width: int
	height: int
	cells: List[Cell]
}
Board : get_cell(x: int, y: int) -> Cell  
Board : get_random_cell() -> Cell
Board : get_next_cells(x: int, y: int, status) -> List[Cell]

class BoardBuilder {
    rules: dict
}
BoardBuilder : make_board()
class RandomBoardBuilder{
	width: int
	height: int
	rules: dict
}
BoardBuilder o-> AnimalBuilder


RandomBoardBuilder : make_board()
class DefinedBoardBuilder{
    board_data: str
    rules: dict
}
DefinedBoardBuilder : make_board()
RandomBoardBuilder ..|> BoardBuilder
DefinedBoardBuilder ..|> BoardBuilder
BoardBuilder ..> Board

interface Battle
Battle : attack_board(board: Board, attacker_cell: Cell) -> Board
Battle --> Board
Battle --> Cell

Cell::animal o--> Animal
Board::cells o--> Cell
```