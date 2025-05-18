from datetime import date,timedelta
from habittracker.dailyhabit import DailyHabit
from habittracker.weeklyhabit import WeeklyHabit
from habittracker.database import JsonDatabase
from habittracker.constants import Periodicity

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
            periodicity(Enum):frequency of a habit.
        Raises:
            ValueError("Unknown periodicity."):If periodicity is not daily or weekly
            ValueError("Habit already exists"):If tries to create an existing habit."""
        if name==None:
            raise ValueError("Invalid Habit!")
        elif name.strip()=="":
            raise ValueError("Invalid Habit!")
        elif not name.lower() in self.habits:
            if periodicity==Periodicity.DAILY:
                temp_habit=DailyHabit(name,description)
                self.habits.update({name.lower():temp_habit})
            elif periodicity==Periodicity.WEEKLY:
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

    def view_pending_habits_daily(self,date=date.today()):
        """
        Method which returns the list of daily habits to be completed today.
        Returns:
            list of DailyHabit objects.
        """
        pending_habits_daily=[]
        #check a habit is active and a daily habit
        for name in self.habits:
            if self.habits[name].active and isinstance(self.habits[name],DailyHabit):
            # if today is not in the list of completed dates add habit to the pending list.
                if date not in self.habits[name].completed_dates:
                    pending_habits_daily.append(name)
        return pending_habits_daily
    
    def view_pending_habits_weekly(self,date=date.today()):
        """
        Method which returns the list of weekly habits pending to complete this week.
        Returns:
            list of WeeklyHabit objects.
        """
        pending_habits_weekly=[]
        # find current week start and end date
        current_week_start=date-timedelta(days=date.weekday())#today.weekday() is 0 for monday,1 for tuesday and so on
        current_week_end=current_week_start+timedelta(days=6)
        #check whether the habit is active and is a weekly habit.
        for name in self.habits: 
            if self.habits[name].active and isinstance(self.habits[name],WeeklyHabit):
                #if no date in the current week is in the completed dates list add it to the pending habit list.
                if not any(current_week_start<=d<=current_week_end for d in self.habits[name].completed_dates):
                    pending_habits_weekly.append(name)
        return pending_habits_weekly









if __name__=='__main__':
    hm=HabitManager()
    # result=hm.view_pending_habits_daily()
    # print(result)
    # result=hm.view_pending_habits_weekly()
    # print(result)
    hm.create_habit(name=" ",description="morning walk",periodicity="daily")

   
   
    
