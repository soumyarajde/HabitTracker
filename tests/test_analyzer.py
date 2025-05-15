import pytest
from datetime import timedelta,date
from functools import reduce
from habittracker.database import HabitDataStorage,JsonDatabase
from habittracker.habit import Habit
from habittracker.dailyhabit import DailyHabit
from habittracker.weeklyhabit import WeeklyHabit
from habittracker.analyzer import HabitAnalyzer

@pytest.fixture
def test_analyzer():
    analyzer=HabitAnalyzer("test_db.json")
    return analyzer

def test_get_currently_tracked_habit(test_analyzer):
    assert test_analyzer.get_currently_tracked_habits()==['sleeping','reading','shopping','exercise','cleaning']

def test_get_habits_with_same_period(test_analyzer):
    assert test_analyzer.get_habits_with_same_period()=={'Daily Habits':['sleeping','reading','exercise'],'Weekly Habits':['shopping','cleaning']}

def test_get_longest_streak(test_analyzer):
    assert test_analyzer.get_longest_streak('sleeping')==7
    assert test_analyzer.get_longest_streak('cleaning')==2

def test_get_longest_streak_all(test_analyzer):
    assert test_analyzer.get_longest_streak_all()=={'sleeping':7,'reading':5,'shopping':2,'exercise':4,'cleaning':2}

def test_longest_streak_non_existent_habit(test_analyzer):
    with pytest.raises (ValueError) as exc_info:
        test_analyzer.get_longest_streak("nonexistent")
    assert str(exc_info.value)=="Habit does not exist."

def test_get_streak(test_analyzer):
    assert test_analyzer.get_streak("sleeping",date=date(2025,5,7))==7
    assert test_analyzer.get_streak("reading",date=date(2025,5,7))==1
    assert test_analyzer.get_streak("sleeping",date=date(2025,5,5))==5
    assert test_analyzer.get_streak("shopping",date=date(2025,5,7))==2