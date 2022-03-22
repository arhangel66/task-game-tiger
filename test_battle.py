# from main import DefinedFieldBuilder
from logic import DefinedBoardBuilder, AnimalBuilder, Battle
from rules import animals_rules


def test_expected_result():
    board = """
     T L L W T L W L D L
     T W T D D D D L L T
     W L T D D W T T D L
     W D T D W D L D T L
     W L D W D W W W D W
     D D D W T W W L W W
     W L W D T W L L D D
     T W D W W L W W W T
     D W T T T T W T T D
     L L D T L D W D T W
    """

    board_builder = DefinedBoardBuilder(board_data=board, rules=animals_rules)
    board = board_builder.build_board()
    print(board)
    attacker_cell = board.get_cell(9, 10)
    attacker_cell.animal = AnimalBuilder(rules=animals_rules).create_animal_by_symbol("T")
    attacker_cell.set_win_status()
    Battle().attack_from_cell(board, attacker_cell)
    print(f"start_cell: {attacker_cell.x}, {attacker_cell.y}, {attacker_cell.animal}")

    expected_result = "T L L - T L - L D L \nT - T - - - - L L T \n- L T - - - T T - L \n- - T - - - L - T L \n- L - - - - - - - - \n- - - - T - - L - - \n- L - - T - L L - - \nT - - - - L - - - T \n- - T T T T - T T - \nL L - T L - - - - - \n"
    print(board)
    assert str(board) == expected_result
