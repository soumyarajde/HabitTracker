from datetime import date
from habit import Habit
from dailyhabit import DailyHabit
from weeklyhabit import WeeklyHabit
from database import HabitDataStorage, JsonDatabase

class HabitManager:
    """Manages all habits.
    Attributes:habits{Habit}:a dictionary of Habit class objects.
                databse:HabitDataStorage:an instance of HabitDataStorage used for databse operations."""
    def __init__(self):
        """Initialize HabitManager object."""
        self.habits={}
        self.database=JsonDatabase('db.json')
        self.habits=self.database.retrieve_data()

    def create_habit(self,name=None,description=None,periodicity=None):
        if not name.lower() in self.habits:
            if periodicity.lower()=='daily':
                temp_habit=DailyHabit(name,description)
                self.habits.update({name.lower():temp_habit})
            elif periodicity.lower()=='weekly':
                temp_habit=WeeklyHabit(name,description)
                self.habits.update({name.lower():temp_habit})
            else:
                print("Unknown periodicity.")
            
        else:   
            print("Habit already exists")
        self.database.save_data(self.habits)

    def delete_habit(self,name):
        """Deletes a given habit."""
        if name.lower()in self.habits:
            self.habits.pop(name.lower())
            print(f"{name} deleted successfully")
        else:
            print(f"Habit {name} does not exist.")
        self.database.save_data(self.habits)

    def deactivate_habit(self,name):
        """Deactivates a habit.Arg:name(str):name of the habit"""
        if name.lower() in self.habits:
            self.habits[name.lower()].deactivate_habit()
        self.database.save_data(self.habits)

    def activate_habit(self,name):
        """Activates a habit.Arg:name(str):name of the habit"""
        if name.lower() in self.habits:
            self.habits[name.lower()].activate_habit()
        self.database.save_data(self.habits)

    def check_off(self,name,date):
        """Marks a habit as completed and add date to the completed dates list."""
        if name.lower() in self.habits:
            self.habits[name.lower()].check_off(date)
        self.database.save_data(self.habits)

    def view_habit(self):
        """Show all habits."""
        habits=self.habits.keys()
        print(habits)


            
    





if __name__=='__main__':
    hm=HabitManager()
   # hm.create_habit("cleaning","cleaning house","weekly") 
    #hm.check_off("shopping",date=date(2025,5,6))
    hm.view_habit()

    
   
    
