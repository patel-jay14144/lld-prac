from typing import List, Dict
from .parking_floor import ParkingFloor
from parking_lot.parking_spot import ParkingSpot, ParkingType
from enum import Enum
from parking_strategy import (
    LowestFloorSmallestIndexStrategy,
    MostAvailableSpotsOnFloorSmallestIndexStrategy,
    BaseParkingStrategy,
)


class ParkingStrategy(Enum):
    LowestFloorSmallestIndexStrategy = (0, LowestFloorSmallestIndexStrategy)
    MostAvailableSpotsOnFloorSmallestIndexStrategy = (
        1,
        MostAvailableSpotsOnFloorSmallestIndexStrategy,
    )

    @classmethod
    def from_int(cls, value: int):
        for item in cls:
            if item.value[0] == value:
                return item.value[1]
        return None


class ParkingLot:
    def __init__(self, parking_definition: List[List[List[int]]]) -> None:
        """
        Initialize the ParkingLot object.

        The ParkingLot object is initialized with the parking definition.
        The parking definition is a 3D list of integers, where each integer represents a parking spot.
        The first dimension of the list represents the floors of the parking lot.
        The second dimension represents the rows on each floor.
        The third dimension represents the columns on each row.
        The value of the integer represents the type of parking spot.
        0 represents an inactive parking spot, 2 represents a two-wheeler parking spot, and 4 represents a four-wheeler parking spot.
        """

        self.floors: List[ParkingFloor] = []

        # Create floors for each object
        for floor_number, floor in enumerate(parking_definition):
            self.floors.append(ParkingFloor(floor, floor_number))

        self.vehicle_number_to_spot_map: Dict[str, ParkingSpot] = {}
        self.ticket_number_to_spot_map: Dict[str, ParkingSpot] = {}

    def print_blueprint(self):
        """
        Prints the blueprint of the parking lot in the console.
        The parking lot blueprint is a 2D representation of the parking lot.
        Each floor is separated by "!!!" and each row is separated by a new line.
        The parking spots are represented by the value of the ParkingType Enum.
        """

        for floor in self.floors:
            print(f"!!! For floor {floor.floor_number}")

            for row in floor.spots:
                for spot in row:
                    print(f"{spot.parking_type.value}", end=" ")

                print("\n")

    def park(
        self,
        vehicle_type: int,
        vehicle_number: str,
        ticket_id: str,
        parking_strategy: int,
    ) -> str | bool:
        """
        Parks a vehicle in the parking lot according to the specified parking strategy.

        The parking strategy is determined by the parking_strategy parameter.
        The vehicle type is determined by the vehicle_type parameter.
        The vehicle number and ticket id are used to identify the vehicle.

        If the parking strategy is not found, returns False.
        If the vehicle is not parked, returns False.
        If the vehicle is parked, returns the parking spot id.

        :param vehicle_type: The type of vehicle
        :param vehicle_number: The number of the vehicle
        :param ticket_id: The ticket id of the vehicle
        :param parking_strategy: The parking strategy to use
        :return: The parking spot id or False if the vehicle is not parked
        """
        selected_parking_strategy: BaseParkingStrategy = ParkingStrategy.from_int(
            parking_strategy
        )
        selected_parking_strategy = selected_parking_strategy()

        print(f"Selected parking strategy: {selected_parking_strategy}")

        selected_parking_spot = selected_parking_strategy.find_available_slot(
            self, ParkingType(vehicle_type)
        )

        if selected_parking_spot is None:
            return False

        self.floors[selected_parking_spot.floor_number].allocate_spot(
            selected_parking_spot.row_number,
            selected_parking_spot.column_number,
            vehicle_number,
            ParkingType(vehicle_type),
            ticket_id,
        )

        self.vehicle_number_to_spot_map[vehicle_number.lower()] = selected_parking_spot
        self.ticket_number_to_spot_map[ticket_id.lower()] = selected_parking_spot
        return selected_parking_spot.spot_id

    def remove_vehicle(self, spot_id: str) -> None:
        """
        Removes a vehicle from a parking spot.

        :param spot_id: The id of the parking spot where the vehicle is parked
        :return: None
        """
        floor, row, column = spot_id.split("-")

        self.floors[int(floor)].remove_vehicle(int(row), int(column))

    def search_vehicle(self, search_query: str) -> str:
        """
        Searches for a vehicle in the parking lot.

        :param search_query: The ticket id or vehicle number to search for
        :return: The parking spot id of the vehicle if found, otherwise an empty string
        """
        if search_query.lower() in self.vehicle_number_to_spot_map:
            return self.vehicle_number_to_spot_map.get(search_query.lower()).spot_id

        if search_query.lower() in self.ticket_number_to_spot_map:
            return self.ticket_number_to_spot_map.get(search_query.lower()).spot_id

        return ""

    def get_free_spots_count(self, floor_number: int) -> int | None:
        """
        Get the number of free parking spots on the specified floor.

        Args:
            floor_number (int): The index of the floor in the parking lot.

        Returns:
            int | None: The number of free parking spots on the given floor, or None
            if the floor number is invalid (i.e., exceeds the number of floors).
        """
        if floor_number >= len(self.floors):
            return None
        return self.floors[floor_number].spot_counts["available_spots"]

    def get_free_spots_count(self, floor_number: int, vehicle_type: int) -> int | None:  # noqa: F811
        """
        Get the number of free parking spots on the specified floor.

        Args:
            floor_number (int): The index of the floor in the parking lot.

        Returns:
            int | None: The number of free parking spots on the given floor, or None
            if the floor number is invalid (i.e., exceeds the number of floors).
        """
        vehicle_type = ParkingType(vehicle_type)
        if floor_number >= len(self.floors):
            return None
        return self.floors[floor_number].spot_counts[vehicle_type]
