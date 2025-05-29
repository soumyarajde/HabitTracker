from datetime import date, timedelta
from functools import reduce, partial
from habittracker.dailyhabit import DailyHabit
from habittracker.weeklyhabit import WeeklyHabit
from habittracker.constants import Periodicity
import logging

logger = logging.getLogger(__name__)


def reducer(acc, i, timestamps, delta):
    """reducer function which is to be passed to functools.reduce function.
        This Updates streak counter for consecutive dates or weeks given the delta.
    Args:
        acc:dict with two keys.
            "current:current consecutive day streak length
            "max":longest streak
        i:integer index into the dates list
        timestamps: list of date objects
        delta: timedelta between dates to conunt as 1 streak
    Returns:
        acc:updated accumulator dict.
    """
    # consider date at this index and previous one.
    current_date = timestamps[i]
    previous_date = timestamps[i - 1]
    # if the difference between two dates are exactly given delta
    if current_date - previous_date == delta:
        # increase the current streak by one
        acc["current"] += 1
        # update the max streak
        acc["max"] = max(acc["current"], acc["max"])
    else:
        # otherwise reset the current streak to 1
        acc["current"] = 1
    return acc


class HabitAnalyzer:
    """
    Class for running analysis on habit data.
    Attributes:
       manager:HabitManager
    """

    def __init__(self, manager=None):
        """
        Initializes Habit Analyzer object.
        Args:
            manager(HabitManager):HabitManager object
        """
        self.manager = manager
        logger.debug(f"Initialized HabitAnalyser with habit manager {manager}")

    def get_streak(self, name, calculation_date):
        """Method to calculate streak of a given habit.
        Args:
            name(string): name of a habit
            calculation_date(date): date on which streak is to be calculated.
        Raises:
            ValueError(f"Habit: {name} does not exist."):If tries to calculate streak of a nonexistent habit.
            ValueError("Invalid date give for streak calculation"): If calculation_date is not valid
        Returns:
            streak(integer):streak of a habit.
        """
        logger.debug(f"Computing streak for habit {name} on date {calculation_date}")
        if not isinstance(calculation_date, date):
            raise ValueError("Invalid date give for streak calculation")
        # check for habit existence and call the calculate_streak function
        if name.lower() in self.manager.habits:
            return self.manager.habits[name.lower()].calculate_streak(calculation_date)
        # when habit does not exist raise error
        else:
            logger.error(f"Habit {name} not found while calculating get_steak.")
            raise ValueError(f"Habit: {name} does not exist.")

    def get_currently_tracked_habits(self):
        """
        Method to return a list of currently tracked habits. Currently tracked habits means currently active habits.
        Returns:
            list:list of habit class objects
        """
        logger.debug(f"checking currently tracked habits.")
        # filter only those (name,Habit object)pairs where Habit object is active
        active_habits = filter(
            lambda habit: habit[1].active, self.manager.habits.items()
        )
        # from each tuple pick only the name(key)
        habit_names = map(lambda habit: habit[0], active_habits)
        # convert map object into a list and return
        return list(habit_names)

    def get_habits_with_same_period(self, period):
        """Method to filter habits with same periodicity.
        Args:
            period:Enum of Periodicity
        Returns:
            list:list of habit names

        """

        if period == Periodicity.DAILY:
            class_name = DailyHabit
        if period == Periodicity.WEEKLY:
            class_name = WeeklyHabit

        logger.debug(f"Fetching habits with same periodicity.")
        # filter those active (name, Habit) pairs based on the period
        _habits = filter(
            lambda habit: isinstance(habit[1], class_name) and habit[1].active,
            self.manager.habits.items(),
        )
        # from each tuple pull out only name(key)
        _habits_names = list(map(lambda habit: habit[0], _habits))
        return _habits_names

    def get_longest_streak(self, name):
        """Method to calculate longest streak of a given habit.
        Args:
            name(string):name of a habit
        Raises:
            ValueError("Habit does not exist."):if tries to get streak of a nonexistent habit.
        Returns:
            integer:longest streak
        """
        logger.debug(f"computing longest streak for habit: {name}")
        # convert name into lowercase which is the used as key in the habit database
        name = name.lower()
        if name in self.manager.habits:
            # streak is zero when completed_dates is empty.
            if not self.manager.habits[name].completed_dates:
                logger.debug(f"No completed dates for habit: {name}")
                return 0
            # check whether a habit is daily
            elif isinstance(self.manager.habits[name], DailyHabit):
                # eliminate duplicate entries and sort dates in ascending order
                dates = list(sorted(set(self.manager.habits[name].completed_dates)))
                # Run the reducer across all inices from 1 to len(dates)-1
                # with initial current and max streak set to 1
                reduce_days = partial(
                    reducer, timestamps=dates, delta=timedelta(days=1)
                )
                result = reduce(
                    reduce_days, range(1, len(dates)), {"current": 1, "max": 1}
                )

            # check a habit is weekly habit?
            elif isinstance(self.manager.habits[name], WeeklyHabit):
                # find week starting for each date in completed dates and create a new list.(monday is the starting of week)
                weeks = []
                for date in self.manager.habits[name].completed_dates:
                    weeks.append(date - timedelta(days=date.weekday()))
                # Eliminate duplicate entries and sort the dates.
                weeks = list(sorted(set(weeks)))

                reduce_weeks = partial(
                    reducer, timestamps=weeks, delta=timedelta(days=7)
                )
                result = reduce(
                    reduce_weeks, range(1, len(weeks)), {"current": 1, "max": 1}
                )
            logger.info(f"longest streak for habit:{name} is {result['max']}")
            return result["max"]
        else:
            logger.error(
                f"Habit: {name} not found while calculating the longest streak."
            )
            raise ValueError(f"Habit: {name} does not exist.")

    def get_longest_streak_all(self):
        """Method to get longest streak of all habits.
        Returns:
            dictionary:{habit name:longest streak}"""
        logger.debug(f"Computing longest streak for all habits")
        # filter active habits
        active = filter(lambda habit: habit[1].active, self.manager.habits.items())
        # for each active habit call method to calculate longest streak
        # convert map object into dict
        return dict(
            map(lambda habit: (habit[0], self.get_longest_streak(habit[0])), active)
        )
