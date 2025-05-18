from enum import Enum
class Periodicity(str,Enum):
    DAILY="daily"
    WEEKLY="weekly"

class AnalyzerOptions(str,Enum):
    DEFAULT_OPTION="Select an analysis"
    CURRENT_STREAK="Show current streak"
    LONGEST_STREAK="Show longest streak"
    DAILY_HABITS="Show daily habits"
    WEEKLY_HABITS="Show weekly habits"
    LONGEST_STREAK_ALL="Show longest streak (All habits)"
    CURRENTLY_TRACKED_HABITS="Show currently tracked habits"