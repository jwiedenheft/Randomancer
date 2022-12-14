# Randomancer
A small Python command line app for selecting options off a random table, inspired by 
[Perchance](https://perchance.org/welcome) and intended for use in 
dice-based games like Dungeons and Dragons.

## How to Use
Roll on a table:

``` ./randomancer.py roll {table_name} ```

Create a more complicated expression that involves multiple tables:

``` ./randomancer.py roll "A {table_name} with {another_table} and {third_table}" ```

Roll dice:

``` ./randomancer.py roll "[1d20]" ```

Roll a certain dice expression against a table:

``` ./randomancer.py roll "{table_name|[1d12+8]}" ```

Roll on a table twice:

``` ./randomancer.py roll "{table_name||2}" ```

Roll 2d6 against a certain table 1d4 times:

``` ./randomancer.py roll "{table_name|[2d6]|[1d4]}" ```

Tables can be created as .json files in a ./tables/ sub-directory.

To roll on a table, pass "{table_name}" as an argument to the roll command.

Rolling dice can be done by surrounding the dice expression with square brackets.

Table results are recursively evaluated, so if you can have results that trigger 
rolls on further tables, or that include dice expressions.

Variables can be stored within the execution of a `roll` command, so that 
a given result can influence future rolls. These variables can be created and 
fetched with the following syntax:

Create: `<NAME=VALUE>`

Fetch: `$<NAME>`

Variable names can only included letters and underscores (_)

For example, in one table result we might create a variable `<ROLL_TIMES=4>` and 
then use that in a later table roll: `{table_name||$<ROLL_TIMES>}`. 
Dice strings can also be included in a variable declaration: `<ROLL_TIMES=[1d6]>`. 
Note, however, that these dice strings are evaluated when the variable is created 
rather than every time it is referenced. 


## Commands
### roll
Parses the provided roll string and returns a result.
### list-tables
Lists all tables available in the json objects in ./tables/
