from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from parking_lot.parking_lot import ParkingLot
    from parking_lot.parking_spot import ParkingSpot, ParkingType
    from parking_lot.parking_floor import ParkingFloor


class BaseParkingStrategy(ABC):
    @abstractmethod
    def find_available_slot(
        self, parking: "ParkingLot", vehicle_type: "ParkingType"
    ) -> Union["ParkingSpot", None]: ...

    def select_nearest_spot_on_floor(
        self, floor: "ParkingFloor", vehicle_type: "ParkingType"
    ) -> Union["ParkingSpot", None]:
        """
        Selects the parking spot with the smallest index on the given floor that matches the specified vehicle type.

        Iterates over the parking spots on the specified floor and returns the first parking spot that matches
        the given vehicle type. The search is conducted in a row-major order, ensuring the smallest index is selected.

        Args:
            floor (ParkingFloor): The floor to search for an available parking spot.
            vehicle_type (ParkingType): The type of vehicle for which a parking spot is needed.

        Returns:
            ParkingSpot: The parking spot with the smallest index that matches the specified vehicle type.
        """
        for row in floor.spots:
            for spot in row:
                if spot.parking_type == vehicle_type:
                    return spot
