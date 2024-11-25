from src.piece.types import ColorType, PieceType
from .base import BasePiece
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.types import Board


class Bishop(BasePiece):
    def __init__(self, color: ColorType, row: int, col: int) -> None:
        super().__init__(color, PieceType.BISHOP, row, col)

    def is_valid_move(self, end_row: int, end_col: int, board: "Board") -> bool:
        if not self.is_destination_empty_or_valid_capture(
            end_row=end_row, end_col=end_col, board=board
        ):
            return False

        col_diff = self.col - end_col
        row_diff = self.row - end_row

        if row_diff != col_diff:
            return False

        for inc in range(1, row_diff + 1):
            if board[self.row + inc][self.col + inc] is not None:
                return False

        return True
