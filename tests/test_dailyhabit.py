import pytest
from datetime import date, timedelta
from habittracker.dailyhabit import DailyHabit


@pytest.fixture
def daily_habit():
    habit = DailyHabit("Exercise", "walk 5km", date(2025, 4, 20))
    return habit


def test_calculate_streak_empty_completed_dates(daily_habit):
    # no check off
    assert daily_habit.calculate_streak(date(2025, 4, 20)) == 0


def test_calculate_streak_empty_invaliddate(daily_habit):
    with pytest.raises(ValueError) as exc_info:
        daily_habit.calculate_streak(None)
    assert str(exc_info.value) == f"Invalid date for streak calculation"


def test_calculate_streak_today_checked(daily_habit):
    # mark today and last three days as completed
    today = date.today()
    daily_habit.completed_dates = [today - timedelta(days=i) for i in range(4)]
    assert daily_habit.calculate_streak(today) == 4


def test_calculate_streak_today_checked_invaliddate(daily_habit):
    # mark today and last three days as completed
    today = date.today()
    daily_habit.completed_dates = [today - timedelta(days=i) for i in range(4)]
    with pytest.raises(ValueError) as exc_info:
        daily_habit.calculate_streak(None)
    assert str(exc_info.value) == f"Invalid date for streak calculation"


def test_calculate_streak_today_not_checked(daily_habit):
    # mark last three days excluding today as completed.
    today = date.today()
    daily_habit.completed_dates = [today - timedelta(days=i) for i in range(1, 4)]
    assert daily_habit.calculate_streak(today) == 3


def test_calculate_streak_single_day_today(daily_habit):
    # only today is in completed dates.
    today = date.today()
    daily_habit.completed_dates = [today]
    assert daily_habit.calculate_streak(today) == 1


def test_calculate_streak_single_day_yesterday(daily_habit):
    # only yesterday is done.
    today = date.today()
    daily_habit.completed_dates = [today - timedelta(days=1)]
    assert daily_habit.calculate_streak(today) == 1


def test_calculate_streak_with_gap(daily_habit):
    # day before yesterday done, yesterday not,today done.
    today = date.today()
    daily_habit.completed_dates = [today, today - timedelta(days=2)]
    assert daily_habit.calculate_streak(today) == 1


def test_calculate_streak_disrupted(daily_habit):
    # day before yesterday done yesterday and today not.
    today = date.today()
    daily_habit.completed_dates = [today - timedelta(days=2)]
    assert daily_habit.calculate_streak(today) == 0


def test_calculate_streak_unsorted_checkoff_dates(daily_habit):
    # check off is done not in order.
    today = date.today()
    daily_habit.completed_dates = [
        today - timedelta(days=2),
        today,
        today - timedelta(days=1),
    ]
    assert daily_habit.calculate_streak(today) == 3


if __name__ == "__main__":
    pytest.main()
