from datetime import date,timedelta
from habittracker.habit import Habit
from habittracker.dailyhabit import DailyHabit
from habittracker.weeklyhabit import WeeklyHabit
from habittracker.database import HabitDataStorage, JsonDatabase

class HabitManager:
    """Manages all habits.
    Attributes:habits{Habit}:a dictionary of Habit class objects.
                databse:HabitDataStorage:an instance of HabitDataStorage used for databse operations."""
    def __init__(self,filepath='db.json'):
        """Initialize HabitManager object.
        Args:
            filepath(string):database filepath.
            """
        self.habits={}
        self.database=JsonDatabase(str(filepath))
        self.habits=self.database.retrieve_data()

    def create_habit(self,name=None,description=None,periodicity=None):
        """
        Creates a habit and add it to a dictionary and save it in the database.
        Habit name in lowercase is used as the key for each habit.
        Args:
            name(string):name of a habit
            description(string):description of a habit.
            periodicity(string):frequency of a habit.
        Raises:
            ValueError("Unknown periodicity."):If periodicity is not daily or weekly
            ValueError("Habit already exists"):If tries to create an existing habit."""
        if not name.lower() in self.habits:
            if periodicity.lower()=='daily':# TODO use enum for periodicity
                temp_habit=DailyHabit(name,description)
                self.habits.update({name.lower():temp_habit})
            elif periodicity.lower()=='weekly':
                temp_habit=WeeklyHabit(name,description)
                self.habits.update({name.lower():temp_habit})
            else:
                raise ValueError("Unknown periodicity.")
        else:   
            raise ValueError("Habit already exists")
            
        self.database.save_data(self.habits)

    def delete_habit(self,name=None):
        """
        Deletes a given habit and update database.
        Args:
            name(string):name of the habit.
        Raises:
            ValueError("Habit does not exist."):If tries to delete a habit which is not in the database.
        """
        if name.lower()in self.habits:
            self.habits.pop(name.lower())
        else:
            raise ValueError("Habit does not exist.")
        self.database.save_data(self.habits)

    def deactivate_habit(self,name=None):
        """
        Deactivates a habit and update database.
        Arg:
            name(str):name of the habit
        Raises:
            ValueError("Habit does not exist."):If tries to deactivate a habit which is not in the database.
        """
        if name.lower() in self.habits:
            self.habits[name.lower()].deactivate_habit()
        else:
            raise ValueError("Habit does not exist.")
        self.database.save_data(self.habits)

    def activate_habit(self,name=None):
        """
        Activates an inactive habit and update database.
        Arg:
            name(str):name of the habit
        Raises:
            ValueError("Habit does not exist."):If tries to activate a habit which is not in the database.
        """
        if name.lower() in self.habits:
            self.habits[name.lower()].activate_habit()
        else:
            raise ValueError("Habit does not exist.")

        self.database.save_data(self.habits)

    def check_off(self,name=None,date=date.today()):
        """
        Marks a habit as completed.Adds date to the completed dates list and update database.
        Args:
            date(date):date on which habit is done.
        Raises:
            ValueError("Habit does not exist."):If tries to check off a habit which is not in the database.
        """
        if name.lower() in self.habits:
            self.habits[name.lower()].check_off(date)
        else:
            raise ValueError("Habit does not exist.")
        self.database.save_data(self.habits)

    def view_pending_habits_daily(self,date=date.today()):#Todo except inactive habit
        
        pending_habits_daily=[]
        for name,habit in self.habits.items():
            if isinstance(self.habits[name],DailyHabit):
                if date not in self.habits[name].completed_dates:
                    pending_habits_daily.append(name)
        return pending_habits_daily
    
    def view_pending_habits_weekly(self,date=date.today()):
        pending_habits_weekly=[]
        current_week_start=date-timedelta(days=date.weekday())#today.weekday() is 0 for monday,1 for tuesday and so on
        current_week_end=current_week_start+timedelta(days=6)
        for name,habit in self.habits.items():
            if isinstance(self.habits[name],WeeklyHabit):
                if not any(current_week_start<=d<=current_week_end for d in self.habits[name].completed_dates):
                    pending_habits_weekly.append(name)
        return pending_habits_weekly









if __name__=='__main__':
    hm=HabitManager()
    result=hm.view_pending_habits_daily()
    print(result)
    result=hm.view_pending_habits_weekly()
    print(result)
   

    
   
    
