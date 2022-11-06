# Randomancer
A small Python command line app for selecting options off a random table, inspired by 
[Perchance](https://perchance.org/welcome) and intended for use in 
dice-based games like Dungeons and Dragons.

## How to Use
``` ./randomancer.py roll "{table_name}" ```
``` ./randomancer.py roll "[1d20]" ```
``` ./randomancer.py roll "{table_name|[1d12+8]}" ```
``` ./randomancer.py roll "A {table_name} with {another_table} and {third_table}" ```

Tables can be created as .json files in a ./tables/ sub-directory.

To roll on a table, pass "{table_name}" as an argument to the roll command.

Rolling dice can be done by surrounding the dice expression with square brackets.

Table results are recursively evaluated, so if you can have results that trigger 
rolls on further tables, or that include dice expressions.

## Commands
### roll
### list-tables
Lists all tables available in the json objects in ./tables/


## Dependencies
- [Typer](https://github.com/tiangolo/typer)