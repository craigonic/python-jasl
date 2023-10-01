"""
This program allows ASL (Advanced Squad Leader) players to set the parameters
associated with a dice roll (phase, action, etc.) and then see the result. The
intent is to provide a list of rules / actions that may apply under the
specified conditions.

Note that the purpose of this program is to provide assistance with the rules
around dice rolls. Players are expected to know and apply the rules.

Written By: Craig R. Campbell  -  November 2022
"""

from jasl.ui.data.actions      import Actions
from jasl.ui.data.phases       import Phases
from jasl.ui.data.rate_of_fire import RateOfFire
from jasl.utilities.dice       import Dice

from drw_check    import DiceRollCheck
from drw_settings import DiceRollSettings

dice_roll_settings = DiceRollSettings()

def __roll_the_dice():
    return DiceRollCheck(Dice(), \
                         dice_roll_settings.phase(), \
                         dice_roll_settings.action(), \
                         dice_roll_settings.rate_of_fire())

def __yes_no_prompt(prompt_text,default,alternative):
    while True:
        user_input = input(prompt_text) or default

        if len(user_input.strip()) == 1 and user_input.isalpha():
            if user_input.lower() == default:
                return False
            if user_input.lower() == alternative:
                return True

while True:
    # Show current settings configuration

    print(dice_roll_settings)

    # Prompt player to change the settings

    if __yes_no_prompt('\nChange current settings (y/N): ','n','y'):
        while True:
            # Prompt player to change the phase

            if __yes_no_prompt('Change current phase (y/N): ','n','y'):
                while True:
                    print('\nSelect the number associated with the new phase.')
                    for entry in Phases:
                        print(f'{entry.value}) {entry}')
                    phase_input = input('Selection: ')

                    if phase_input.isdigit() and \
                       int(phase_input) >= Phases.RALLY.value and \
                       int(phase_input) <= Phases.CLOSE_COMBAT.value:
                        dice_roll_settings.set_phase(Phases(int(phase_input)))
                        break

            # Prompt player to change the action

            if __yes_no_prompt('Change current action (y/N): ','n','y'):
                while True:
                    print('\nSelect the number associated with the new action.')
                    valid_actions = dice_roll_settings.actions()
                    for entry in valid_actions:
                        print(f'{entry.value}) {entry}')
                    action_input = input('Selection: ')

                    if action_input.isdigit() and \
                       int(action_input) >= Actions.CCT.value and \
                       int(action_input) <= Actions.RALLY.value and \
                       Actions(int(action_input)) in valid_actions:
                        dice_roll_settings.set_action(Actions(int(action_input)))
                        break

            # If applicable, prompt player to change the rate of fire

            if dice_roll_settings.rate_of_fire_is_applicable():
                if __yes_no_prompt('Change rate of fire (y/N): ','n','y'):
                    while True:
                        print('\nSelect the new rate of fire.')
                        for entry in RateOfFire:
                            print(f'{entry.value}) {entry}')
                        rate_of_fire_input = input('Selection: ')

                        if rate_of_fire_input.isdigit() and \
                           int(rate_of_fire_input) >= RateOfFire.NONE.value and \
                           int(rate_of_fire_input) <= RateOfFire.THREE.value:
                            dice_roll_settings.set_rate_of_fire(RateOfFire(int(rate_of_fire_input)))
                            break

            # Show updated settings

            print(f'\n{dice_roll_settings}\n'.format(dice_roll_settings))

            # Prompt player to confirm updated settings are correct

            if not __yes_no_prompt('Proceed with current settings (Y/n): ','y','n'):
                break

    print(f'\n{__roll_the_dice()}\n')

    # Prompt player to continue using this program

    if __yes_no_prompt('Continue (Y/n): ','y','n'):
        break
