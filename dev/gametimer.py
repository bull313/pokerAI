"""
GameTimer:
    Contains time modules and keeps track of the blind interval time
"""

"""
Imports
"""
from threading import Timer
from time import time

class GameTimer:
    """
    Constants
    """
    SECONDS_PER_MINIUTE = 60

    """
    Constructor
    """
    def __init__(self, interval_time, callback):
        self._interval_time = interval_time   ### Time to set the timer to (in minutes)
        self._callback = callback             ### Callback function to call when time is up
        self._timer = None                    ### Timer thread object
        self._start_time = None               ### Time when the timer is activated


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
        Get the time in the format of X minutes and Y seconds
        """
        minutes = int(time)
        seconds = GameTimer.convert_min_to_sec(time - minutes)

        time_str = ""
        minutes_str = ""
        seconds_str = ""

        """
        Format the minutes string or do not include it if there are 0 minutes
        """
        if minutes == 1:
            minutes_str = "%d minute"
        elif minutes > 0:
            minutes_str = "%d minutes"

        """
        Format the seconds string or do not include it if there are a whole number of minutes more than 0
        """
        if seconds == 1:
            seconds_str = "%d second"
        elif seconds > 0 or minutes == 0:
            seconds_str = "%d seconds"

        """
        Combine the minutes and seconds strings together if they both exist
        """
        if len(minutes_str) > 0:
            time_str += ( minutes_str % minutes )

            if len(seconds_str) > 0:
                time_str += " and %s" % ( seconds_str % seconds )

        elif len(seconds_str):
            time_str += seconds_str % seconds

        return time_str

    """
    Public Methods
    """
    def get_interval_time(self):
        return self._interval_time

    def get_remaining_time(self):
        """
        Get the difference between the current time and the timer start time
        And subtract it from the initial time to get the remaining time
        """
        current_time = time()
        time_difference = current_time - self._start_time
        interval_time_secs = GameTimer.convert_min_to_sec(self._interval_time)
        remaining_time_sec = interval_time_secs - time_difference
        return GameTimer.convert_sec_to_min(remaining_time_sec)

    def start(self):
        """
        Create a new timer instance to call the callback function at the blind time interval
        Set the thread as a daemon thread so that it will terminate immediately if the game is over
        """
        interval_time_secs = GameTimer.convert_min_to_sec(self._interval_time)

        self._timer = Timer(interval_time_secs, self._callback)
        self._timer.daemon = True
        self._start_time = time()
        self._timer.start()
