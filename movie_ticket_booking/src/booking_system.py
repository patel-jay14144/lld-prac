from collections import defaultdict
from typing import List, Set, Dict, Union
from datetime import datetime

from .cinema import Cinema
from .movie_show import MovieShow


class BookingSystem:
    def __init__(self) -> None:
        self.city_to_movie_mapping: Dict[int, Dict[int, Set[Cinema]]] = defaultdict(
            lambda: defaultdict(set)
        )
        self.cinemas_mapping: Dict[int, Cinema] = {}
        self.shows: Dict[int, MovieShow] = {}

    def add_cinema(
        self,
        cinema_id: int,
        city_id: int,
        screen_count: int,
        screen_row: int,
        screen_column: int,
    ):
        """Create a new Cinema object and store it into self.cinemas_mapping

        Args:
            cinema_id (int): _description_
            city_id (int): _description_
            screen_count (int): _description_
            screen_row (int): _description_
            screen_column (int): _description_
        """

        new_cinema_obj = Cinema(
            cinema_id=cinema_id,
            city_id=city_id,
            screen_count=screen_count,
            screen_rows=screen_row,
            screen_columns=screen_column,
        )

        self.cinemas_mapping[cinema_id] = new_cinema_obj

    def add_show(
        self,
        show_id: int,
        movie_id: int,
        cinema_id: int,
        screen_index: int,
        start_time: datetime,
        end_time: datetime,
    ) -> bool:
        cinema_obj = self.cinemas_mapping.get(cinema_id)

        if not cinema_obj:
            raise Exception("Invalid cinema ID")

        added_movie_show = cinema_obj.add_show(
            show_id,
            movie_id,
            screen_index,
            start_time,
            end_time,
        )

        if added_movie_show:
            self.shows[show_id] = added_movie_show
            self.city_to_movie_mapping[cinema_obj.city_id][movie_id].add(cinema_obj)
            return True

        return False

    def get_free_seats_count(self, show_id: int):
        if not self.shows.get(show_id):
            raise Exception("Invalid show id")

        return self.shows.get(show_id).available_seats_count

    def book_ticket(
        self, ticket_id: str, show_id: int, tickets_count: int
    ) -> Union[List[str] | bool]:
        """
        Books a specified number of tickets for a given show.

        Args:
            ticket_id (str): The unique identifier for the ticket.
            show_id (int): The ID of the show for which tickets are being booked.
            tickets_count (int): The number of tickets to book.

        Raises:
            Exception: If the show_id is invalid or does not exist in the system.

        """

        if not self.shows.get(show_id):
            raise Exception(f"Invalid show id {show_id}")

        return self.shows.get(show_id).book_ticket(ticket_id, tickets_count)

    def list_cinemas(self, movie_id: int, city_id: int) -> List[int]:
        cinemas = self.city_to_movie_mapping.get(city_id).get(movie_id)

        return [cinema.cinema_id for cinema in cinemas]
