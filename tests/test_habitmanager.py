import pytest
import json
from datetime import date
from habittracker.habitmanager import HabitManager
from habittracker.habit import Habit
from habittracker.dailyhabit import DailyHabit
from habittracker.weeklyhabit import WeeklyHabit
from habittracker.database import HabitDataStorage,JsonDatabase
import os

@pytest.fixture
def habit_manager():
    file_path = "testdb.json"
    manager=HabitManager(file_path)
    yield  manager
    if os.path.exists(file_path):
        os.remove(file_path)

def test_create_daily_habit(habit_manager):
    habit_manager.create_habit("Drinking","8 glass water","daily")
    assert "drinking" in habit_manager.habits
    assert isinstance(habit_manager.habits['drinking'],DailyHabit)

def test_create_weekly_habit(habit_manager):
    habit_manager.create_habit("shopping","for the week","weekly")
    assert "shopping" in habit_manager.habits
    assert isinstance(habit_manager.habits["shopping"],WeeklyHabit)

def test_create_habit_already_exists(habit_manager):
    habit_manager.create_habit("Drinking","8 glass water","daily")
    with pytest.raises(ValueError) as exc_info:
        habit_manager.create_habit("drinking")
    assert str(exc_info.value)=="Habit already exists"

def test_create_habit_invalid_period(habit_manager):
    with pytest.raises(ValueError) as exc_info:
        habit_manager.create_habit("Drinking","8 glass water","7")
    assert str(exc_info.value)=="Unknown periodicity."


def test_delete_habit(habit_manager):
    #first create a habit.Then delete it.
    habit_manager.create_habit("Reading","1 hour","daily")
    habit_manager.delete_habit("Reading")
    assert  "Reading" not in habit_manager.habits

def test_delete_non_existent_habit(habit_manager):
    with pytest.raises(ValueError) as exc_info:
        habit_manager.delete_habit("exercise")
    assert str(exc_info.value)=="Habit does not exist."

def test_deactivate_activate(habit_manager):
    habit_manager.create_habit("Drinking","8 glass water","daily")
    habit_manager.deactivate_habit("drinking")
    assert not habit_manager.habits['drinking'].active
    habit_manager.activate_habit("drinking")
    assert habit_manager.habits['drinking'].active

def test_check_off_habit_default_date(habit_manager):
    habit_manager.create_habit("shopping","for the week","weekly")
    habit_manager.check_off("shopping")
    today=date.today()
    assert today in habit_manager.habits["shopping"].completed_dates

def test_check_off_habit_custom_date(habit_manager):
    habit_manager.create_habit("shopping","for the week","weekly")
    custom_date=date(2025,5,1)
    habit_manager.check_off("Shopping",custom_date)
    assert custom_date in habit_manager.habits["shopping"].completed_dates

#def test_view_habit(habit_manager)
#test database integration