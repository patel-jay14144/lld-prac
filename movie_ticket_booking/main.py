from src.booking_system import BookingSystem
from datetime import datetime


booking_system = BookingSystem()


def test_add_cinema():
    booking_system.add_cinema(1, 1, 3, 5, 5)

    assert booking_system.cinemas_mapping[1], "❗️ Cinema not created"


def test_add_show():
    response = booking_system.add_show(
        1, 1, 1, 1, datetime(2024, 11, 3, 9, 00), datetime(2024, 11, 3, 11, 00)
    )
    assert response, "❗️ Show not added"


def test_get_free_seats_count():
    available_seats = booking_system.get_free_seats_count(1)
    assert available_seats == 25, "❗️ Invalid available seats"


def test_list_cinemas():
    cinemas = booking_system.list_cinemas(1, 1)
    assert cinemas == [1], "❗️ Invalid cinemas for a particular movie and cities"


def test_book_ticket():
    tickets = booking_system.book_ticket("ticket-1", 1, 3)
    assert tickets == [
        "0-0",
        "0-1",
        "0-2",
    ], "❗️ Invalid cinemas for a particular movie and cities"

    available_seats = booking_system.get_free_seats_count(1)
    assert available_seats == 22, "❗️ Invalid available seats after booking tickets"


test_add_cinema()
test_add_show()
test_get_free_seats_count()
test_list_cinemas()
test_book_ticket()
print("✅ All test cases passed")
