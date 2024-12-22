#--------------------------------------------------------------------------------------------------
#File Headers:
#--------------------------------------------------------------------------------------------------
#Shebang:
#!/usr/bin/env python


#Encoding:
# -*- coding: utf-8 -*-


#Docstring:
"""
Filename: omo.py
Author: PERVasive
Date: 05/09/2018
Version: 1.0
Description:
    An exponential decay model for bladder filling. This is based on observing that since
    the volume of bodily fluids must remain constant, the rate at which the kidneys produce
    urine should be proportional to the amount of excess water in the body.
    
    The exponential decay model has been calibrated for a half-life equivalent to a urine
    production rate of 750 mL/hr.

License: The MIT License (MIT)
Contact: https://github.com/perv-asive
Dependencies: collections, statistics, random, math
"""


#Dunders:
__author__ = "PERVasive"
__copyright__ = "Copyright (c) 2018 perv-asive"
__credits__ = ["PERVasive"]
__license__ = "The MIT License (MIT)"
__version__ = "1.0.0"
__maintainer__ = "PERVasive"
__contact__ = "https://github.com/perv-asive"
__status__ = "Production"
#--------------------------------------------------------------------------------------------------




#----------------------------
#Import Statements:
#----------------------------
import collections
import statistics
import random
from math import log2
#----------------------------



#------------------------------------------------------------------------------------------------------------
#Exterior Variables:
#------------------------------------------------------------------------------------------------------------
# h is the half life of water consumed before it gets absorbed, in minutes
h = float(45)
# default_capacity is 500 mL, the accepted figure for human bladder size
# this is known to be low for Omo players, but it is better to err low
default_capacity = 500
# after asking permission, we cannot ask again until bladder has increased
# by capacity/fullness_quantum. This method is balanced between large and small bladders.
fullness_quantum = 5.0
#------------------------------------------------------------------------------------------------------------




#------------------------------------------------------------------------------------------------------------
#Permission Class:
#------------------------------------------------------------------------------------------------------------
class Permission(collections.namedtuple('Permission', ['time', 'permission'])):
    pass
#------------------------------------------------------------------------------------------------------------




#------------------------------------------------------------------------------------------------------------
#Drink Class:
#------------------------------------------------------------------------------------------------------------
class Drink(collections.namedtuple('Drink', ['time', 'amount'])):
    def unabsorbed(self, t):
        if t > self.time:
            return (2 ** ((self.time - t) / h)) * self.amount
        else:
            return self.amount
#------------------------------------------------------------------------------------------------------------




#------------------------------------------------------------------------------------------------------------
#Release Class:
#------------------------------------------------------------------------------------------------------------
class Release(collections.namedtuple('Release', ['time', 'amount', 'permission'])):
    pass
#------------------------------------------------------------------------------------------------------------




#------------------------------------------------------------------------------------------------------------
#Drinker Class:
#------------------------------------------------------------------------------------------------------------
class Drinker(object):
    def __init__(self):
        random.seed()
        self._history = []
        self.old_accidents = []
        self._permission = Permission(None, False)

    @property
    def history(self):
        return self._history[:]

    @history.setter
    def history(self, value):
        self._history = sorted(value, key=lambda el: el.time)

    @property
    def drinks(self):
        return [el for el in self._history if isinstance(el, Drink)]

    @property
    def releases(self):
        return [el for el in self._history if isinstance(el, Release)]

    @property
    def accidents(self):
        return [el for el in self._history if isinstance(el, Release) and not el.permission]

    @property
    def capacity(self):
        all_accidents = [el.amount for el in self.accidents] + self.old_accidents
        if all_accidents:
            new_cap = statistics.mean(all_accidents)
            return new_cap if new_cap else default_capacity
        else:
            return default_capacity

    @property
    def eta(self):
        excess_latent_water = \
            sum(el.amount for el in self.drinks) - sum(el.amount for el in self.releases) - self.capacity
        if excess_latent_water > 0:
            start_time = min(el.time for el in self.drinks)
            # Inverse function of sum(unabsorbed), must be solved by hand algebraically
            # Result will change if additional drinks after ETA is reached
            return start_time + \
                h*log2(sum(el.amount*2**((el.time - start_time)/h) for el in self.drinks)/excess_latent_water)
        else:
            return None

    def absorbed(self, t):
        return sum(el.amount - el.unabsorbed(t) for el in self.drinks)

    def bladder(self, t):
        return self.absorbed(t) - sum(el.amount for el in
                                      self.releases if el.time <= t)

    def add_drink(self, t, amount):
        self.history += [Drink(t, amount)]

    def add_release(self, t, permission):
        self.history += [Release(t, self.bladder(t), permission)]

    def desperation(self, t):
        # Normalize holding over capacity down to 1.0
        # So that permission is always possible
        fullness = self.bladder(t)/float(self.capacity)
        return 1.0 if fullness > 1.0 else fullness

    def roll_allowed(self, t):
        if not self._permission.time:
            return True
        else:
            return self.absorbed(t) - self.absorbed(self._permission.time) > self.capacity/fullness_quantum

    def roll_for_permission(self, t):
        # 10% chance of guaranteed yes or no
        roll = random.random()*1.2 - 0.1
        answer = roll > self.desperation(t)
        self._permission = Permission(t, answer)
        return answer
#------------------------------------------------------------------------------------------------------------
