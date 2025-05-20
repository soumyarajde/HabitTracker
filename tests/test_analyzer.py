import pytest
from datetime import date
from functools import reduce
from habittracker.analyzer import HabitAnalyzer

@pytest.fixture
def test_analyzer():
    analyzer=HabitAnalyzer("test_db.json")
    return analyzer

def test_get_currently_tracked_habit(test_analyzer):
    assert test_analyzer.get_currently_tracked_habits()==['exercise','sleeping','drinking','cleaning','shopping']

def test_get_habits_with_same_period(test_analyzer):
    assert test_analyzer.get_habits_with_same_period()=={'Daily Habits':['exercise','sleeping','drinking',],'Weekly Habits':['cleaning','shopping']}

def test_get_longest_streak(test_analyzer):
    assert test_analyzer.get_longest_streak('exercise')==15
    assert test_analyzer.get_longest_streak('sleeping')==10

def test_get_longest_streak_all(test_analyzer):
    assert test_analyzer.get_longest_streak_all()=={'sleeping':10,'drinking':10,'shopping':4,'exercise':15,'cleaning':2}

def test_longest_streak_non_existent_habit(test_analyzer):
    with pytest.raises (ValueError) as exc_info:
        test_analyzer.get_longest_streak("nonexistent")
    assert str(exc_info.value)=="Habit does not exist."

def test_get_streak(test_analyzer):
    assert test_analyzer.get_streak("sleeping",date=date(2025,5,20))==3
    assert test_analyzer.get_streak("drinking",date=date(2025,5,20))==4
    assert test_analyzer.get_streak("sleeping",date=date(2025,5,15))==5
    assert test_analyzer.get_streak("shopping",date=date(2025,5,19))==4