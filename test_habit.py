import unittest
from datetime import datetime,date,timedelta
from habit import Habit

class TestHabit(unittest.TestCase):

    def test_initialization_with_default_date(self):
        habit=Habit(name="Drinking",description="2 ltrs of water")
        self.assertEqual(habit.name,"Drinking")
        self.assertEqual(habit.description,"2 ltrs of water")
        self.assertEqual(habit.creation_date,datetime.today().date())
        self.assertEqual(habit.completed_dates,[])
        self.assertTrue(habit.active)

    def setUp(self):
        """Creates a habit instance which can be used for further testing"""
        self.custom_date=date(2025,5,4)
        self.habit=Habit(name="Drinking",description="2 ltrs of water",creation_date=self.custom_date)

    def test_initialization_with_custom_date(self):
        self.assertEqual(self.habit.name,"Drinking")
        self.assertEqual(self.habit.description,"2 ltrs of water")
        self.assertEqual(self.habit.creation_date,self.custom_date)
        self.assertEqual(self.habit.completed_dates,[])
        self.assertTrue(self.habit.active)
    
    def test_repr(self):
        result=repr(self.habit)
        self.assertIn("Name:Drinking",result)
        self.assertIn("Description:2 ltrs of water",result)
        self.assertIn("Creation_date:2025-05-04",result)
        self.assertIn("Completed_dates:[]",result)
        self.assertIn("Active:True",result)
        
    def test_check_off_default_date(self):
        self.habit.check_off()
        self.assertIn(datetime.today().date(),self.habit.completed_dates)

    def test_check_off_custom_date(self):
        self.habit.check_off(date=date(2025,5,6))
        self.assertIn(date(2025,5,6),self.habit.completed_dates)

    def test_deactivate_habit(self):
        self.habit.deactivate_habit()
        self.assertFalse(self.habit.active)

    def test_activate_habit(self):
        self.habit.deactivate_habit()
        self.habit.activate_habit()
        self.assertTrue(self.habit.active)


    
if __name__=="__main__":
    unittest.main()