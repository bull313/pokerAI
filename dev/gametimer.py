"""
GameTimer:
    Contains time modules and keeps track of the blind interval time
"""

"""
Imports
"""
from datetime import timedelta
from threading import Timer
from time import time

class GameTimer:
    """
    Constants
    """
    SECONDS_PER_MINIUTE = 60
    TIME_STR = "%0.2d:%0.2d"

    """
    Constructor
    """
    def __init__(self, interval_time, callback):
        self._interval_time = interval_time ### Time to set the timer to (in minutes)
        self._callback      = callback      ### Callback function to call when time is up
        self._timer         = None          ### Timer thread object
        self._start_time    = None          ### Time when the timer is activated

    """
    Static Methods
    """
    @staticmethod
    def convert_sec_to_min(value):
        return value / GameTimer.SECONDS_PER_MINIUTE

    @staticmethod
    def convert_min_to_sec(value):
        return value * GameTimer.SECONDS_PER_MINIUTE

    @staticmethod
    def minutes_to_str(time):
        """
        Convert the time in minutes to minutes and seconds
        """
        time_conversion = timedelta(minutes=time)
        minutes, seconds = divmod(time_conversion.seconds, GameTimer.SECONDS_PER_MINIUTE)

        """
        Return the minute and seconds in the time format
        """
        return GameTimer.TIME_STR % (minutes, seconds)

    """
    Public Methods
    """
    def get_interval_time(self):
        return self._interval_time

    def get_remaining_time(self):
        """
        Get the elapsed time (curren time minus start time)
        """
        current_time = time()
        elapsed_time = current_time - self._start_time

        """
        Convert interval time to seconds and find the difference between the initial time and elapsed time
        """
        remaining_time_sec = GameTimer.convert_min_to_sec(self._interval_time) - elapsed_time

        """
        Return the results in minutes
        """
        return GameTimer.convert_sec_to_min(remaining_time_sec)

    def start(self):
        """
        Create a new timer instance to call the callback function at the blind time interval
        Set the thread as a daemon thread so that it will terminate immediately if the game is over
        """
        self._timer = Timer(GameTimer.convert_min_to_sec(self._interval_time), self._callback)
        self._timer.daemon = True
        self._start_time = time()
        self._timer.start()
