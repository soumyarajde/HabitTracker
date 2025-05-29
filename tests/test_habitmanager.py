import pytest
from datetime import date
from habittracker.habitmanager import HabitManager
from habittracker.dailyhabit import DailyHabit
from habittracker.weeklyhabit import WeeklyHabit
from habittracker.constants import Periodicity
import os


@pytest.fixture
def habit_manager():
    file_name = "test_hm.json"
    manager = HabitManager(file_name)
    yield manager
    if os.path.exists(file_name):
        os.remove(file_name)


def test_create_daily_habit(habit_manager):
    habit_manager.create_habit(
        "Drinking", "8 glass water", Periodicity.DAILY, date.today()
    )
    assert "drinking" in habit_manager.habits
    assert isinstance(habit_manager.habits["drinking"], DailyHabit)


def test_create_weekly_habit(habit_manager):
    habit_manager.create_habit(
        "shopping", "for the week", Periodicity.WEEKLY, date.today()
    )
    assert "shopping" in habit_manager.habits
    assert isinstance(habit_manager.habits["shopping"], WeeklyHabit)


def test_create_habit_already_exists(habit_manager):
    habit_manager.create_habit(
        "Drinking", "8 glass water", Periodicity.DAILY, date.today()
    )
    with pytest.raises(ValueError) as exc_info:
        habit_manager.create_habit("drinking")
    assert str(exc_info.value) == "Habit: drinking already exists"


def test_create_habit_invalid_period(habit_manager):
    with pytest.raises(ValueError) as exc_info:
        habit_manager.create_habit("Drinking", "8 glass water", "7", date.today())
    assert str(exc_info.value) == "Unknown periodicity."


def test_create_empty_habit(habit_manager):
    with pytest.raises(ValueError) as exc_info:
        habit_manager.create_habit(" ", "test", Periodicity.DAILY, date.today())
    assert str(exc_info.value) == "Invalid Habit:  "
    with pytest.raises(ValueError) as exc_info:
        habit_manager.create_habit("", "test", Periodicity.DAILY, date.today())
    assert str(exc_info.value) == "Invalid Habit: "


def test_create_None_habit(habit_manager):
    with pytest.raises(ValueError) as exc_info:
        habit_manager.create_habit(None, "test", Periodicity.DAILY, date.today())
    assert str(exc_info.value) == "Invalid Habit: None"


def test_create_empty_habit_desc(habit_manager):
    with pytest.raises(ValueError) as exc_info:
        habitname = "test"
        habit_manager.create_habit(habitname, " ", Periodicity.DAILY, date.today())
    assert str(exc_info.value) == f"Empty description for Habit: {habitname}"


def test_create_None_habit_desc(habit_manager):
    with pytest.raises(ValueError) as exc_info:
        habitname = "test"
        habit_manager.create_habit(habitname, None, Periodicity.DAILY, date.today())
    assert str(exc_info.value) == f"Invalid description None for  Habit: {habitname}"


def test_create_None_habit_creation_date(habit_manager):
    with pytest.raises(ValueError) as exc_info:
        habitname = "test"
        habit_manager.create_habit(habitname, "test desc", Periodicity.DAILY, None)
    assert str(exc_info.value) == f"Invalid date for Habit: {habitname}"


def test_create_empty_habit_creation_date(habit_manager):
    with pytest.raises(ValueError) as exc_info:
        habitname = "test"
        habit_manager.create_habit(habitname, "test desc", Periodicity.DAILY, "")
    assert str(exc_info.value) == f"Invalid date for Habit: {habitname}"


def test_create_other_object_habit_creation_date(habit_manager):
    with pytest.raises(ValueError) as exc_info:
        habitname = "test"
        habit_manager.create_habit(habitname, "test desc", Periodicity.DAILY, 12)
    assert str(exc_info.value) == f"Invalid date for Habit: {habitname}"


def test_create_invalid_habit_period(habit_manager):
    with pytest.raises(ValueError) as exc_info:
        habit_manager.create_habit("test", "test desc", 3, date.today())
    assert str(exc_info.value) == "Unknown periodicity."


def test_delete_habit(habit_manager):
    # first create a habit.Then delete it.
    habit_manager.create_habit("Reading", "1 hour", Periodicity.DAILY, date.today())
    habit_manager.delete_habit("Reading")
    assert "Reading" not in habit_manager.habits


def test_delete_non_existent_habit(habit_manager):
    with pytest.raises(ValueError) as exc_info:
        habit_manager.delete_habit("nonexistent")
    assert str(exc_info.value) == "Habit: nonexistent does not exist."


def test_deactivate_activate(habit_manager):
    habit_manager.create_habit(
        "Drinking", "8 glass water", Periodicity.DAILY, date.today()
    )
    habit_manager.deactivate_habit("drinking")
    assert not habit_manager.habits["drinking"].active
    habit_manager.activate_habit("drinking")
    assert habit_manager.habits["drinking"].active


