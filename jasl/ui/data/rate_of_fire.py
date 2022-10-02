"""
This module provides the RateOfFire enum.

Written By: Craig R. Campbell  -  September 2022
"""

from enum import Enum

class RateOfFire(Enum):
    """
    An enum class used to represent rate of fire values that may be available to
    an ASL counter.

    Note that the string representation of the enum value will be returned
    as a label rather than a direct copy (e.g., "1" instead of "ONE").
    """

    NONE = 0
    ONE = 1
    TWO = 2
    THREE = 3

    __enum_attr_map__ = { 'NONE':  ['None'], \
                          'ONE':   ['1'], \
                          'TWO':   ['2'], \
                          'THREE': ['3'] }

    def __str__(self):
        """Returns the label associated with the enum value."""
        return self.__class__.__enum_attr_map__[self.name][0]

# @cond TEST

if __name__ == "__main__":
    none = RateOfFire.NONE
    print(none)
    print(none.name)
    print(none.value)
    print(str(none))
    print(repr(none))

# @endcond
