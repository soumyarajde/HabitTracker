from datetime import date, timedelta
from habittracker.habit import Habit
import logging

logger = logging.getLogger(__name__)


class DailyHabit(Habit):
    """A subclass of Habit class which represents daily habit."""

    def __init__(self, name, description, creation_date=None, active=True):
        super().__init__(name, description, creation_date, active)
        logger.debug(
            f"Initializes DailyHabit object with name:{self.name},description: {self.description},creation_date: {self.creation_date},active: {active}"
        )

    def calculate_streak(self, calculation_date):
        """
        Method to calculate streak for a given habit.If today is not in the completed dates then return the streak upto previous day.
        Args:
            calculation_date:(date) date on which streak has to be calculated.
        Raises:
            ValueError("Invalid date for streak calculation"): If invalid date is used for calculation
        Returns:
            integer:streak of a habit.
        """
        if not isinstance(calculation_date, date):
            raise ValueError("Invalid date for streak calculation")
        # if completed dates is empty streak is zero
        if not self.completed_dates:
            return 0
        streak = 0
        today = calculation_date
        # set today_flag  to check whether habit is done today or not.
        today_flag = today in self.completed_dates
        # if habit is not done today then calculate streak upto yesterday.For that today is set to previous day.
        if not today_flag:
            today = today - timedelta(days=1)
        # check for today in the completed_dates list.If today is in the list increase streak by one and today is set to previous day
        while today in self.completed_dates:
            streak += 1
            today -= timedelta(days=1)
        logger.info(f"streak for habit:{self.name} on {calculation_date} is {streak}")
        return streak
