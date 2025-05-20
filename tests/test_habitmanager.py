import pytest
from datetime import date
from habittracker.habitmanager import HabitManager
from habittracker.dailyhabit import DailyHabit
from habittracker.weeklyhabit import WeeklyHabit
from habittracker.constants import Periodicity
import os

@pytest.fixture
def habit_manager():
    file_path = "testdb.json"
    manager=HabitManager(file_path)
    yield  manager
    if os.path.exists(file_path):
        os.remove(file_path)

def test_create_daily_habit(habit_manager):
    habit_manager.create_habit("Drinking","8 glass water",Periodicity.DAILY)
    assert "drinking" in habit_manager.habits
    assert isinstance(habit_manager.habits['drinking'],DailyHabit)

def test_create_weekly_habit(habit_manager):
    habit_manager.create_habit("shopping","for the week",Periodicity.WEEKLY)
    assert "shopping" in habit_manager.habits
    assert isinstance(habit_manager.habits["shopping"],WeeklyHabit)

def test_create_habit_already_exists(habit_manager):
    habit_manager.create_habit("Drinking","8 glass water",Periodicity.DAILY)
    with pytest.raises(ValueError) as exc_info:
        habit_manager.create_habit("drinking")
    assert str(exc_info.value)=="Habit already exists"

def test_create_habit_invalid_period(habit_manager):
    with pytest.raises(ValueError) as exc_info:
        habit_manager.create_habit("Drinking","8 glass water","7")
    assert str(exc_info.value)=="Unknown periodicity."

# TODO test_create_empty_habit #inputvalidation
def test_create_empty_habit(habit_manager):
    with pytest.raises(ValueError) as exc_info:
        habit_manager.create_habit(" ","test",Periodicity.DAILY)
    assert str(exc_info.value)=="Invalid Habit!"
    with pytest.raises(ValueError) as exc_info:
        habit_manager.create_habit(None,"test",Periodicity.DAILY)
    assert str(exc_info.value)=="Invalid Habit!"

def test_delete_habit(habit_manager):
    #first create a habit.Then delete it.
    habit_manager.create_habit("Reading","1 hour",Periodicity.DAILY)
    habit_manager.delete_habit("Reading")
    assert  "Reading" not in habit_manager.habits

def test_delete_non_existent_habit(habit_manager):
    with pytest.raises(ValueError) as exc_info:
        habit_manager.delete_habit("exercise")
    assert str(exc_info.value)=="Habit does not exist."

def test_deactivate_activate(habit_manager):
    habit_manager.create_habit("Drinking","8 glass water",Periodicity.DAILY)
    habit_manager.deactivate_habit("drinking")
    assert not habit_manager.habits['drinking'].active
    habit_manager.activate_habit("drinking")
    assert habit_manager.habits['drinking'].active

    
def test_dactivate_checkoff_habit(habit_manager):
    habit_manager.create_habit("Drinking","8 glass water",Periodicity.DAILY)
    habit_manager.deactivate_habit("Drinking")
    with pytest.raises(ValueError) as exc_info:
        habit_manager.check_off("Drinking")
    assert str(exc_info.value)=="Inactive Habit!"

def test_check_off_habit_default_date(habit_manager):
    habit_manager.create_habit("shopping","for the week",Periodicity.WEEKLY)
    habit_manager.check_off("shopping")
    today=date.today()
    assert today in habit_manager.habits["shopping"].completed_dates

def test_check_off_habit_custom_date(habit_manager):
    habit_manager.create_habit("shopping","for the week",Periodicity.WEEKLY)
    custom_date=date(2025,5,1)
    habit_manager.check_off("Shopping",custom_date)
    assert custom_date in habit_manager.habits["shopping"].completed_dates

def test_view_pending_habits_daily(habit_manager):
    #create a daily habit
    habit_manager.create_habit("Drinking","8 glass water",Periodicity.DAILY)
    #check of it
    habit_manager.check_off("Drinking")
    #create another daily habit and no check off
    habit_manager.create_habit("Meditation","30mins",Periodicity.DAILY)
    assert habit_manager.view_pending_habits_daily()==["meditation"]

def test_view_pending_habits_weekly(habit_manager):
    #create a weekly habit
    habit_manager.create_habit("Cleaning","house",Periodicity.WEEKLY)
    #check of it
    habit_manager.check_off("Cleaning")
    #create another weekly habit and no check off
    habit_manager.create_habit("Workout","test",Periodicity.WEEKLY)
    assert habit_manager.view_pending_habits_weekly()==["workout"]

    
