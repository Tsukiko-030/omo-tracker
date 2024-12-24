#----------------------------
# File Headers:
#----------------------------
# Shebang:
#!/usr/bin/env python


# Encoding:
# -*- coding: utf-8 -*-


# Docstring:
"""
Filename: timer.py
Authors: Tsukiko
Date: 23/12/2024
Version: 1.0.0
Description:
    A basic timer class that will primarily be used to track remaining hold time,
    consequently it is only designed to track time for hours, not days or beyond
    and it's precision is limited to seconds.
    

License: MIT License
Contact: tsukiko1701@gmail.com
Dependencies: time
"""


# Dunders:
__author__ = "Tsukiko"
__copyright__ = "Copyright (c) 2025 Tsukiko-030"
__credits__ = ["Tsukiko"]
__license__ = "The MIT License (MIT)"
__version__ = "1.0.0"
__maintainer__ = "Tsukiko"
__email__ = "tsukiko1701@gmail.com"
__status__ = "Production"
#----------------------------




#----------------------------
# Import Statements:
#----------------------------
import time
#----------------------------




#--------------------------------------
# Exterior Functions:
#--------------------------------------
#--------------------------------------




#----------------------------------------------------------------------------------------------------------------------
# StopwatchError Class:
#----------------------------------------------------------------------------------------------------------------------
class TimerError(Exception):
    """This custom exception is used to report errors in the use of the Timer class."""
#----------------------------------------------------------------------------------------------------------------------




#----------------------------------------------------------------------------------------------------------------------
# Template Class:
#----------------------------------------------------------------------------------------------------------------------
class Timer():
    # Constructor:
    def __init__(self, duration):
        """
        Initializes the Countdown class.
        :param duration: Countdown duration in seconds.
        """
        if duration <= 0:
            raise ValueError("Duration must be greater than zero.")
        
        self._initial_duration = int(duration)
        self._remaining_time = int(duration)
        self._start_time = None
        self._running = False




    # Private Methods:
    def _update_remaining_time(self):
        """Updates the remaining time based on elapsed time since start."""
        if self.is_running():
            elapsed = int(time.perf_counter()) - self._start_time
            self._remaining_time -= int(elapsed)
            self._start_time = int(time.perf_counter())
            # Prevent negative remaining time:
            if self._remaining_time <= 0:
                self._remaining_time = 0
                self._running = False




     # Public Methods:
    def is_running(self):
        """Returns True if the countdown is running."""
        return self._running

    def start_countdown(self):
        """Starts the countdown."""
        if self.is_running():
            raise TimerError("The countdown is already running.")
        if self._remaining_time <= 0:
            raise TimerError("The countdown has already finished. Reset to start again.")
        
        self._start_time = int(time.perf_counter())
        self._running = True

    def pause_countdown(self):
        """Pauses the countdown."""
        if not self.is_running():
            raise TimerError("Cannot pause a countdown that isn't running.")
        self._update_remaining_time()
        self._running = False

    def resume_countdown(self):
        """Resumes the countdown."""
        if self.is_running():
            raise TimerError("Cannot resume a running countdown.")
        if self._remaining_time <= 0:
            raise TimerError("Cannot resume a finished countdown. Reset to start again.")
        
        self._start_time = int(time.perf_counter())
        self._running = True

    def reset_countdown(self):
        """Resets the countdown to its initial duration."""
        self._remaining_time = self._initial_duration
        self._start_time = None
        self._running = False

    def get_remaining_time(self):
        """Returns the remaining time in seconds."""
        if self.is_running():
            self._update_remaining_time()
        return self._remaining_time

    def output_remaining_time(self):
        """Returns the remaining time as a formatted string (hh:mm:ss)."""
        remaining = self.get_remaining_time()
        hours = remaining // 3600
        minutes = (remaining % 3600) // 60
        seconds = remaining % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
#----------------------------------------------------------------------------------------------------------------------




#--------------------------------------------------------------------------------------------------
# Ideas for Improvements:
#--------------------------------------------------------------------------------------------------
"""
* 
"""
#--------------------------------------------------------------------------------------------------




#--------------------------------------------------------------------------------------------------
# References:
#--------------------------------------------------------------------------------------------------
"""
* 
"""
#--------------------------------------------------------------------------------------------------
