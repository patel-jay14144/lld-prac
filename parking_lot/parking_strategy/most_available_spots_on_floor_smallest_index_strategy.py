from .base import BaseParkingStrategy
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from parking_lot.parking_lot import ParkingLot
    from parking_lot.parking_spot import ParkingSpot, ParkingType


class MostAvailableSpotsOnFloorSmallestIndexStrategy(BaseParkingStrategy):
    def find_available_slot(
        self, parking: "ParkingLot", vehicle_type: "ParkingType"
    ) -> Union["ParkingSpot", None]:
        """
        Finds the first available parking spot on the floor with the maximum number of free spots.

        If multiple floors have the same number of free spots, the floor with the lowest index is chosen.
        If no available spot is found, returns None.

        Args:
            parking (ParkingLot): The parking lot to search for an available parking spot.
            vehicle_type (ParkingType): The type of vehicle for which a parking spot is needed.

        Returns:
            ParkingSpot | None: The first available parking spot on the floor with the maximum number of free spots,
                                or None if no available spot is found.
        """

        floor_with_maximum_free_space = -1
        available_spots_in_winning_candidate = -1

        for floor in parking.floors:
            if floor.spot_counts[vehicle_type] > 0 and (
                floor.spot_counts[vehicle_type] > available_spots_in_winning_candidate
            ):
                floor_with_maximum_free_space = floor.floor_number

        if floor_with_maximum_free_space == -1:
            return

        return self.select_nearest_spot_on_floor(
            parking.floors[floor_with_maximum_free_space], vehicle_type
        )
