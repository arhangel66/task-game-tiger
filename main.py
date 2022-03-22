from core import RandomBoardBuilder, Battle
from rules import animals_rules


def main():
    board_builder = RandomBoardBuilder(width=10, height=10, rules=animals_rules)
    board = board_builder.build_board()
    print(board)

    attacker_cell = board.get_random_cell()
    attacker_cell.set_win_status()
    print(f"start_cell: {attacker_cell.x}, {attacker_cell.y}, {attacker_cell.animal}")

    Battle().attack_from_cell(board, attacker_cell)
    print(board)

if __name__ == "__main__":
    main()

