import pytest
from datetime import date,datetime,timedelta
from habittracker.habit import Habit
from habittracker.weeklyhabit import WeeklyHabit

@pytest.fixture
def weekly_habit():
    habit=WeeklyHabit("TestName","Test description")
    return habit

def test_calculate_streak_empty(weekly_habit):
    # no check off
    assert weekly_habit.calculate_streak()==0

def test_calculate_streak_includes_current_week(weekly_habit):
    # mark last three weeks including current week as completed.
    today=date.today()
    weekly_habit.completed_dates=[today-timedelta(days=7*i)for i in range(3)]
    assert weekly_habit.calculate_streak()==3

def test_calculate_streak_excludes_current_week(weekly_habit):
    #mark last three weeks excluding current week as completed.
    today=date.today()
    weekly_habit.completed_dates=[today-timedelta(days=7*i)for i in range(1,4)]
    assert weekly_habit.calculate_streak()==3

def test_calculate_streak_noncontinuous_weeks(weekly_habit):
    # mark current week and the two weeks before last week as completed.last week has no check off.
    today=date.today()
    weekly_habit.completed_dates=[today,today-timedelta(days=14),today-timedelta(days=21)]
    assert weekly_habit.calculate_streak()==1

def test_calculate_streak_multiple_checkoff_same_week(weekly_habit):
    # multiple check off in a single week
    day=date(2025,5,9)#friday
    weekly_habit.completed_dates=[day,day-timedelta(days=2)]
    assert weekly_habit.calculate_streak(date=date(2025,5,9))==1

def test_calculate_streak_unsorted_checkoff_dates(weekly_habit):
    today=date.today()
    weekly_habit.completed_dates=[today,today-timedelta(days=14),today-timedelta(days=7)]
    assert weekly_habit.calculate_streak()==3

     