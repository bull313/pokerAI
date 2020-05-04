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
    def __init__(self, interval_time, callback, init_start_time=0):
        self._callback              = callback          ### Callback function to call when time is up
        self._current_interval_time = 0                 ### TIme value that the timer is currently set to
        self._init_start_time       = init_start_time   ### Time value to use first before using the normal interval time
        self._interval_time         = interval_time     ### Time to set the timer to (in minutes)
        self._start_time            = 0                 ### Time when the timer is activated
        self._timer                 = None              ### Timer thread object

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
    Private Methods
    """
    def _modified_callback(self):
        """
        Special callback function that invoke the callback function as normal
        and also removes the initial start time to begin setting the timer at the norrmal interval
        """
        self._callback()
        self._init_start_time = 0

    """
    Public Methods
    """
    def get_interval_time(self):
        """
        Get the timer's current interval time (initial start time if it is set, otherwise the normal interval time)
        """
        interval_time = self._interval_time

        if self._init_start_time:
            interval_time = self._init_start_time
        
        return interval_time

    def get_remaining_time(self):
        """
        Get the time left on the timer
        """
        remaining_time = 0

        """
        Return a value of 0 if the timer is not set
        """
        if self._start_time is not None:
            """
            Get the elapsed time (current time minus start time)
            and the interval time
            """
            current_time    = time()
            elapsed_time    = current_time - self._start_time
            interval_time   = self._current_interval_time

            """
            Convert the interval time to seconds and find the difference between the initial time and elapsed time
            """
            remaining_time_sec = GameTimer.convert_min_to_sec(interval_time) - elapsed_time

            """
            Set the lower limit of the remaining time to 0 (cannot have negative remaining time)
            """
            remaining_time_sec = max(remaining_time_sec, 0)

            """
            Convert the remaining seconds into minutes
            """
            remaining_time = GameTimer.convert_sec_to_min(remaining_time_sec)

        """
        Return the result
        """
        return remaining_time

    def start(self):
        """
        Get the current interval time and convert it to seconds for the timer object
        """
        self._current_interval_time = self.get_interval_time()
        interval_time_seconds       = GameTimer.convert_min_to_sec(self._current_interval_time)
        callback                    = self._callback

        """
        Use the modified callback to remove the initial start time if it is set
        Initial start time may only be used once
        """
        if self._init_start_time:
            callback = self._modified_callback

        """
        Create a new timer instance to call the callback function at the blind time interval
        Set the thread as a daemon thread so that it will terminate immediately if the game is over
        """
        self._timer         = Timer(GameTimer.convert_min_to_sec(self._current_interval_time), callback)
        self._timer.daemon  = True
        self._start_time    = time()
        self._timer.start()
