from parking_lot.parking_lot import ParkingLot


parking = ParkingLot(
    [
        [[4, 4, 2, 2], [2, 4, 2, 0], [0, 2, 2, 2], [4, 4, 4, 0]],
        [[4, 4, 2, 2], [2, 4, 2, 0], [0, 2, 2, 2], [4, 4, 4, 2]],
    ]
)


# parking.print_blueprint()
def test_free_spots_on_floor_zero():
    assert parking.get_free_spots_count(0) == 13
    assert parking.get_free_spots_count(0, 2) == 7


def test_free_spots_on_floor_one():
    assert parking.get_free_spots_count(1) == 14
    assert parking.get_free_spots_count(1, 2) == 8


def test_park_two_wheeler_with_strategy_zero():
    spot_id = parking.park(2, "GJ12MK1234", "123", 0)

    assert spot_id, "❗️ Did not find parking"
    assert type(spot_id) is str, "❗️ Response is not of type string"
    assert spot_id == "0-0-2", "❗️ Vehicle parked at incorrect spot"

    # Search for the parked vehicle
    assert (
        parking.search_vehicle("GJ12MK1234") == "0-0-2"
    ), "❗️ Couldn't find vehicle from vehicle_number"
    assert (
        parking.search_vehicle("123") == "0-0-2"
    ), "❗️ Couldn't find vehicle from ticket_number"

    assert parking.get_free_spots_count(0) == 12, "❗️ Number of spots not reduced"
    assert (
        parking.get_free_spots_count(0, 2) == 6
    ), "❗️ Number of spots not reduced for that vehicle type"


def test_park_two_wheeler_with_strategy_one():
    spot_id = parking.park(2, "GJ12MK1235", "124", 1)

    assert spot_id, "❗️ Did not find parking"
    assert type(spot_id) is str, "❗️ Response is not of type string"
    assert spot_id == "1-0-2", "❗️ Vehicle parked at incorrect spot"

    # Search for the parked vehicle
    assert (
        parking.search_vehicle("GJ12MK1235") == "1-0-2"
    ), "❗️ Couldn't find vehicle from vehicle_number"
    assert (
        parking.search_vehicle("124") == "1-0-2"
    ), "❗️ Couldn't find vehicle from ticket_number"

    assert parking.get_free_spots_count(1) == 13, "❗️ Number of spots not reduced"
    assert (
        parking.get_free_spots_count(1, 2) == 7
    ), "❗️ Number of spots not reduced for that vehicle type"


test_free_spots_on_floor_zero()
test_free_spots_on_floor_one()
test_park_two_wheeler_with_strategy_one()

print("✅ All test cases passed")
