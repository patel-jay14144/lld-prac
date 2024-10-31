from collections import defaultdict
from typing import List
from .parking_spot import ParkingSpot, ParkingType


class ParkingFloor:
    def __init__(self, floor_definition: List[List[int]], floor_number: int) -> None:
        """
        Initialize a ParkingFloor object.

        The ParkingFloor object is initialized with the floor definition and floor number.
        The floor definition is a 2D list of integers, where each integer represents a parking spot.
        The first dimension of the list represents the rows on each floor.
        The second dimension represents the columns on each row.
        The value of the integer represents the type of parking spot.
        0 represents an inactive parking spot, 2 represents a two-wheeler parking spot, and 4 represents a four-wheeler parking spot.

        The floor number is the index of the floor in the parking lot.
        """

        self.spot_counts = defaultdict(lambda: 0)
        self.spots: List[List[ParkingSpot]] = []
        self.floor_number = floor_number

        # Iterate for each row
        for row_number, row in enumerate(floor_definition):
            spots_in_current_row: List[ParkingSpot] = []

            # Create a spot object for each spot in that row
            for column_number, spot in enumerate(row):
                spots_in_current_row.append(
                    ParkingSpot(spot, self.floor_number, row_number, column_number)
                )
                self.__incr_available_spots(ParkingType(spot))

            self.spots.append(spots_in_current_row)

    def __reset_total_spots(self):
        """
        Resets the total number of available and total spots in the floor.

        The total number of available spots is the sum of the number of two-wheeler and four-wheeler spots.
        The total number of spots is the sum of the total number of available spots and the number of inactive spots.
        """
        self.spot_counts["available_spots"] = (
            self.spot_counts[ParkingType.TWO_WHEELER_SPOT]
            + self.spot_counts[ParkingType.FOUR_WHEELER_SPOT]
        )

        self.spot_counts["total"] = (
            self.spot_counts["available_spots"]
            + self.spot_counts[ParkingType.INACTIVE_SPOT]
        )

    def __incr_available_spots(self, parking_type: ParkingType, increment_by: int = 1):
        """
        Increments the number of available two-wheeler parking spots in the floor by the given amount.

        Args:
            increment_by (int): The amount to increment the number of available two-wheeler parking spots by. Defaults to 1.
        """
        self.spot_counts[parking_type] += increment_by
        self.__reset_total_spots()

    def __decr_available_spots(self, parking_type: ParkingType, decrement_by: int = 1):
        """
        Increments the number of available two-wheeler parking spots in the floor by the given amount.

        Args:
            decrement_by (int): The amount to increment the number of available two-wheeler parking spots by. Defaults to 1.
        """
        self.spot_counts[parking_type] -= decrement_by
        self.__reset_total_spots()

    def allocate_spot(
        self,
        row: int,
        column: int,
        vehicle_number: str,
        parking_type: ParkingType,
        ticket_id: str,
    ):
        """
        Allocates a parking spot at the given row and column and assigns it to a vehicle.

        The function allocates the parking spot at the given row and column, making it unavailable for future parking.
        It also decrements the count of available spots on the floor for the spot's parking type.

        Args:
            row (int): The row index of the parking spot.
            column (int): The column index of the parking spot.
            vehicle_number (str): The vehicle number of the vehicle that is being parked.
            parking_type (ParkingType): The type of parking spot.
            ticket_id (str): The ticket id of the vehicle that is being parked.
        """
        allocated_spot = self.spots[row][column]

        allocated_spot.is_available = False
        allocated_spot.parked_vehicle = vehicle_number
        allocated_spot.ticket_id = ticket_id
        self.__decr_available_spots(parking_type)

    def remove_vehicle(self, row: int, column: int):
        """
        Removes a vehicle from the specified parking spot and updates the availability.

        The function releases the parking spot at the given row and column, making it available for future parking.
        It also increments the count of available spots on the floor for the spot's parking type.

        Args:
            row (int): The row index of the parking spot.
            column (int): The column index of the parking spot.
        """
        spot = self.spots[row][column]
        spot.release_spot()

        # Update floor meta
        self.__incr_available_spots(spot.parking_type)
