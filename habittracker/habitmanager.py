from datetime import date, timedelta
from habittracker.dailyhabit import DailyHabit
from habittracker.weeklyhabit import WeeklyHabit
from habittracker.database import JSONDatabase
from habittracker.constants import Periodicity
import logging

logger = logging.getLogger(__name__)


class HabitManager:
    """Manages all habits.
    Attributes:_habits{Habit}:a dictionary of Habit class objects.
                database:JsonDatabase:an instance of JsonDatabase used for databse operations.
    """

    def __init__(self, filename="db.json"):
        """Initialize HabitManager object.
        Args:
            filename(string):file name of database.
        """
        logger.debug(f"Initializing Habit Manager")
        self._habits = dict()
        self.database = JSONDatabase(str(filename))
        self._habits = self.database.retrieve_data()
        logger.debug(f"Loading database from {filename}")

    def create_habit(
        self, name=None, description=None, periodicity=None, creation_date=None
    ):
        """
        Creates a habit and add it to a dictionary and save it in the database.
        Habit name in lowercase is used as the key for each habit.
        Args:
            name(string):name of a habit
            description(string):description of a habit.
            periodicity(Enum):frequency of a habit.
            creation_date(date):date on which habit is created
        Raises:
            ValueError("Unknown periodicity."):If periodicity is not daily or weekly
            ValueError("Habit already exists"):If tries to create an existing habit.
            ValueError(f"Invalid date for Habit: {name}"): If invalid date object is passed
        """
        logger.debug(f"creating habit")
        # Check for name is None
        if name == None:
            raise ValueError(f"Invalid Habit: {name}")
        # Check for empty name
        elif name.strip() == "":
            raise ValueError(f"Invalid Habit: {name}")
        # check for habit existing or not
        elif not name.lower() in self._habits:
            # check for descriptioon is None
            if description == None:
                raise ValueError(f"Invalid description None for  Habit: {name}")
            # check for empty description
            elif description.strip() == "":
                raise ValueError(f"Empty description for Habit: {name}")
            # If invalid date is passed raise error
            if not isinstance(creation_date, date):
                raise ValueError(f"Invalid date for Habit: {name}")

            # check for periodicty daily and create the correct object
            elif periodicity == Periodicity.DAILY:
                temp_habit = DailyHabit(name, description, creation_date)
                self._habits.update({name.lower(): temp_habit})
                # check for periodicty weekly and create the correct object
            elif periodicity == Periodicity.WEEKLY:
                temp_habit = WeeklyHabit(name, description, creation_date)
                self._habits.update({name.lower(): temp_habit})
                logger.info(f"Habit {name} created.")
            # if periodicity is other than daily or weekly raise error.
            else:
                raise ValueError("Unknown periodicity.")
        # if habit name is already there raise error
        else:
            raise ValueError(f"Habit: {name} already exists")
        # update database
        self.database.save_data(self._habits)

    def delete_habit(self, name=None):
        """
        Deletes a given habit and update database.
        Args:
            name(string):name of the habit.
        Raises:
            ValueError("Habit: {name} does not exist."):If tries to delete a habit which is not in the database.
        """
        # check for habit is existing and if true remove it from form the habits dict.
        if name.lower() in self._habits:
            self._habits.pop(name.lower())
            logger.info(f"Habit: {name} deleted.")
        else:
            # habit not existing raise error
            logger.error(f"Habit: {name} not found.")
            raise ValueError(f"Habit: {name} does not exist.")
        # update database
        self.database.save_data(self._habits)

    def deactivate_habit(self, name=None):
        """
        Deactivates a habit and update database.
        Arg:
            name(str):name of the habit
        Raises:
            ValueError("Habit: {name} does not exist."):If tries to deactivate a habit which is not in the database.
        """
        # check for habit existence and if true deactivate it
        if name.lower() in self._habits:
            self._habits[name.lower()].deactivate_habit()
            logger.info(f"Habit: {name} deactivated.")
        else:
            # otherwise raise error
            logger.error(f"Habit: {name} not found.")
            raise ValueError(f"Habit: {name} does not exist.")
        # update database
        self.database.save_data(self._habits)

    def activate_habit(self, name=None):
        """
        Activates an inactive habit and update database.
        Arg:
            name(str):name of the habit
        Raises:
            ValueError("Habit: {name} does not exist."):If tries to activate a habit which is not in the database.
        """
        # check for habit existence and if true activate it
        if name.lower() in self._habits:
            self._habits[name.lower()].activate_habit()
            logger.info(f"Habit: {name} activated.")
        # otherwise raise error
        else:
            logger.error(f"Habit: {name} not found.")
            raise ValueError(f"Habit: {name} does not exist.")
        # update database
        self.database.save_data(self._habits)

    def check_off(self, name=None, checkoff_date=None):
        """
        Marks a habit as completed.Adds date to the completed dates list and update database.
        Args:
            name(str):name of the habit
            checkoff_date(date): date on which habit is  marked done.
        Raises:
            ValueError(f"Invalid checkoff date for Habit: {name}"): If check_off date is not a date object.
            ValueError("Habit: {name} does not exist."):If tries to check off a habit which is not in the database.
        """
        # check for habit existence 
        if name.lower() in self._habits:
            # check for valid date if true call habit.check_off method
            if not isinstance(checkoff_date, date):
                raise ValueError(f"Invalid checkoff date for Habit: {name}")
            else:
                self._habits[name.lower()].check_off(checkoff_date)
           
            logger.info(f"Habit: {name} checked off on {checkoff_date}")
        # otherwise raise error
        else:
            logger.error(f"Habit: {name} not found.")
            raise ValueError(f"Habit: {name} does not exist.")
        # update databse
        self.database.save_data(self._habits)

    def view_pending_habits_daily(self, evaluation_date):
        """
         Method which returns the list of daily habits to be completed today.
        Args:
            evaluation_date(date): date on which pending status is calculated
         Returns:
             list of DailyHabit objects.
        Raises:
             ValueError("Invalid evaluation_date"): If invalid date object is passed.

        """
        if not isinstance(evaluation_date, date):
            raise ValueError(f"Invalid evaluation_date")
        pending_habits_daily = []
        # check a habit is active and a daily habit
        for name in self._habits:
            if self._habits[name].active and isinstance(self._habits[name], DailyHabit):
                # if today is not in the list of completed dates add habit to the pending list.
                if evaluation_date not in self._habits[name].completed_dates:
                    pending_habits_daily.append(name)
        logger.info(f"Pending daily habits: {pending_habits_daily}")
        return pending_habits_daily

    def view_pending_habits_weekly(self, evaluation_date):
        """
         Method which returns the list of weekly habits pending to complete this week.
        Args:
            evaluation_date(date): date on which pending status is calculated
         Returns:
             list of WeeklyHabit objects.
        Raises:
             ValueError("Invalid evaluation_date"): If invalid date object is passed.

        """
        if not isinstance(evaluation_date, date):
            raise ValueError(f"Invalid evaluation_date")
        pending_habits_weekly = []
        # find current week start and end date
        current_week_start = evaluation_date - timedelta(
            days=evaluation_date.weekday()
        )  # today.weekday() is 0 for monday,1 for tuesday and so on
        current_week_end = current_week_start + timedelta(days=6)
        # check whether the habit is active and is a weekly habit.
        for name in self._habits:
            if self._habits[name].active and isinstance(
                self._habits[name], WeeklyHabit
            ):
                # if no date in the current week is in the completed dates list add it to the pending habit list.
                if not any(
                    current_week_start <= d <= current_week_end
                    for d in self._habits[name].completed_dates
                ):
                    pending_habits_weekly.append(name)
        logger.info(f"Pending weekly habits:{pending_habits_weekly}")
        return pending_habits_weekly

    @property
    def habits(self):
        """Read only view of all habits as a dict name:Habit."""
        return dict(self._habits)

    def get_habit(self, name: str):
        """
        Fetch a single habit by name (case insensitive)
        Args:
            name(str):name of habit
        Returns:
            habit(Habit):Habit object with name provided as argument.
        Raises:
            ValueError(f"Habit: {name} does not exist.").If key does not found.
        """
        try:
            logger.debug(f"fetching habit: {name}")
            return self._habits[name.lower()]
        except KeyError:
            logger.error(f"Habit: {name} not found.")
            raise ValueError(f"Habit: {name} does not exist.")
