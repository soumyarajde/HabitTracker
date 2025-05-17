import json
from habittracker.habit import Habit
from habittracker.dailyhabit import DailyHabit
from habittracker.weeklyhabit import WeeklyHabit

class HabitDataStorage:
    """
    Super class of all file based storage classes.
    Attribute:
        filename(string) name of the file to which data is to be saved.
    """
    def __init__(self,filename):
        """
        Initializes a new instance of HabitDataStorage.
        Arg:
            filename(string):name of database."""
        
        self.filename=filename

    def save_data(self):
        """Method to save data to the database."""
        raise NotImplementedError

    def retrieve_data(self):
        """Method to retrieve data from the database."""
        raise NotImplementedError

class JsonDatabase(HabitDataStorage):
    """Represents a subclass of class HabitDataStorage which stores data in json file."""
    
    def __init__(self,filename):
        super().__init__(filename)

    def save_data(self,habits):
        """
        Save habit data to the json file.
        Args:
            habits(dictionary):dictionary of habit class objects.
        """
        _data={}
        for habit_name,habit in habits.items():
            _data.update({habit_name:habit.serialize()})
        try:
            with open(self.filename,"w") as f:
                json.dump(_data,f)
        except FileNotFoundError:
            print(f"Wrong file name specified : {self.filename}")

    
    def retrieve_data(self):
        """
        Reload the data stored in a json file.
        Returns:
            dictionary:dictionary of Habit class objects.
        """
        habits={}
        try:
            with open(self.filename) as f:
                data=json.load(f)
         # return null set when the file is empty or does not exist.       
        except json.decoder.JSONDecodeError as e:
            print(f"Error loading jason {e}")
            return {}
        except FileNotFoundError as e:
            print(f"Error loading jason {e}")
            return {} 
        for habit_name,habit in data.items():
            if habit['class_name']=='DailyHabit':
                habits[habit_name]=DailyHabit.deserialize(habit)
            elif habit['class_name']=='WeeklyHabit':
                habits[habit_name]=WeeklyHabit.deserialize(habit)

        return habits
        
        

        
    

if __name__ == "__main__":
    db = JsonDatabase("tf.json")
    db.retrieve_data()