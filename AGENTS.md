# Repository guidance

## Build, test, and lint

- There is no conventional build, test, or lint configuration, and no checked-in test suite. Consequently, there is no existing single-test command.
- Run the interactive dice-roll wizard from the repository root with `PYTHONPATH=. python3 DiceRollWizard/drw.py`.
- Pylint is an external system dependency, not a repository dependency. When it is installed, run `pylint jasl DiceRollWizard` and keep the code clean with no Pylint warnings.
- The Makefiles provide `docs`, `doxygen`, and `clean` targets, not application build or test targets. They include `$(JASL_BASE)/util/jasl.make` and depend on shared build variables and documentation tools supplied outside this repository.
- Set `JASL_BASE` to the parent `jasl` repository root when building documentation. The parent repository is not required to run the programs in this repository.

## Architecture

- This standalone repository mirrors many classes and interfaces from the parent `jasl` repository, but the repositories do not contain identical APIs. Prefer common interfaces where counterparts exist, while preserving classes that are specific to either repository.
- `jasl/utilities/dice.py` owns random die generation and exposes the individual dice and combined white/colored total. It does not interpret a roll.
- `jasl/ui/data/` defines the `Actions`, `Phases`, and `RateOfFire` enums used as shared domain values.
- `DiceRollWizard/drw_settings.py` stores the selected phase, action, and rate of fire. Its phase-to-action map constrains valid combinations and rate of fire applies only to IFT actions.
- `DiceRollWizard/drw_check.py` combines a `Dice` result with those settings to produce possible rule effects; it does not manage the interactive settings flow.
- `DiceRollWizard/drw.py` is the interactive command-line entry point. It gathers and confirms settings, then creates a `DiceRollCheck` from a fresh `Dice` roll.

## Code conventions

- Keep responsibilities separate: dice generation belongs in `jasl.utilities`, shared domain enums in `jasl.ui.data`, settings validation in `drw_settings.py`, and interpretation of roll outcomes in `drw_check.py`.
- Enum members have internal names and numeric values, while their display labels are defined in each enum's `__enum_attr_map__` and returned by `__str__`. Preserve these labels when adding or changing members.
- The domain classes expose values through methods such as `phase()`, `actions()`, and `combined_result()` rather than public attributes; follow that interface pattern in callers.
- Existing files use `if __name__ == "__main__":` examples. These examples are manual demonstrations, not an automated test suite.
