from src.piece.types import ColorType, PieceType
from .base import BasePiece
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.types import Board


class Pawn(BasePiece):
    def __init__(self, color: ColorType, row: int, col: int) -> None:
        super().__init__(color, PieceType.PAWN, row, col)

    def __has_moved_two_squares(self, end_row: int) -> bool:
        row_diff = self.row - end_row

        if self.color == ColorType.WHITE:
            return row_diff == -2

        return row_diff == 2

    def __has_moved_one_square(self, end_row: int) -> bool:
        row_diff = self.row - end_row

        if self.color == ColorType.WHITE:
            return row_diff == 1

        return row_diff == -1

    def __is_at_starting_position(self) -> bool:
        if self.color == ColorType.WHITE:
            return self.row == 1

        return self.row == 6

    def __has_moved_straight(self, end_col: int) -> bool:
        return self.col == end_col

    def __is_diagonal_capture(self, end_col: int) -> bool:
        col_diff = self.col - end_col

        return col_diff == 1 or col_diff == -1

    def is_valid_move(self, end_row: int, end_col: int, board: "Board") -> bool:
        if not self.is_destination_empty_or_valid_capture(
            end_row=end_row, end_col=end_col, board=board
        ):
            return False

        if not self.__has_moved_straight(end_col=end_col):
            return False

        if self.__is_at_starting_position() and not (
            self.__has_moved_one_square(end_row=end_row)
            or self.__has_moved_two_squares(end_row=end_row)
        ):
            return False

        if not self.__is_at_starting_position() and not self.__has_moved_one_square(
            end_row=end_row
        ):
            return False

        return True

    def is_valid_capture(self, end_row: int, end_col: int, board: "Board") -> bool:
        if not self.is_opposite_color_piece(
            end_row=end_row, end_col=end_col, board=board
        ):
            return False

        if board[end_row][end_col] is None:
            return False

        if not self.__is_diagonal_capture(end_col=end_col):
            return False

        return True
