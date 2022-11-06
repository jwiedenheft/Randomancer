#!/usr/bin/env python3


from operator import indexOf
from os import path
import typer
import json
import re
import random

app = typer.Typer()

def get_table(table_name: str):
    file = open("./tables.json")
    tables = json.load(file)
    file.close()
    if table_name not in tables.keys():
        print(f"Could not find table '{table_name}'!")
        return table_name
    return (tables[table_name])

def parse_roll(roll_string: str):
    dice_matches = re.finditer('\[(.+?)\]', roll_string)
    for match in dice_matches:
        dice_string = match.group(1)
        result = str(parse_dice_element(dice_string))
        result = parse_roll(result)
        roll_string = roll_string.replace(match.group(0), result)
    
    table_matches = re.finditer('{(.+?)}', roll_string)
    for match in table_matches:
        table = match.group(1)
        if table == "encounter_distance":
            twoDsix = random.randint(1,6) + random.randint(1,6)
            result = f"{twoDsix * 20} ft."
        #print(f"Rolling on table '{table}'...")
        else:
            options = get_table(table)
            result = random.choice(options)
            result = parse_roll(result)
            #print(f"-- Rolled '{result}'.")
        start = match.start() 
        end = match.end()
        roll_string = roll_string.replace(match.group(0), result)
    return roll_string


def parse_dice_roll(roll_string: str):
    split_string = roll_string.split("+")
    if len(split_string) > 2:
        print("Invalid dice roll string!")
        return
    if len(split_string) == 2:
        add_num = int(split_string[1].strip())
    else:
        add_num = 0
    dice = split_string[0].strip()
    dice_split = dice.split("d")
    num_dice = int(dice_split[0])
    die_max = int(dice_split[1])
    roll_total = add_num
    for i in range(0, num_dice):
        die_roll = random.randint(1,die_max)
        roll_total += die_roll
    return roll_total

def parse_dice_element(roll_string: str):
    if "|" in roll_string:
        split = roll_string.split("|")
        table_name = split[0]
        table = get_table(table_name)
        dice_result = parse_dice_roll(split[1])
        if dice_result > len(table):
            return (table[-1])
        else:
            return (table[dice_result - 1])
    else:
        return (parse_dice_roll(roll_string))

@app.command()
def roll(roll_string: str, iterations: int = typer.Argument(1)):
    for i in range(0,iterations):
        result = parse_roll(roll_string)
        print(result)

@app.command()
def roll_dice(roll_string: str, iterations: int = typer.Argument(1)):
    for i in range(0,iterations):
        total = parse_dice_roll(roll_string)
        print(total)

@app.command()
def quick_roll(name: str, iterations: int = typer.Argument(1)):
    file = open("./quick_roll.json")
    data = json.load(file)
    file.close()
    if name not in data.keys():
        print(f"Could not find quick roll entry '{name}'!")
        return
    roll(data[name], iterations)

@app.command()
def list_tables():
    file = open("./tables.json")
    data = json.load(file)
    file.close()
    for key in data.keys():
        print(key)

@app.command()
def terminal():
    exitFlag = False
    while exitFlag is not True:
        string = input("> ")
        match string:
            case "exit":
                exitFlag = True
            case "list":
                list_tables()
            case _:
                roll(string, 1)



if __name__ == "__main__":
    app()

