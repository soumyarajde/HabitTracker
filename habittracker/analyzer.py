from datetime import date,timedelta
from functools import reduce
from habittracker.database import HabitDataStorage,JsonDatabase
from habittracker.habit import Habit
from habittracker.dailyhabit import DailyHabit
from habittracker.weeklyhabit import WeeklyHabit

class HabitAnalyzer:
    def __init__(self,file_path='db.json'):
        self.database=JsonDatabase(str(file_path))
        self.habits=self.database.retrieve_data()

    def get_streak(self,name,date=date.today()):
        if name.lower() in self.habits:
            return self.habits[name.lower()].calculate_streak(date)
        else:
            raise ValueError("Habit does not exist.")
        
    def get_currently_tracked_habits(self):
        return list(map(lambda habit:habit[0],filter(lambda habit:habit[1].active,self.habits.items())))
         
    def get_habits_with_same_period(self):
        return {
            'Daily Habits':list(map(lambda habit:habit[0],filter(lambda habit:isinstance(habit[1],DailyHabit),self.habits.items()))),
           'Weekly Habits':list(map(lambda habit:habit[0],filter(lambda habit:isinstance(habit[1],WeeklyHabit),self.habits.items()))),
        }
    
    def get_longest_streak(self,name):
        name=name.lower()
        if name in self.habits:
            if not self.habits[name].completed_dates:
                return 0
            
            elif isinstance(self.habits[name],DailyHabit):
                dates=sorted(self.habits[name].completed_dates)
                def reducer(acc,i):
                    current_date=dates[i]
                    previous_date=dates[i-1]
                    if current_date-previous_date==timedelta(days=1):
                        acc["current"]+=1
                        acc["max"]=max(acc["current"],acc["max"])
                    else:
                        acc["current"]=1
                    return acc
                result=reduce(reducer,range(1,len(dates)),{"current":1,"max":1})
            elif isinstance(self.habits[name],WeeklyHabit):
                #find week starting for each date in completed dates and create a new list.(monday is the starting of week)
                weeks=[]
                for date in self.habits[name].completed_dates:
                    weeks.append(date-timedelta(days=date.weekday()))
                # Eliminate duplicate entries and sort the dates.
                weeks=list(sorted(set(weeks)))
                # define reducer function which is to be used in reduce tool.
                def reducer(acc,i):
                    current_week=weeks[i]
                    previous_week=weeks[i-1]
                    if current_week-previous_week==timedelta(days=7):
                        acc["current"]+=1
                        acc["max"]=max(acc["current"],acc["max"])
                    else:
                        acc["current"]=1
                    return acc
                result=reduce(reducer,range(1,len(weeks)),{"current":1,"max":1})

            return result['max']
        else:
            raise ValueError("Habit does not exist.")
    
    
    def get_longest_streak_all(self):
            return dict(
                map(lambda habit:(habit[0],self.get_longest_streak(habit[0])),self.habits.items())
            )
if __name__=='__main__':
  
   ha=HabitAnalyzer()
   #streak=ha.get_streak("sleeping",date=date(2025,5,7))
   #print(streak)
   print(ha.get_habits_with_same_period())
   #print(ha.get_longest_streak_all())