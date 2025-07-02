"""Farmer entity type class of inseeds_farmer_management"""

import numpy as np
import math

from inseeds.components import farming


class Farmer(farming.management.tillage.Farmer):

    def __init__(self, **kwargs):
        """Initialize an instance of Farmer."""
        super().__init__(**kwargs)  # must be the first line

        self.capital = 1000 # TODO: what is the initial C?

    @property
    def capital(self):
        self._capital = self.cropyield
        return self._capital
    
    # TODO: Do we need this?
    # @capital.setter
    # def capital(value):
    #     self._capital = value

    # TODO: Implement new equation
    @property
    def attitude_own_land(self):
        super().attitude_own_land(self)

    # TODO: Impelemtn new equation
    @property
    def attitude_social_learning(self):
        super().attitude_social_learning(self)

    def update_pbc(self, C, TC):

        if C >= TC:

            if self.tpb > 0.5:
                # decrease pbc after strategy switch
                self._pbc =  max(self._pbc - 0.25, 0.5)

            # increase pbc if tpb is near 0.5 to learn from own experience
            elif self.tpb <= 0.5 and self.tpb > 0.4:
                self._pbc =  min(
                    self._pbc + self.diff_pbc_income_function(C, TC) + self.diff_pbc_ts_function(ts = self.strategy_switch_duration), 1
                )
            else:
                self._pbc =  min(
                    self._pbc + self.diff_pbc_income_function(C, TC), 1
                )
        else:
            self._pbc = 0.5

    def diff_pbc_income_function(C, TC):
        alpha = 3 #shift to the right
        beta = 0.5
        gamma = 6
        return 0.25 / (1 + math.exp(-gamma*((C - (alpha*TC))/(TC/beta))))
    
    # TODO: needs to be revised  
    def diff_pbc_ts_function(ts):
        return 0.25 / ts

