from dataclasses import dataclass
from typing import List

from .seat import Seat
from .movie_show import MovieShow


@dataclass
class Ticket:
    ticket_id: str
    seats: List[Seat]
    show: MovieShow
