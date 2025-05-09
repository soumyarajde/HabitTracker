from datetime import datetime,date,timedelta
from habit import Habit

class DailyHabit(Habit):
    """A subclass of Habit class which represents daily habit."""
    def __init__(self,name,description,creation_date=datetime.today().date(),active=True):
        super().__init__(name,description,creation_date,active)


    def calculate_streak(self):
        """Calculate current streak for a given habit.If today is not in the completed dates then return the streak of yesterday."""
        if not self.completed_dates:
            return 0
        today_flag=date.today()in self.completed_dates
        streak=0
        today=date.today()
        if not today_flag:
            today=today-timedelta(days=1)
        
        while today in self.completed_dates:
            streak+=1
            today-=timedelta(days=1)
        return streak
               
    
       



if __name__=='__main__':
    habit=DailyHabit("Reading","30 mins")
   # habit.check_off(date=date(2025,5,5))
    #habit.check_off(date(2025,5,6))
    #habit.check_off(date(2025,5,7))
    streak=habit.calculate_streak()
    print(streak)