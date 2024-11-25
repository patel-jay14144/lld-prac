from src.piece.types import ColorType, PieceType
from .base import BasePiece
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.types import Board


class Rook(BasePiece):
    def __init__(self, color: ColorType, row: int, col: int) -> None:
        super().__init__(color, PieceType.ROOK, row, col)
        self.has_piece_moved = False

    def is_valid_move(self, end_row: int, end_col: int, board: "Board") -> bool:
        if not self.is_destination_empty_or_valid_capture(
            end_row=end_row, end_col=end_col, board=board
        ):
            return False

        if self.row != end_row and self.col != end_col:
            return False

        if self.row != end_row:
            for row in range(self.row, end_row + 1):
                if board[row][self.col] is not None:
                    return False

        if self.col != end_col:
            for col in range(self.col, end_col + 1):
                if board[self.row][col] is not None:
                    return False

        return True
