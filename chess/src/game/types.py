from typing import List, Union

from src.piece.base import BasePiece

Square = Union[BasePiece, None]
Board = List[List[Square]]
