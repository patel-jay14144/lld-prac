from datetime import datetime
from typing import Dict, List

from .screen import Screen
from .movie_show import MovieShow


class Cinema:
    def __init__(
        self,
        cinema_id: int,
        city_id: int,
        screen_count: int,
        screen_rows: int,
        screen_columns: int,
    ) -> None:
        self.cinema_id = cinema_id
        self.city_id = city_id
        self.screens: List[Screen] = [
            Screen(screen_rows, screen_columns) for _ in range(screen_count)
        ]

        self.shows: Dict[int, MovieShow] = {}

    def add_show(
        self,
        show_id: int,
        movie_id: int,
        screen_index: int,
        start_time: datetime,
        end_time: datetime,
    ) -> MovieShow:
        if self.shows.get(show_id):
            raise Exception(f"Show with id {show_id} already exists")

        if screen_index >= len(self.screens) or screen_index < 0:
            raise Exception(f"Invalid screen index {screen_index}")

        new_movie_show = MovieShow(
            show_id=show_id,
            movie_id=movie_id,
            cinema=self,
            start_time=start_time,
            end_time=end_time,
            screen=self.screens[screen_index],
        )

        self.shows[show_id] = new_movie_show

        return new_movie_show
