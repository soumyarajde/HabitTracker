from datetime import datetime,date,timedelta
from habittracker.habit import Habit


class WeeklyHabit(Habit):
    """A subclass of Habit class which represents weekly habit."""
    def __init__(self,name,description,creation_date=datetime.today().date(),active=True):
        super().__init__(name,description,creation_date,active)

    
    def calculate_streak(self):
        """Calculate and return current streak of a weekly habit.If no check off for current week return streak of previous week."""
       
        if not self.completed_dates:
            return 0
        strek=0
        today=date.today()
        completed_dates=set(self.completed_dates)
        #starts checking from the current week and go backward.
        #week starts on monday
        current_week_start=today-timedelta(days=today.weekday())
        current_week_end=current_week_start+timedelta(days=6)
        current_week_flag=any(current_week_start<=d<=current_week_end for d in completed_dates)
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

    
    
if __name__=='__main__':
    weekly_habit=WeeklyHabit("Shopping","for the week")
    
    weekly_habit.check_off(date(2025,4,8))
    weekly_habit.check_off(date(2025,4,15))
    weekly_habit.check_off(date(2025,4,18))
    weekly_habit.check_off(date(2025,4,23))
    weekly_habit.check_off(date(2025,4,30))
    ser = weekly_habit.serialize()
    d = DailyHabit.deserialize(ser)
    w = WeeklyHabit.deserialize(ser)
    print(d)
    print(w)
    #weekly_habit.check_off()
    # result=weekly_habit.calculate_current_streak()
    # print(f"streak= {result}")
    
    
    
        
        
    
       