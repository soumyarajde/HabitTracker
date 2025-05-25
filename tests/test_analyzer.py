import os
import pytest
from datetime import date
from functools import reduce
from habittracker.analyzer import HabitAnalyzer
from habittracker.habitmanager import HabitManager
from habittracker.constants import Periodicity


@pytest.fixture
def test_analyzer():
    filename="test_ha.json"
    # ensure file does not exist before creating tests, to sovle problems if file is not deleted somehow from last test run
    if os.path.exists(filename):
        os.remove(filename)
    hm = HabitManager(filename)
    hm.create_habit(name="exercise",
                    description="morning walk",
                    periodicity=Periodicity.DAILY)
    hm.check_off("exercise", date(2025, 4, 21))
    hm.check_off("exercise", date(2025, 4, 22))
    hm.check_off("exercise", date(2025, 4, 23))
    hm.check_off("exercise", date(2025, 4, 24))
    hm.check_off("exercise", date(2025, 4, 25))
    hm.check_off("exercise", date(2025, 4, 26))
    hm.check_off("exercise", date(2025, 4, 27))
    hm.check_off("exercise", date(2025, 4, 28))
    hm.check_off("exercise", date(2025, 4, 29))
    hm.check_off("exercise", date(2025, 4, 30))
    hm.check_off("exercise", date(2025, 5,  1))
    hm.check_off("exercise", date(2025, 5,  2))
    hm.check_off("exercise", date(2025, 5,  3))
    hm.check_off("exercise", date(2025, 5,  4))
    hm.check_off("exercise", date(2025, 5,  5))
    hm.check_off("exercise", date(2025, 5,  7))
    hm.check_off("exercise", date(2025, 5,  8))
    hm.check_off("exercise", date(2025, 5,  9))
    hm.check_off("exercise", date(2025, 5, 10))
    hm.check_off("exercise", date(2025, 5, 11))
    hm.check_off("exercise", date(2025, 5, 12))
    hm.check_off("exercise", date(2025, 5, 13))
    hm.check_off("exercise", date(2025, 5, 14))
    hm.check_off("exercise", date(2025, 5, 15))
    hm.check_off("exercise", date(2025, 5, 16))
    hm.check_off("exercise", date(2025, 5, 17))
    hm.check_off("exercise", date(2025, 5, 18))
    hm.check_off("exercise", date(2025, 5, 19))
    hm.check_off("exercise", date(2025, 5, 20))

    hm.create_habit(name="sleeping",
                    description="8 hours",
                    periodicity=Periodicity.DAILY)
    hm.check_off("sleeping", date(2025, 4, 21))
    hm.check_off("sleeping", date(2025, 4, 22))
    hm.check_off("sleeping", date(2025, 4, 23))
    hm.check_off("sleeping", date(2025, 4, 24))
    hm.check_off("sleeping", date(2025, 4, 25))
    hm.check_off("sleeping", date(2025, 4, 26))
    hm.check_off("sleeping", date(2025, 4, 27))
    hm.check_off("sleeping", date(2025, 4, 28))
    hm.check_off("sleeping", date(2025, 4, 29))
    hm.check_off("sleeping", date(2025, 4, 30))
    hm.check_off("sleeping", date(2025, 5,  2))
    hm.check_off("sleeping", date(2025, 5,  3))
    hm.check_off("sleeping", date(2025, 5,  4))
    hm.check_off("sleeping", date(2025, 5,  5))
    hm.check_off("sleeping", date(2025, 5,  6))
    hm.check_off("sleeping", date(2025, 5,  7))
    hm.check_off("sleeping", date(2025, 5,  8))
    hm.check_off("sleeping", date(2025, 5, 11))
    hm.check_off("sleeping", date(2025, 5, 12))
    hm.check_off("sleeping", date(2025, 5, 13))
    hm.check_off("sleeping", date(2025, 5, 14))
    hm.check_off("sleeping", date(2025, 5, 15))
    hm.check_off("sleeping", date(2025, 5, 16))
    hm.check_off("sleeping", date(2025, 5, 18))
    hm.check_off("sleeping", date(2025, 5, 19))
    hm.check_off("sleeping", date(2025, 5, 20))

    hm.create_habit(name="drinking",
                    description="2 ltrs water",
                    periodicity=Periodicity.DAILY)

    hm.check_off("drinking", date(2025, 4, 21))
    hm.check_off("drinking", date(2025, 4, 22))
    hm.check_off("drinking", date(2025, 4, 23))
    hm.check_off("drinking", date(2025, 4, 24))
    hm.check_off("drinking", date(2025, 4, 26))
    hm.check_off("drinking", date(2025, 4, 27))
    hm.check_off("drinking", date(2025, 4, 28))
    hm.check_off("drinking", date(2025, 4, 29))
    hm.check_off("drinking", date(2025, 5,  1))
    hm.check_off("drinking", date(2025, 5,  2))
    hm.check_off("drinking", date(2025, 5,  3))
    hm.check_off("drinking", date(2025, 5,  4))
    hm.check_off("drinking", date(2025, 5,  5))
    hm.check_off("drinking", date(2025, 5,  6))
    hm.check_off("drinking", date(2025, 5,  7))
    hm.check_off("drinking", date(2025, 5,  8))
    hm.check_off("drinking", date(2025, 5,  9))
    hm.check_off("drinking", date(2025, 5, 10))
    hm.check_off("drinking", date(2025, 5, 12))
    hm.check_off("drinking", date(2025, 5, 13))
    hm.check_off("drinking", date(2025, 5, 14))
    hm.check_off("drinking", date(2025, 5, 16))
    hm.check_off("drinking", date(2025, 5, 17))
    hm.check_off("drinking", date(2025, 5, 18))
    hm.check_off("drinking", date(2025, 5, 19))

    hm.create_habit(name="cleaning",
                    description="cleaning house",
                    periodicity=Periodicity.WEEKLY)
    hm.check_off("cleaning", date(2025, 4, 22))
    hm.check_off("cleaning", date(2025, 4, 29))
    hm.check_off("cleaning", date(2025, 5, 13))
    hm.check_off("cleaning", date(2025, 5, 20))

    hm.create_habit(name="shopping",
                    description="for the week",
                    periodicity=Periodicity.WEEKLY)
    hm.check_off("shopping", date(2025, 4, 22))
    hm.check_off("shopping", date(2025, 4, 30))
    hm.check_off("shopping", date(2025, 5,  6))
    hm.check_off("shopping", date(2025, 5, 13))

    hm.create_habit(name="reading",
                    description="30 mins",
                    periodicity=Periodicity.DAILY)
    
    hm.create_habit(name="inactive habit",
                    description="30 mins",
                    periodicity=Periodicity.DAILY)
    hm.deactivate_habit("inactive habit")

    hm.create_habit(name="repeating habit",
                    description="description",
                    periodicity=Periodicity.DAILY)
    hm.check_off("repeating habit", date(2025, 5, 10))
    hm.check_off("repeating habit", date(2025, 5, 9))
    hm.check_off("repeating habit", date(2025, 5, 11))
    hm.check_off("repeating habit", date(2025, 5, 11))
    hm.check_off("repeating habit", date(2025, 5, 12))
    hm.check_off("repeating habit", date(2025, 5, 13))
    hm.check_off("repeating habit", date(2025, 5, 20))
    hm.check_off("repeating habit", date(2025, 5, 20))
    hm.check_off("repeating habit", date(2025, 5, 20))
    hm.check_off("repeating habit", date(2025, 5, 21))
    hm.check_off("repeating habit", date(2025, 5, 21))
    hm.check_off("repeating habit", date(2025, 5, 22))

    
    hm.create_habit(name="repeating weekly habit",
                    description="description",
                    periodicity=Periodicity.WEEKLY)
    hm.check_off("repeating weekly habit", date(2025, 5, 10))
    hm.check_off("repeating weekly habit", date(2025, 5, 7))
    hm.check_off("repeating weekly habit", date(2025, 5, 13))
    hm.check_off("repeating weekly habit", date(2025, 5, 15))
    hm.check_off("repeating weekly habit", date(2025, 5, 21))
    hm.check_off("repeating weekly habit", date(2025, 5, 1))
    
    

    analyzer = HabitAnalyzer(hm)
    yield analyzer
    if os.path.exists(filename):
        os.remove(filename)



