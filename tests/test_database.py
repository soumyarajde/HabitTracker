import pytest
import json
from habittracker.habit import Habit
from habittracker.dailyhabit import DailyHabit
from habittracker.weeklyhabit import WeeklyHabit
from habittracker.database import HabitDataStorage, JsonDatabase


@pytest.fixture
def sample_habits():
    daily_habit = DailyHabit("Reading", "30 mins")
    weekly_habit = WeeklyHabit("Cleaning", "house")
    return {"reading": daily_habit, "cleaning": weekly_habit}


@pytest.fixture
def json_db(tmp_path):
    filename = tmp_path / "test.json"
    return JsonDatabase(filename)


def test_save_data(json_db, sample_habits):
    json_db.save_data(sample_habits)

    with open(json_db.filename, "r") as f:
        data = json.load(f)
        assert data["reading"]["name"] == "Reading"
        assert data["reading"]["class_name"] == "DailyHabit"
        assert data["cleaning"]["name"] == "Cleaning"
        assert data["cleaning"]["class_name"] == "WeeklyHabit"


def test_retrieve_data(json_db, sample_habits):
    # first save data
    json_db.save_data(sample_habits)
    # retrieve habit from json file
    habits = json_db.retrieve_data()
    isinstance(habits["reading"], DailyHabit)
    isinstance(habits["cleaning"], WeeklyHabit)


def test_retrieve_data_invalid_file(tmp_path):
    # create an invalid file.
    filename = tmp_path / "dummy_file.json"
    filename.write_text("This is not json data.")
    db = JsonDatabase(str(filename))  # load data using habit database.
    habits = db.retrieve_data()
    assert habits == {}  # return null set on failure


def test_retrieve_data_filenotfound(tmp_path):
    # create an invalid file.
    filename = tmp_path / "jj.json"
    db = JsonDatabase(str(filename))  # load data using habit database.
    habits = db.retrieve_data()
    assert habits == {}  # return null set on failure
