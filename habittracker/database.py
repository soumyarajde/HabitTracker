import json
from habittracker.habit import Habit
from habittracker.dailyhabit import DailyHabit
from habittracker.weeklyhabit import WeeklyHabit

class HabitDataStorage:
    """Manages habit data saving and loading.
    Attribute:filename(string) name of the file to which data is to be saved."""
    def __init__(self,filename):
        """Initializes a new instance of HabitDataStorage.
        Arg:filename(string)"""
        
        self.filename=filename

    def save_data(self):
        raise NotImplementedError

    def retrieve_data(self):
        raise NotImplementedError

class JsonDatabase(HabitDataStorage):
    """Represents a subclass of class HabitDataStorage which stores data in json file."""
    
    def __init__(self,filename):
        super().__init__(filename)

    def save_data(self,habits):
        """Save habit data to the json file."""
        _data={}
        for habit_name,habit in habits.items():
            _data.update({habit_name:habit.serialize()})
        with open(self.filename,"w") as f:
            json.dump(_data,f)

    
    def retrieve_data(self):
        """Reload the data stored in json file"""
        habits={}
        with open(self.filename) as f:
            try:
                data=json.load(f)
            except json.decoder.JSONDecodeError as e:
                print(f"Error loading jason {e}")
                return {}
            for habit_name,habit in data.items():
                if habit['class_name']=='DailyHabit':
                    habits[habit_name]=DailyHabit.deserialize(habit)
                elif habit['class_name']=='WeeklyHabit':
                    habits[habit_name]=WeeklyHabit.deserialize(habit)

        return habits
        
        

        
    

