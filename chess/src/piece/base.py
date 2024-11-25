from .types import PieceType, ColorType
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.types import Board


class BasePiece(ABC):
    def __init__(
        self, color: ColorType, piece_type: PieceType, row: int, col: int
    ) -> None:
        self.color = color
        self.type = piece_type
        self.skips_obstacles = self.type == PieceType.KNIGHT
        self.row = row
        self.col = col

    def is_destination_empty_or_valid_capture(
        self, end_row: int, end_col: int, board: "Board"
    ) -> bool:
        if board[end_row][end_col] is not None:
            return self.is_valid_capture(end_row=end_row, end_col=end_col, board=board)

        return True

    def is_opposite_color_piece(
        self, end_row: int, end_col: int, board: "Board"
    ) -> bool:
        if self.color == board[end_row][end_col].color:
            return False
        return True

    @abstractmethod
    def is_valid_move(self, end_row: int, end_col: int, board: "Board") -> bool:
        pass

    def is_valid_capture(self, end_row: int, end_col: int, board: "Board") -> bool:
        if not self.is_opposite_color_piece(
            end_row=end_row, end_col=end_col, board=board
        ):
            return False
