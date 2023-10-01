
"""
This module provides the DiceRollSettings class, maintains the state of the
items used by DiceRollCheck.

Note that this class only stores the state of the items that can be applied to
a roll of the dice. It does not actually roll them.

Written By: Craig R. Campbell  -  February 2022
"""

from jasl.ui.data.actions      import Actions
from jasl.ui.data.phases       import Phases
from jasl.ui.data.rate_of_fire import RateOfFire

class DiceRollSettings:
    """
    A class used to store the current values of the key items that affect an ASL
    dice roll. This includes the turn phase, action to be taken, and the rate of
    fire. Note that the latter applies only under specific conditions.
    """

    # Map the legal action(s) for each phase.

    __phase_to_action_map = { Phases.RALLY:          [Actions.RALLY], \
                              Phases.PREP_FIRE:      [Actions.IFT,Actions.MORALE_CHECK], \
                              Phases.MOVEMENT:       [Actions.IFT,Actions.MORALE_CHECK], \
                              Phases.DEFENSIVE_FIRE: [Actions.IFT,Actions.MORALE_CHECK], \
                              Phases.ADVANCING_FIRE: [Actions.IFT,Actions.MORALE_CHECK], \
                              Phases.ROUT:           [Actions.IFT,Actions.MORALE_CHECK], \
                              Phases.ADVANCE:        [], \
                              Phases.CLOSE_COMBAT:   [Actions.CCT] }

    def __init__(self):
        """
        Initializes a class instance. The default phase and action are "Rally"
        and the rate of fire is set to zero.
        """

        self.__phase = Phases.RALLY
        self.__action = Actions.RALLY
        self.__rate_of_fire = RateOfFire.NONE

    def __phase_has_action(self,phase,action):
        # Returns a value indicating whether or not the indicated action is
        # valid in the specified phase.

        try:
            self.__phase_to_action_map.get(phase).index(action)
        except ValueError:
            return False

        return True


    def phase(self):
        """Returns the current phase setting."""

        return self.__phase

    def set_phase(self,phase):
        """
        Changes the phase setting to the specified value. If the current action
        is not available in the specified phase it will be changed to the first
        one associated with the new phase.
        Parameters
        ----------
        phase : Phases
            The new phase setting
        """

        # Don't bother with the rest if there is no actual change.

        if phase == self.__phase:
            return

        # Update the action setting if the current one isn't compatible with the
        # new phase.

        if not self.__phase_has_action(phase,self.__action):
            self.__action = self.__phase_to_action_map.get(phase)[0]

        self.__phase = phase

    def action(self):
        """Returns the current action setting."""

        return self.__action

    def actions(self):
        """Returns a list of the actions available during the current phase."""

        return self.__phase_to_action_map.get(self.__phase)

    def set_action(self,action):
        """
        Changes the action setting to the specified value. If the current phase
        is not compatible with the new action it will be changed to the first
        appropriate value.
        Parameters
        ----------
        action : Actions
            The new action setting
        """

        # Don't bother with the rest if there is no actual change.

        if action == self.__action:
            return

        # If the new action isn't compatible with the current phase, find the
        # first phase that will allow it.

        if not self.__phase_has_action(self.__phase,action):
            for phase in self.__phase_to_action_map:
                if self.__phase_has_action(phase,action):
                    self.__phase = phase

        self.__action = action

    def rate_of_fire(self):
        """Returns the current rate of fire setting. If it is not applicable
        to the current phase and action the return value is RateOfFire.NONE."""

        if self.rate_of_fire_is_applicable():
            return self.__rate_of_fire

        return RateOfFire.NONE

    def set_rate_of_fire(self,rate_of_fire):
        """
        Changes the rate of fire setting to the specified value.
        ----------
        rate_of_fire : RateOfFire
            The new rate of fire setting
        """

        self.__rate_of_fire = rate_of_fire

    def rate_of_fire_is_applicable(self):
        """ Indicates if the rate of fire value applies for the current action.
        """

        return Actions.IFT == self.__action

    def __str__(self):
        """Returns a string describing the state of the current class instance."""

        label  = 'Settings - '
        phase  = 'phase: ' + str(self.phase())
        action = 'action: ' + str(self.action())
        rof    = 'rate of fire: ' + str(self.rate_of_fire())

        if not self.rate_of_fire_is_applicable():
            rof = ''

        return '\t'.join([label,phase,action,rof])

# @cond TEST

if __name__ == "__main__":
    diceRollSettings = DiceRollSettings()
    print(diceRollSettings.actions())
    print(diceRollSettings) # Show default state.
    diceRollSettings.set_phase(Phases.PREP_FIRE)
    diceRollSettings.set_rate_of_fire(RateOfFire.ONE)
    print(diceRollSettings.actions())
    print(diceRollSettings)
    diceRollSettings.set_action(Actions.RALLY)
    print(diceRollSettings)

# @endcond
