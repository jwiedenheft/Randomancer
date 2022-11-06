# Randomancer
A small python app for selecting options off a random table, inspired by games like Dungeons and Dragons.

## How to Use
Tables can be created as .json files in a ./tables/ sub-directory.

To roll on a table, pass "{table_name}" as an argument to the roll command.

Rolling dice can be done by surrounding the dice expression with square brackets.

Table results are recursively evaluated, so if you can have results that trigger rolls on further tables, 
or that include dice expressions.

## Commands
### roll
### list-tables
Lists all tables available in the json objects in ./tables/


## Dependencies
- [Typer](https://github.com/tiangolo/typer)