#!/usr/bin/env python3


from operator import indexOf
import os
from os import path
import typer
import json
import re
import random

app = typer.Typer()
tables = {}
tables_directory = "tables"
for filename in os.listdir(tables_directory):
    f = os.path.join(tables_directory, filename)
    if os.path.isfile(f) and filename.lower().endswith('.json'):
        file = open(f)
        table = json.load(file)
        file.close()
        tables.update(table)

def get_table(table_name: str):
    if table_name not in tables.keys():
        print(f"Could not find table '{table_name}'!")
        return table_name
    return (tables[table_name])

def parse_table_element(table_string: str):
    result = table_string
    if table_string == "encounter_distance":
        twoDsix = random.randint(1,6) + random.randint(1,6)
        result = f"{twoDsix * 20} ft."
    #print(f"Rolling on table '{table}'...")
    else:
        parts = table_string.split("|")
        table = parts[0]
        options = get_table(table)
        if len(parts) > 1:
            num = int(parse_roll(parts[1]))
            choice = options[num]
        else:
            choice = random.choice(options)
        result = parse_roll(choice)
        #print(f"-- Rolled '{result}'.")
    return result

def parse_roll(roll_string: str):
    words = roll_string.split(" ")
    i = 0
    for word in words:
        result = word
        if re.match('\[(.+?)\]', word):
            dice_string = word[1:-1]
            result = str(parse_dice_string(dice_string))
            result = parse_roll(result)
        elif re.match('{(.+?)}', word):
            dice_string = word[1:-1]
            result = parse_table_element(dice_string)
        words[i] = result
        i += 1
    return ' '.join(words)

def parse_dice_string(roll_string: str):
    roll_string = roll_string.lower()
    operators = re.findall("[+|-|*]", roll_string)
    if len(operators) > 0:
        operator = operators[0]
        parts = roll_string.split(operator)
        if len(parts) > 2:
            print("Dice string has more than one operator!")
            return 0
        first_num = int(parse_dice_string(parts[0]))
        second_num = int(parse_dice_string(parts[1]))
        match operator:
            case "+":
                total = first_num + second_num
            case "-":
                total = first_num - second_num
            case "*":
                total = first_num * second_num
        return int(total)
    elif re.search("d",roll_string):
        dice_split = roll_string.split("d")
        num_dice = int(dice_split[0])
        die_max = int(dice_split[1])
        roll_total = 0
        for i in range(0, num_dice):
            die_roll = random.randint(1,die_max)
            roll_total += die_roll
        return int(roll_total)
    else:
        return int(roll_string)

@app.command()
def roll(roll_string: str, iterations: int = typer.Argument(1)):
    for i in range(0,iterations):
        result = parse_roll(roll_string)
        print(result)

@app.command()
def roll_dice(roll_string: str, iterations: int = typer.Argument(1)):
    for i in range(0,iterations):
        total = parse_dice_string(roll_string)
        print(total)

@app.command()
def list_tables():
    for key in tables.keys():
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

