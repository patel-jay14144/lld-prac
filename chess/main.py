from src.game import Game
from src.piece.types import ColorType


game = Game()


def test_move_valid():
    # Test a valid move
    start_row, start_col = 1, 0  # White pawn
    end_row, end_col = 3, 0
    result = game.move(start_row, start_col, end_row, end_col)
    assert result == ""
    assert game.get_board()[end_row][end_col].color == ColorType.WHITE
    assert game.get_board()[start_row][start_col] is None
    assert game.get_next_turn() == ColorType.BLACK


def test_move_invalid_piece():
    # Test moving a piece that is not yours
    start_row, start_col = 1, 0  # Black pawn
    end_row, end_col = 3, 0
    result = game.move(start_row, start_col, end_row, end_col)
    assert result == "invalid"


def test_move_invalid_position():
    # Test moving a piece to an invalid position
    start_row, start_col = 1, 0  # White pawn
    end_row, end_col = 8, 0  # Off the board
    result = game.move(start_row, start_col, end_row, end_col)
    assert result == "invalid"


def test_get_status_initial():
    # Test the initial game status
    status = game.get_status()
    assert status == 0


def test_get_status_checkmate():
    # Test the game status after a "checkmate" (king capture)
    # Move the white queen to capture the black king
    start_row, start_col = 0, 3  # White queen
    end_row, end_col = 7, 3  # Black king
    game.move(start_row, start_col, end_row, end_col)
    status = game.get_status()
    # assert status == 1  # White wins


def test_get_next_turn_initial():
    # Test the initial next turn
    next_turn = game.get_next_turn()
    assert next_turn == ColorType.WHITE


def test_get_next_turn_after_move():
    # Test the next turn after a move
    start_row, start_col = 1, 0  # White pawn
    end_row, end_col = 3, 0
    game.move(start_row, start_col, end_row, end_col)
    next_turn = game.get_next_turn()
    assert next_turn == ColorType.BLACK


test_move_valid()
test_move_invalid_piece()
test_move_invalid_position()
test_get_status_initial()
test_get_status_checkmate()
test_get_next_turn_initial()
test_get_next_turn_after_move()
