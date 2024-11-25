from .types import Board

from src.piece import Bishop, Knight, Queen, King, Rook, Pawn
from src.piece.types import ColorType


class Game:
    def __init__(self) -> None:
        self.__board: Board = [
            [
                Rook(color=ColorType.WHITE, row=0, col=0),
                Knight(color=ColorType.WHITE, row=0, col=1),
                Bishop(color=ColorType.WHITE, row=0, col=2),
                King(color=ColorType.WHITE, row=0, col=3),
                Queen(color=ColorType.WHITE, row=0, col=4),
                Bishop(color=ColorType.WHITE, row=0, col=5),
                Knight(color=ColorType.WHITE, row=0, col=6),
                Rook(color=ColorType.WHITE, row=0, col=7),
            ],
            [Pawn(color=ColorType.WHITE, row=1, col=i) for i in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [Pawn(color=ColorType.BLACK, row=6, col=i) for i in range(8)],
            [
                Rook(color=ColorType.BLACK, row=7, col=0),
                Knight(color=ColorType.BLACK, row=7, col=1),
                Bishop(color=ColorType.BLACK, row=7, col=2),
                King(color=ColorType.BLACK, row=7, col=3),
                Queen(color=ColorType.BLACK, row=7, col=4),
                Bishop(color=ColorType.BLACK, row=7, col=5),
                Knight(color=ColorType.BLACK, row=7, col=6),
                Rook(color=ColorType.BLACK, row=7, col=7),
            ],
        ]
        self.__status = 0
        self.whose_turn: ColorType = ColorType.WHITE

    def __change_whose_turn_it_is(self):
        if self.whose_turn == ColorType.WHITE:
            self.whose_turn = ColorType.BLACK
        else:
            self.whose_turn = ColorType.WHITE

    def move(self, start_row: int, start_col: int, end_row: int, end_col: int) -> str:
        if start_row < 0 or start_row > 7 or start_col < 0 or start_col > 7:
            return "invalid"

        if end_row < 0 or end_row > 7 or end_col < 0 or end_col > 7:
            return "invalid"

        if self.__board[start_row][start_col] is None:
            return "invalid"

        if self.__board[start_row][start_col].color != self.whose_turn:
            return "invalid"

        if self.__board[start_row][start_col].is_valid_move(
            end_row, end_col, self.__board
        ):
            piece_at_end_before_the_move = self.__board[end_row][end_col]
            self.__board[end_row][end_col] = self.__board[start_row][start_col]
            self.__board[start_row][start_col] = None

            if type(self.__board[end_row][end_col]) is King:
                self.__status = 1 if self.whose_turn == ColorType.WHITE else 2
            else:
                self.__change_whose_turn_it_is()
            return piece_at_end_before_the_move or ""
        else:
            return "invalid"

    def get_next_turn(self) -> ColorType:
        return self.whose_turn

    def get_status(self) -> int:
        return self.__status

    def get_board(self) -> Board:
        return self.__board
