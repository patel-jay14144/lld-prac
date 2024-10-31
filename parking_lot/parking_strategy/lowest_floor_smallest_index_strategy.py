from .base import BaseParkingStrategy

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from parking_lot.parking_lot import ParkingLot
    from parking_lot.parking_spot import ParkingSpot, ParkingType


class LowestFloorSmallestIndexStrategy(BaseParkingStrategy):
    def find_available_slot(
        self, parking: "ParkingLot", vehicle_type: "ParkingType"
    ) -> Union["ParkingSpot", None]:
        """
        Finds the nearest available parking spot on the lowest floor of the given vehicle type.

        The search is conducted in a row-major order, ensuring the smallest index is selected.

        Args:
            parking (ParkingLot): The parking lot to search for an available parking spot.
            vehicle_type (ParkingType): The type of vehicle for which a parking spot is needed.

        Returns:
            ParkingSpot | None: The parking spot with the smallest index that matches the specified vehicle type. If no such spot is found, returns None.
        """

        for floor in parking.floors:
            if floor.spot_counts[vehicle_type] > 0:
                return self.select_nearest_spot_on_floor(floor, vehicle_type)
