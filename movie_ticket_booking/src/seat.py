from dataclasses import dataclass


@dataclass
class Seat:
    row_number: int
    column_number: int
    is_available: bool = True

    @property
    def seat_number(self) -> str:
        return f"{self.row_number}-{self.column_number}"
