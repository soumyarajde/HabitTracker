from datetime import datetime,date,time,timedelta
import logging
logger = logging.getLogger(__name__)

class Habit:
    """
    Represents super class of all habit classes.
    Attributes:
        name(string):The name of the habit.
        description(string):A short desription about the habit.
        creation_date(date):The date on which a habit is created.
        completed_dates([dates]):The list of check off dates.
        active(bool):Shows status of a habit active/inactive.True for active and False for inactive
    """
    def __init__(self,name=None,description=None,creation_date=datetime.today().date(),active=True):
        """
        Initializes a new object of the Habit class.
        Args:
        name(string):The name of habit.
        description(string):A short description about habit.
        creation_date(date):Date on which a habit is created.
        active(bool):status of a habit.
        """
        self.name=name
        self.description=description
        self.creation_date=creation_date
        self.completed_dates=[]
        self.active=active
        # logger.debug(
        #     f"Initializing Habit with name: {self.name},description: {self.description},creation_date: {self.creation_date},active: {active}")

    def serialize(self):
        """
        Convert Habit class object into json serializable dictionary.
        Returns:
            dictionary:habit class object converted into dictionary of string.
        """
        _habitdict={}
        _habitdict['name']=self.name
        _habitdict['description']=self.description
        _habitdict['completed_dates']=[date.isoformat() for date in self.completed_dates] 
        _habitdict['active']=self.active
        _habitdict['creation_date']=self.creation_date.isoformat()
        _habitdict['class_name']=self.__class__.__name__
        return _habitdict
    
    @classmethod
    def deserialize(cls,_dict):
        """
        Reconstruct Habit class object from json dictionary.
        Arg:
             _dict(dictionary):dictionary of habit data retrived from json file
        Returns:
            habit class object.
        """
        _creation_date=datetime.fromisoformat(_dict.get('creation_date')).date()
        _habit=cls(_dict.get('name','NoName'),_dict.get('description','NoDesc'),_creation_date,_dict.get('active'))
        _habit.completed_dates=[datetime.fromisoformat(date_str).date() for date_str in _dict.get('completed_dates')]
       
        return _habit
    
    def __repr__(self):
        """Returns the string representation of an object."""
        return f"{self.__class__.__name__}(Name:{self.name}, Description:{self.description}, Creation_date:{self.creation_date}, Completed_dates:{self.completed_dates}, Active:{self.active})" #TODO also print the name of the class at the begining of the f string for easy debugging
    
    def check_off(self,date=datetime.today().date()):
        """
        Add the check off date of a habit to the completed_dates list.
        Args:
            date(date).Date on which habit is done.
        Raises:
            ValueError if the habit is inactive.
        """
        if self.active:
            self.completed_dates.append(date)
            logger.debug(f"checking of habit: {self.name} on date:{date}")
        else:
            logging.error(f"Habit:{self.name} is inactive.")
            raise ValueError("Inactive Habit!")

    def deactivate_habit(self):
        """Deactivate a habit by changing the value of self.active to False."""
        self.active=False
        logger.debug(f"Habit:{self.name} deactivated.")

    def activate_habit(self):
        """Activate a habit by setting self.active to True"""
        self.active=True
        logger.debug(f"Habit:{self.name} activated.")

    def calculate_streak(self):
        """Method to calculate streak."""
        raise NotImplementedError



       

    
    
    
