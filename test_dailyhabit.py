import unittest
from datetime import date,datetime,timedelta
from habit import Habit
from dailyhabit import DailyHabit

class TestDailyHabit(unittest.TestCase):
    
    def setUp(self):
        self.daily_habit=DailyHabit("Sleeping","8 hours")
        self.check_off_date=date(2025,5,7)
        self.daily_habit.check_off(self.check_off_date)


    def test_serialize_daily_habit(self):
        result=self.daily_habit.serialize()
        self.assertEqual(result['name'],"Sleeping")
        self.assertEqual(result['description'],"8 hours")
        self.assertEqual(result['completed_dates'],["2025-05-07"])
        self.assertEqual(result['creation_date'],self.daily_habit.creation_date.isoformat())
        self.assertEqual(result['active'],True)
        self.assertEqual(result['class_name'],'DailyHabit')

    def test_deserialize_daily_habit(self):
        data={
            'name':'Sleeping',
            'description':'8 hours',
            'completed_dates':['2025-05-04','2025-05-05'],
            'creation_date':'2025-05-03',
            'active':'True',
            'class_name':'DailyHabit',
        }
        daily_habit=DailyHabit.deserialize(data)
        self.assertEqual(daily_habit.name,"Sleeping")
        self.assertEqual(daily_habit.description,"8 hours")
        self.assertEqual(daily_habit.creation_date,date(2025,5,3))
        self.assertEqual(daily_habit.completed_dates,[date(2025,5,4),date(2025,5,5)])
        self.assertEqual(daily_habit.active,True)

    def test_calculate_streak_empty(self):
        pass
    def test_calculate_streak_includes_today(self):
        pass
    def test_calculate_streak_excludes_today(self):
        pass
    def test_calculate_streak_single_day_today(self):
        pass
    def test_calculate_streak_single_day_yesterday(self):
        pass
    def test_calculate_streak_noncontinuous_days(self):
        pass
    


if __name__=='__main__':
    unittest.main()
                         