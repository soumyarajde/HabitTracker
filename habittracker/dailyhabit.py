from datetime import datetime,date,timedelta
from habittracker.habit import Habit

class DailyHabit(Habit):
    """A subclass of Habit class which represents daily habit."""
    def __init__(self,name,description,creation_date=datetime.today().date(),active=True):
        super().__init__(name,description,creation_date,active)


    def calculate_streak(self,date=date.today()):
        """
        Calculate current streak for a given habit.If today is not in the completed dates then return the streak of yesterday.
        Args:
            date:(date) date on which streak has to be calculated.
        Returns:
            integer:streak of a habit.
        """
        # if completed dates is empty streak is zero
        if not self.completed_dates:
            return 0
        streak=0
        today=date
        #set today_flag  to check whether habit is done today or not.
        today_flag=today in self.completed_dates
        #if habit is not done today then calculate streak upto yesterday.For that today is set to previous day.
        if not today_flag:
            today=today-timedelta(days=1)
        #check for today in the completed_dates list.If today is in the list increase streak by one and today is set to previous day
        while today in self.completed_dates:
            streak+=1
            today-=timedelta(days=1)
        return streak
               

    