def test_get_currently_tracked_habit(test_analyzer):
    assert test_analyzer.get_currently_tracked_habits() == [
        "exercise",
        "sleeping",
        "drinking",
        "cleaning",
        "shopping",
        "reading",
        "repeating habit",
        "repeating weekly habit"

    ]
    assert "inactive habit" not in test_analyzer.get_currently_tracked_habits()


def test_get_habits_with_same_period_daily(test_analyzer):
    assert test_analyzer.get_habits_with_same_period(period=Periodicity.DAILY) == [
        "exercise",
        "sleeping",
        "drinking",
        "reading",
        "repeating habit"
    ]  


def test_get_habits_with_same_period_weekly(test_analyzer):
    assert test_analyzer.get_habits_with_same_period(period=Periodicity.WEEKLY) == [
        "cleaning",
        "shopping",
        "repeating weekly habit"
    ]


def test_get_longest_streak(test_analyzer):
    assert test_analyzer.get_longest_streak("exercise") == 15
    assert test_analyzer.get_longest_streak("sleeping") == 10
    assert test_analyzer.get_longest_streak("reading") == 0
    assert test_analyzer.get_longest_streak("cleaning") == 2


def test_get_longest_streak_all(test_analyzer):
    assert test_analyzer.get_longest_streak_all() == {
        "sleeping": 10,
        "drinking": 10,
        "shopping": 4,
        "exercise": 15,
        "cleaning": 2,
        "reading": 0,
        "repeating habit": 5,
        "repeating weekly habit":4,
    }


def test_longest_streak_non_existent_habit(test_analyzer):
    with pytest.raises(ValueError) as exc_info:
        test_analyzer.get_longest_streak("nonexistent")
    assert str(exc_info.value) == "Habit: nonexistent does not exist."


def test_get_streak(test_analyzer):
    assert test_analyzer.get_streak("sleeping", date=date(2025, 5, 20)) == 3
    assert test_analyzer.get_streak("drinking", date=date(2025, 5, 20)) == 4
    assert test_analyzer.get_streak("sleeping", date=date(2025, 5, 15)) == 5
    assert test_analyzer.get_streak("shopping", date=date(2025, 5, 19)) == 4
    assert test_analyzer.get_streak("cleaning", date=date(2025, 5, 15)) == 1

def test_get_streak_repeating_dates_daily(test_analyzer):
    assert test_analyzer.get_streak("repeating habit", date=date(2025, 5, 21)) == 2
    assert test_analyzer.get_streak("repeating habit", date=date(2025, 5, 22)) == 3

def test_get_longest_streak_repeating_daily(test_analyzer):
    assert test_analyzer.get_longest_streak("repeating habit") == 5

def test_get_streak_repeating_dates_weekly(test_analyzer):
    assert test_analyzer.get_streak("repeating weekly habit", date=date(2025, 5, 21)) == 4
    assert test_analyzer.get_streak("repeating weekly habit", date=date(2025, 5, 15)) == 3


def test_get_streak_no_completion(test_analyzer):
    assert test_analyzer.get_streak("reading") == 0
