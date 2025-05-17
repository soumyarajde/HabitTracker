from datetime import datetime,date,timedelta
from habittracker.habit import Habit


class WeeklyHabit(Habit):
    """A subclass of Habit class which represents weekly habit."""
    def __init__(self,name,description,creation_date=datetime.today().date(),active=True):
        super().__init__(name,description,creation_date,active)

    
    def calculate_streak(self,date=date.today()):
        """
        Calculate and return current streak of a weekly habit.If no check off for current week return streak upto previous week.
        Args:
            date(date):date on which streak has to be calculated.
        Returns:
            streak(integer):streak of a habit.
        """
        # if completed dates is empty streak is zero
        if not self.completed_dates:
            return 0
        strek=0
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
            current_week_start-=timedelta(days=7)
            current_week_end-=timedelta(days=7)
        while True:
            if any(current_week_start<=d<=current_week_end for d in completed_dates):
                strek+=1
                current_week_start-=timedelta(days=7)
                current_week_end-=timedelta(days=7)
            else:
                break
        return strek

    
    

    
    
        
        
    
       