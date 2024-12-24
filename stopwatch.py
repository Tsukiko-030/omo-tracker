#--------------------------------------------------------------------------------------------------
# File Headers:
#--------------------------------------------------------------------------------------------------
# Shebang:
#!/usr/bin/env python


# Encoding:
# -*- coding: utf-8 -*-


# Docstring:
"""
Filename: stopwatch.py
Authors: Tsukiko
Date: 23/12/2024
Version: 1.0.0
Description:
    A basic stopwatch class that will primarily be used to track elapsed hold time,
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
#--------------------------------------------------------------------------------------------------




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
class StopwatchError(Exception):
    """This custom exception is used to report errors in the use of the Stopwatch class."""
#----------------------------------------------------------------------------------------------------------------------




#----------------------------------------------------------------------------------------------------------------------
# Stopwatch Class:
#----------------------------------------------------------------------------------------------------------------------
class Stopwatch():
    # Constructor:
    def __init__(self):
        """Initializes the Stopwatch Class."""
        self._start_time = None
        self._elapsed_time = 0
        self._running = False




    # Private Methods:
    def _update_elapsed_time(self):
        """Updates the _elapsed_time variable. To be used for stopping and resuming the stopwatch."""
        if self.is_running():
            self._elapsed_time += int(time.perf_counter()) - self._start_time
            self._start_time = int(time.perf_counter())  # Reset start time for ongoing tracking
    



    # Public Methods:
    def is_running(self):
        """Returns True if the stopwatch is running and returns false if the stopwatch is not running."""
        return self._running
    



    def start_stopwatch(self):
        """Starts the stopwatch."""
        if self.is_running():
            raise StopwatchError("The stopwatch is running. Use .stop_stopwatch() to stop the stopwatch.")
        

        self._start_time = int(time.perf_counter())
        self._running = True
    



    def stop_stopwatch(self):
        """Stops the stopwatch."""
        if not self.is_running():
            raise StopwatchError("The stopwatch is not running. Use .start_stopwatch() to start the stopwatch.")
        

        # Update elapsed time before stopping:
        self._update_elapsed_time()
        self._running = False




    def pause_stopwatch(self):
        """Pauses the stopwatch without resetting elapsed time."""
        if not self.is_running():
            raise StopwatchError("Cannot pause a stopwatch that isn't running.")
        
        
        self._update_elapsed_time()
        self._running = False




    def resume_stopwatch(self):
        """Resumes the stopwatch after pausing."""
        if self.is_running():
            raise StopwatchError("Cannot resume a running stopwatch.")
        
        
        self._start_time = int(time.perf_counter())
        self._running = True




    def reset_stopwatch(self):
        """Resets the stopwatch to 00:00:00."""
        if self.is_running():
            self.stop_stopwatch()
        

        self._start_time = None
        self._elapsed_time = 0




    def get_elapsed_time(self):
        """Returns the total time since the stopwatch was started."""
        if self.is_running():
            # Calculate elapsed time without modifying the stored value:
            return self._elapsed_time + (int(time.perf_counter()) - self._start_time)
       
       
        return self._elapsed_time





    def output_elapsed_time(self):
        """Returns the elapsed time since the stopwatch was started in the string format hh:mm:ss."""
        # Get elapsed time:
        elapsed = self.get_elapsed_time()
        

        # Convert seconds into hours, minutes, and seconds:
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        

        # Format the time as hh:mm:ss:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
#----------------------------------------------------------------------------------------------------------------------



#--------------------------------------------------------------------------------------------------
# Ideas for Improvements:
#--------------------------------------------------------------------------------------------------
"""
* Allow the stopwatch to track starts and stops and continute running.

* Allow the stopwatch to output, elapsed days, months and years.
  This project should not require such functionality so it has not been implemented here.

* Allow the stopwatch to store the start time in a persistent file on the computer's storage drive,
  and retrieve it. This could allow the stopwatch to continue tracking time even after the application
  is closed or after a power interruption.
  Taking this a step further, storing the file on the cloud could allow the stopwatch
  to persist across multiple internet connected devices or after complete system reset.
"""
#--------------------------------------------------------------------------------------------------




#--------------------------------------------------------------------------------------------------
# References:
#--------------------------------------------------------------------------------------------------
"""
* https://realpython.com/python-timer/#a-python-timer-class
"""
#--------------------------------------------------------------------------------------------------
