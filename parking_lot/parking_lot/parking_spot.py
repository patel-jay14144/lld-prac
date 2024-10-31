from enum import Enum


class ParkingType(Enum):
    INACTIVE_SPOT = 0
    TWO_WHEELER_SPOT = 2
    FOUR_WHEELER_SPOT = 4


class ParkingSpot:
    def __init__(
        self, parking_type: int, floor_number: int, row_number: int, column_number: int
    ) -> None:
        """
        Initialize a ParkingSpot object.

        The ParkingSpot object is initialized with a parking type.
        The parking type is an instance of the ParkingType Enum which represents the type of vehicle
        that can be parked in this spot (inactive, two-wheeler, or four-wheeler).
        Sets the availability of the parking spot based on the parking type.
        """

        self.parking_type = ParkingType(parking_type)

        # Slot state
        self.is_available = bool(self.parking_type.value)
        self.parked_vehicle: str | None = None
        self.ticket_id: str | None = None

        # Slot meta
        self.floor_number: int = floor_number
        self.row_number: int = row_number
        self.column_number: int = column_number

    @property
    def spot_id(self):
        """
        The unique identifier for a parking spot in the format "floorNumber-rowNumber-columnNumber".
        """

        return f"{self.floor_number}-{self.row_number}-{self.column_number}"

    def release_spot(self):
        """
        Releases the parking spot, making it available for future parking.

        This function marks the spot as available and clears the parked vehicle and ticket ID,
        effectively resetting the spot for the next use.
        """

        self.is_available = True
        self.parked_vehicle = None
        self.ticket_id = None
