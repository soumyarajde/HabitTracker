from enum import Enum
class Periodicity(str,Enum):
    DAILY="daily"
    WEEKLY="weekly"

class AnalyzerOptions(str,Enum):
    DEFAULT_OPTION="Select an analysis"
    CURRENT_STREAK="Current streak"
    LONGEST_STREAK="Longest streak"
    DAILY_HABITS="Daily habits"
    WEEKLY_HABITS="Weekly habits"
    LONGEST_STREAK_ALL="Longest Streak All"
    CURRENTLY_TRACKED_HABITS="Currently Tracked habits"