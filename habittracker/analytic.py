from habittracker.database import HabitDataStorage,JsonDatabase
from habittracker.habit import Habit
from habittracker.dailyhabit import DailyHabit
from habittracker.weeklyhabit import WeeklyHabit

class HabitAnalyzer:
    def __init__(self):
        self.database=JsonDatabase('db.json')
        self.habits=self.database.retrieve_data()

    def get_streak(self,name):
        if name.lower() in self.habits:
            return self.habits[name.lower()].calculate_streak()
        
    def get_currently_tracked_habits(self):
        return list(map(lambda habit:habit[0],filter(lambda habit:habit[1].active,self.habits.items())))
         
    def get_habits_with_same_period(self):
        return {
            'Daily Habits':list(map(lambda habit:habit[0],filter(lambda habit:isinstance(habit[1],DailyHabit),self.habits.items()))),
           ' Weekly Habits':list(map(lambda habit:habit[0],filter(lambda habit:isinstance(habit[1],WeeklyHabit),self.habits.items()))),
        }
    # def get_longest_streak():
        
    #     pass
    # def get_longest_streak_all():
    #     pass


if __name__=='__main__':
  
   ha=HabitAnalyzer()
   #streak=ha.get_streak("reading")
   #print(streak)
   print(ha.get_currently_tracked_habits())
   print(ha.get_habits_with_same_period())