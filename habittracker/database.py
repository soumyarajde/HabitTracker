import json
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
        # access each habit in habits dictionary at a time habit_name(key) habit(value)
        for habit_name,habit in habits.items():
        # serialize each habit and add it to a dictionary.Here key is habit name in lowercase and value serialized habit object
            _data.update({habit_name:habit.serialize()})
        # save data into database file
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
        #load the data in json file and assign to a variable 'data'.It is a dictionary.
        try:
            with open(self.filename) as f:
                data=json.load(f)
         # return null set when the file is empty or does not exist.       
        except json.decoder.JSONDecodeError as e:
            print(f"Error loading json {e}")
            return {}
        except FileNotFoundError as e:
            print(f"Error loading json {e}")
            return {} 
        # consider each item in the data dict.Convert it back to habit object by deserialization.
        for habit_name,habit in data.items():
            # if the class name of the item belongs to 'DailyHabit' call deserialization for that class.
            if habit['class_name']=='DailyHabit':
                habits[habit_name]=DailyHabit.deserialize(habit)
            # if the class name of the item belongs to 'WeeklyHabit' call deserialization for WeeklyHabit.
            elif habit['class_name']=='WeeklyHabit':
                habits[habit_name]=WeeklyHabit.deserialize(habit)
        # return the dictionary of reconstructed habit objects
        return habits
    
    
        
        