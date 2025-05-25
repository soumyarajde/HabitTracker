from datetime import datetime,date,timedelta
from habittracker.habit import Habit
import logging
logger = logging.getLogger(__name__)

class WeeklyHabit(Habit):
    """A subclass of Habit class which represents weekly habit."""
    def __init__(self,name,description,creation_date=datetime.today().date(),active=True):
        super().__init__(name,description,creation_date,active)
        logger.debug(f"Initializes WeeklyHabit object with name:{self.name},description: {self.description},creation_date: {self.creation_date},active: {active}")

    
    def calculate_streak(self,date=date.today()):
        """
        Method to calculate  current streak of a weekly habit.If no check off for current week return streak upto previous week.
        Args:
            date(date):date on which streak has to be calculated.
        Returns:
            streak(integer):streak of a habit.
        """
        # if completed dates is empty streak is zero
        if not self.completed_dates:
            return 0
        streak=0
        today=date
        # eliminate duplicate entries by converting into set
        completed_dates=set(self.completed_dates)
        #starts checking from the current week and go backward.
        #week starts on monday
        current_week_start=today-timedelta(days=today.weekday())#today.weekday() is 0 for monday,1 for tuesday and so on
        current_week_end=current_week_start+timedelta(days=6)
        #check whether habit is done or not in the current week.
        # That is any date between start and end dates of current week is in the completed dates  list.
        current_week_flag=any(current_week_start<=d<=current_week_end for d in completed_dates)
        #if habit not done during current week calculate streak upto previous week.
        if not current_week_flag:
        #current week is now previous week.week start date is 7days before current week start.
        # week end is 7 days before current week end.   
            current_week_start-=timedelta(days=7)
            current_week_end-=timedelta(days=7)
        #check for date between current week start and week end in the completed dates list.
        while True:
            if any(current_week_start<=d<=current_week_end for d in completed_dates):
                #if at least one date in the current week is in list incarese streak by 1.
                streak+=1
                current_week_start-=timedelta(days=7)
                current_week_end-=timedelta(days=7)
            else:
                break
        logger.info(f"streak for habit:{self.name} on {date} is {streak}")
        return streak

    
    

    
    
        
        
    
       