def test_activate_nonexistent_habit(habit_manager):
    with pytest.raises(ValueError) as exc_info:
        habit_manager.activate_habit("nonexistent")
    assert str(exc_info.value) == "Habit: nonexistent does not exist."


def test_deactivate_nonexistent_habit(habit_manager):
    with pytest.raises(ValueError) as exc_info:
        habit_manager.deactivate_habit("nonexistent")
    assert str(exc_info.value) == "Habit: nonexistent does not exist."


def test_dactivate_checkoff_habit(habit_manager):
    habit_manager.create_habit(
        "Drinking", "8 glass water", Periodicity.DAILY, date.today()
    )
    habit_manager.deactivate_habit("Drinking")
    with pytest.raises(ValueError) as exc_info:
        habit_manager.check_off("Drinking",date.today())
    assert str(exc_info.value) == "Inactive Habit!"


def test_check_off_habit_default_date(habit_manager):
    habit_manager.create_habit(
        "shopping", "for the week", Periodicity.WEEKLY, date.today()
    )
    today = date.today()
    habit_manager.check_off("shopping", today)
    assert today in habit_manager.habits["shopping"].completed_dates


def test_check_off_habit_custom_date(habit_manager):
    habit_manager.create_habit(
        "shopping", "for the week", Periodicity.WEEKLY, date.today()
    )
    custom_date = date(2025, 5, 1)
    habit_manager.check_off("Shopping", custom_date)
    assert custom_date in habit_manager.habits["shopping"].completed_dates


def test_check_off_nonexistent_habit(habit_manager):
    with pytest.raises(ValueError) as exc_info:
        habit_manager.check_off("nonexistent", checkoff_date=date.today())
    assert str(exc_info.value) == "Habit: nonexistent does not exist."


def test_check_off_habit_invalid_date(habit_manager):
    habitname = "test"
    habit_manager.create_habit(
        habitname, "for the week", Periodicity.WEEKLY, date.today()
    )
    with pytest.raises(ValueError) as exc_info:
        habit_manager.check_off(habitname, checkoff_date=None)
    assert str(exc_info.value) == f"Invalid checkoff date for Habit: {habitname}"


def test_view_pending_habits_daily(habit_manager):
    # create a daily habit
    today = date.today()
    habit_manager.create_habit("Drinking", "8 glass water", Periodicity.DAILY, today)
    # check of it
    habit_manager.check_off("Drinking", today)
    # create another daily habit and no check off
    habit_manager.create_habit("Meditation", "30mins", Periodicity.DAILY, today)
    assert habit_manager.view_pending_habits_daily(today) == ["meditation"]


def test_view_pending_habits_daily_invaliddate(habit_manager):
    # create a daily habit
    today = date.today()
    habit_manager.create_habit("Drinking", "8 glass water", Periodicity.DAILY, today)
    # check of it
    habit_manager.check_off("Drinking", today)
    # create another daily habit and no check off
    habit_manager.create_habit("Meditation", "30mins", Periodicity.DAILY, today)
    with pytest.raises(ValueError) as exc_info:
        habit_manager.view_pending_habits_daily(None)
    assert str(exc_info.value) == f"Invalid evaluation_date"


def test_view_pending_habits_weekly(habit_manager):
    # create a weekly habit
    today = date.today()
    habit_manager.create_habit("Cleaning", "house", Periodicity.WEEKLY, today)
    # check of it
    habit_manager.check_off("Cleaning", today)
    # create another weekly habit and no check off
    habit_manager.create_habit("Workout", "test", Periodicity.WEEKLY, today)
    assert habit_manager.view_pending_habits_weekly(today) == ["workout"]


def test_view_pending_habits_weekly_invaliddate(habit_manager):
    # create a weekly habit
    today = date.today()
    habit_manager.create_habit("Cleaning", "house", Periodicity.WEEKLY, today)
    # check of it
    habit_manager.check_off("Cleaning", today)
    # create another weekly habit and no check off
    habit_manager.create_habit("Workout", "test", Periodicity.WEEKLY, today)
    with pytest.raises(ValueError) as exc_info:
        habit_manager.view_pending_habits_weekly(None)
    assert str(exc_info.value) == f"Invalid evaluation_date"


def test_get_habit(habit_manager):
    habit_manager.create_habit(
        "Drinking", "8 glass water", Periodicity.DAILY, date.today()
    )
    assert habit_manager.get_habit("Drinking").name == "Drinking"
    assert habit_manager.get_habit("Drinking").description == "8 glass water"
    assert habit_manager.get_habit("Drinking").creation_date == date.today()
    assert habit_manager.get_habit("Drinking").completed_dates == []
    assert habit_manager.get_habit("Drinking").active == True


def test_get_habit_nonexistent_habit(habit_manager):
    with pytest.raises(ValueError) as exc_info:
        habit_manager.get_habit("nonexistent")
    assert str(exc_info.value) == "Habit: nonexistent does not exist."
