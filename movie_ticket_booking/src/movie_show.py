from datetime import datetime
from typing import Dict, List, Union, TYPE_CHECKING

from .seat import Seat

if TYPE_CHECKING:
    from .cinema import Cinema
    from .screen import Screen
    from .ticket import Ticket


class MovieShow:
    def __init__(
        self,
        show_id: int,
        movie_id: int,
        cinema: "Cinema",
        start_time: datetime,
        end_time: datetime,
        screen: "Screen",
    ) -> None:
        self.show_id = show_id
        self.movie_id = movie_id
        self.cinema = cinema
        self.start_time = start_time
        self.end_time = end_time
        self.screen = screen

        self._available_seats_count = self.screen.row_count * self.screen.column_count
        self.available_seats: List[List[Seat]] = [
            [Seat(row, column) for column in range(self.screen.column_count)]
            for row in range(self.screen.row_count)
        ]
        self.tickets_map: Dict[str, "Ticket"] = {}

    @property
    def available_seats_count(self):
        """
        The number of available seats in the show.

        This property is read-only.
        """

        return self._available_seats_count

    def book_ticket(self, ticket_id: str, tickets_count: int) -> Union[List[str], bool]:
        """
        Books a specified number of tickets for a movie show.

        This method attempts to reserve a given number of continuous seats
        for a particular show. If continuous seats are not available, it
        selects the best available seats based on booking criteria.

        Args:
            ticket_id (str): The unique identifier for the ticket.
            tickets_count (int): The number of seats to be booked.

        Returns:
            Union[List[str], bool]: A list of seat numbers if booking is successful,
            otherwise False if there are not enough available seats.
        """
        from .ticket import Ticket

        seats_if_no_continuous_seats_found: List[Seat] = []
        continuous_seats: List[Seat] = []

        if tickets_count > self.available_seats_count:
            return False

        for row in self.available_seats:
            for seat in row:
                if not seat.is_available:
                    continuous_seats = []
                    continue

                if (
                    seat.is_available
                    and len(seats_if_no_continuous_seats_found) < tickets_count
                ):
                    seats_if_no_continuous_seats_found.append(seat)

                continuous_seats.append(seat)

                if len(continuous_seats) == tickets_count:
                    break

            continuous_seats = []

        if len(continuous_seats) == tickets_count:
            selected_seats = continuous_seats
        else:
            selected_seats = seats_if_no_continuous_seats_found

        response: List[str] = []
        for seat in selected_seats:
            seat.is_available = False
            self._available_seats_count -= 1
            response.append(seat.seat_number)

        self.tickets_map = Ticket(
            ticket_id=ticket_id, seats=selected_seats, show=self.show_id
        )

        return response
