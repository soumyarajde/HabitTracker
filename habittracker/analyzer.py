from datetime import date,timedelta
from functools import reduce
from habittracker.database import JsonDatabase
from habittracker.dailyhabit import DailyHabit
from habittracker.weeklyhabit import WeeklyHabit

class HabitAnalyzer:
    """
    Class for running analysis on habit data storage database.
    Attributes:
       database:JsonDatabase()
    """
    def __init__(self,file_name='db.json'):
        """
        Initializes Habit Analyzer object.
        Args:
            file_name(string):name of database
        """
        self.database=JsonDatabase(file_name)
        
    def get_streak(self,name,date=date.today()):
        """Method to calculate streak of a given habit.
        Args:
            name(string):name of a habit
            date(date):date on which streak is to be calculated.
        Raises:
            ValueError("Habit does not exist."):If tries to calculate streak of a nonexistent habit.
        Returns:
            streak(integer):streak of a habit.
        """
        # load the habits data into habits
        habits=self.database.retrieve_data()
        # check for habit existence and call the calculate_streak function
        if name.lower() in habits:
            return habits[name.lower()].calculate_streak(date)
        # when habit does not exist raise error
        else:
            raise ValueError("Habit does not exist.")
        
    def get_currently_tracked_habits(self):
        """
        Method to return a list of currently tracked habits.Currently tracked habits means currently active habits.
        Returns:
            list:list of habit class objects
        """
        # load database
        habits=self.database.retrieve_data()
        #filter only those (name,Habit object)pairs where Habit object is active
        #Each item is a tuple (name,Habit object)
        # from each tuple pick only the name(key)
        # convert map object into a list and return
        return list(map(lambda habit:habit[0],filter(lambda habit:habit[1].active,habits.items())))
         
    def get_habits_with_same_period(self):
        """Method to filter habits with same periodicity.
        Returns:
            dict:dictionary of Daily Habits and Weekly Habits.
            {"Daily Habits":[DailyHabit objects],"Weekly Habits":[WeeklyHabit objects]}
        """
        # load database
        habits=self.database.retrieve_data()
        # filter those (name, Habit) pairs where Habit is a DailyHabit object
        # from each tuple pull out only name(key)
        #convert the map object into a list.
        # use 'Daily Habits' as key and list as value
        #repeat the same for 'Weekly Habit'
        # return a dictionary with two key-value pairs 'Daily Habits' and 'Weekly Habits'


        return {
            'Daily Habits':list(map(lambda habit:habit[0],filter(lambda habit:isinstance(habit[1],DailyHabit),habits.items()))),
           'Weekly Habits':list(map(lambda habit:habit[0],filter(lambda habit:isinstance(habit[1],WeeklyHabit),habits.items()))),
        }
    
    def get_longest_streak(self,name):
        """Method to calculate longest streak of a given habit.
        Args:
            name(string):name of a habit
        Raises:
            ValueError("Habit does not exist."):if tries to get streak of a nonexistent habit.
        Returns:
            integer:longest streak
        """
        habits=self.database.retrieve_data()
        name=name.lower()
        if name in habits:
        # streak is zero when completed_dates is empty.
            if not habits[name].completed_dates:
                return 0
        # check whether a habit is daily  
            elif isinstance(habits[name],DailyHabit):
        #eliminate duplicate entries and sort dates in ascending order        
                dates=list(sorted(set(habits[name].completed_dates)))
        #define reducer function which is to be passed to reduce tool.
                def reducer(acc,i):
                    """Update streak counter for consecutive dates.
                    Args:
                        acc:dict with two keys.
                            "current:current consecutive day streak length
                            "max":longest streak 
                        i:integer index into the dates list
                    Returns:
                        acc:updated accumulator dict.
                    """
                    # consider date at this index and previous one.
                    current_date=dates[i]
                    previous_date=dates[i-1]
                    #if the difference between two dates are exactly one day
                    if current_date-previous_date==timedelta(days=1):
                    #increase the current streak by one
                        acc["current"]+=1
                    #update the max streak
                        acc["max"]=max(acc["current"],acc["max"])
                    else:
                    #otherwise reset the current streak to 1
                        acc["current"]=1
                    return acc
                # Run the reducer across all inices from 1 to len(dates)-1 
                # with initial current and max streak set to 1
                result=reduce(reducer,range(1,len(dates)),{"current":1,"max":1})

            #check a habit is weekly habit?    
            elif isinstance(habits[name],WeeklyHabit):
                #find week starting for each date in completed dates and create a new list.(monday is the starting of week)
                weeks=[]
                for date in habits[name].completed_dates:
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
        """Method to get longest streak of all habits.
        Returns:
            dictionary:{habit name:longest streak}"""
        # load database
        habits=self.database.retrieve_data()
        return dict(
            map(lambda habit:(habit[0],self.get_longest_streak(habit[0])),habits.items())
        )
if __name__=='__main__':
  
   ha=HabitAnalyzer()
  