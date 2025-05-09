import unittest
from datetime import date,datetime,timedelta
from habit import Habit
from weeklyhabit import WeeklyHabit

class TestWeeklyHabit(unittest.TestCase):
    
    def setUp(self):
        self.daily_habit=WeeklyHabit("Shopping","for the week")
        self.check_off_date=date(2025,5,7)
        self.daily_habit.check_off(self.check_off_date)

    def test_serialize_weekly_habit(self):
        result=self.daily_habit.serialize()
        self.assertEqual(result['name'],"Shopping")
        self.assertEqual(result['description'],"for the week")
        self.assertEqual(result['completed_dates'],["2025-05-07"])
        self.assertEqual(result['creation_date'],self.daily_habit.creation_date.isoformat())
        self.assertEqual(result['active'],True)
        self.assertEqual(result['class_name'],'WeeklyHabit')

    def test_deserialize_weekly_habit(self):
        data={
            'name':'Shopping',
            'description':'for the week',
            'completed_dates':['2025-05-04','2025-05-12'],
            'creation_date':'2025-05-03',
            'active':'True',
            'class_name':'WeeklyHabit',
        }
        weekly_habit=WeeklyHabit.deserialize(data)
        self.assertEqual(weekly_habit.name,"Shopping")
        self.assertEqual(weekly_habit.description,"for the week")
        self.assertEqual(weekly_habit.creation_date,date(2025,5,3))
        self.assertEqual(weekly_habit.completed_dates,[date(2025,5,4),date(2025,5,12)])
        self.assertEqual(weekly_habit.active,True) 

    def test_calculate_streak_empty(self):
        pass
    def test_calculate_streak_includes_current_week(self):
        pass
    def test_calculate_streak_excludes_excludes_current_week(self):
        pass
    def test_calculate_streak_noncontinuous_weeks(self):
        pass
    
if __name__=='__main__':
    unittest.main()
                         