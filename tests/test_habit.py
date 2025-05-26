import pytest
from datetime import date, datetime, timedelta
from habittracker.habit import Habit


@pytest.fixture
def test_habit():
    return Habit(name="Reading", description="30 mins",creation_date=date(2025,5,1))


def test_initialization(test_habit):
    assert test_habit.name == "Reading"
    assert test_habit.description == "30 mins"
    assert test_habit.creation_date==date(2025,5,1)
    assert isinstance(test_habit.creation_date, date)
    assert test_habit.completed_dates == []
    assert test_habit.active is True


def test_check_off(test_habit):
    today = date.today()
    test_habit.check_off(today)
    assert today in test_habit.completed_dates


def test_deactivate_activate_habit(test_habit):
    # first deactivate the habit then activate.
    test_habit.deactivate_habit()
    assert not test_habit.active
    test_habit.activate_habit()
    assert test_habit


def test_check_off_deactivated_habit(test_habit):
    # first deactivate a habit and then try to check off it.
    test_habit.deactivate_habit()
    with pytest.raises(ValueError) as exc_info:
        test_habit.check_off()
    assert str(exc_info.value) == "Inactive Habit!"


def test_serialize_deserialize(test_habit):
    # add a completion date
    today = date.today()
    test_habit.check_off(today)
    # serialize habit first and then deserialize
    data = test_habit.serialize()
    restored_habit = Habit.deserialize(data)
    assert restored_habit.name == test_habit.name
    assert restored_habit.description == test_habit.description
    assert restored_habit.creation_date == test_habit.creation_date
    assert restored_habit.completed_dates == test_habit.completed_dates
    assert restored_habit.active == test_habit.active
    assert isinstance(restored_habit, Habit)

def test_calculate_streak(test_habit):
    with pytest.raises(NotImplementedError) as exc_info:
        test_habit.calculate_streak()

def test_repr_exact_string(test_habit):
    test_habit.check_off(date=date(2025,5,21))
    expected = (
        "Habit("
        "Name:Reading, "
        "Description:30 mins, "
        "Creation_date:2025-05-01, "
        "Completed_dates:[datetime.date(2025, 5, 21)], "
        "Active:True)"
    )
    assert repr(test_habit)==expected
if __name__ == "__main__":
    pytest.main()
