import pytest
from datetime import date
from functools import reduce
from habittracker.analyzer import HabitAnalyzer
from habittracker.habitmanager import HabitManager
from habittracker.constants import Periodicity

@pytest.fixture
def test_analyzer():
    manager=HabitManager(filename="test_db.json")
    analyzer=HabitAnalyzer(manager)
    return analyzer

def test_get_currently_tracked_habit(test_analyzer):
    assert test_analyzer.get_currently_tracked_habits()==['exercise','sleeping','drinking','cleaning','shopping','reading']

def test_get_habits_with_same_period_daily(test_analyzer):
    assert test_analyzer.get_habits_with_same_period(period=Periodicity.DAILY)==['exercise','sleeping','drinking','reading']#'Weekly Habits':['cleaning','shopping']

def test_get_habits_with_same_period_weekly(test_analyzer):
    assert test_analyzer.get_habits_with_same_period(period=Periodicity.WEEKLY)==['cleaning','shopping']

def test_get_longest_streak(test_analyzer):
    assert test_analyzer.get_longest_streak('exercise')==15
    assert test_analyzer.get_longest_streak('sleeping')==10
    assert test_analyzer.get_longest_streak('reading')==0
    assert test_analyzer.get_longest_streak('cleaning')==2

def test_get_longest_streak_all(test_analyzer):
    assert test_analyzer.get_longest_streak_all()=={'sleeping':10,'drinking':10,'shopping':4,'exercise':15,'cleaning':2,'reading':0}

def test_longest_streak_non_existent_habit(test_analyzer):
    with pytest.raises (ValueError) as exc_info:
        test_analyzer.get_longest_streak("nonexistent")
    assert str(exc_info.value)=="Habit: nonexistent does not exist."

def test_get_streak(test_analyzer):
    assert test_analyzer.get_streak("sleeping",date=date(2025,5,20))==3
    assert test_analyzer.get_streak("drinking",date=date(2025,5,20))==4
    assert test_analyzer.get_streak("sleeping",date=date(2025,5,15))==5
    assert test_analyzer.get_streak("shopping",date=date(2025,5,19))==4
    assert test_analyzer.get_streak("cleaning",date=date(2025,5,15))==1

def test_get_streak_no_completion(test_analyzer):
    assert test_analyzer.get_streak('reading')==0