from src.piece.types import ColorType, PieceType
from .base import BasePiece
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.types import Board


class King(BasePiece):
    def __init__(self, color: ColorType, row: int, col: int) -> None:
        super().__init__(color, PieceType.KING, row, col)

    def is_valid_move(self, end_row: int, end_col: int, board: "Board") -> bool:
        if not self.is_destination_empty_or_valid_capture(
            end_row=end_row, end_col=end_col, board=board
        ):
            return False

        row_diff = abs(self.row - end_row)
        col_diff = abs(self.col - end_col)

        if row_diff != 0 and row_diff != 1:
            return False

        if col_diff != 0 and row_diff != 1:
            return False

        return True
