#!/usr/bin/env python3

import os
import typer
import json
import re
import random

app = typer.Typer()

def init_tables():
    tables = {}
    tables_directory = "tables"
    for filename in os.listdir(tables_directory):
        f = os.path.join(tables_directory, filename)
        if os.path.isfile(f) and filename.lower().endswith('.json'):
            file = open(f, encoding='UTF8')
            table = json.load(file)
            file.close()
            tables.update(table)
    return tables

def get_table(table_name: str):
    tables = init_tables()
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
        choices = []
        match len(parts):
            case 3:
                parse_2 = parse_roll(parts[2])
                if parse_2 == '':
                    parse_2 = 1
                iterations = int(parse_2)
                for i in range(0,iterations):
                    num = parse_roll(parts[1])
                    if num in ['',0]:
                        choices.append(random.choice(options))
                    else:
                        choices.append(options[int(num)])
            case 2:
                num = int(parse_roll(parts[1]))
                choices.append(options[num-1])
            case 1:
                choices.append(random.choice(options))
        results = [parse_roll(choice) for choice in choices]
        result = "; ".join(results)
        #print(f"-- Rolled '{result}'.")
    return result

variables = {}

def parse_roll(roll_string: str):
    global variables
    #print("Roll string: " + roll_string)
    variable_assign_patten = '<([A-Z_]+?)=(.+?)>'
    match = re.search(variable_assign_patten, roll_string)
    while match is not None:
        key = parse_roll(match.group(1))
        value = parse_roll(match.group(2))
        variables[key] = value
        before = roll_string[:match.start()]
        after = roll_string[match.end():]
        roll_string = before + "" + after
        match = re.search(variable_assign_patten, roll_string)
    
    variable_fetch_pattern = '\$<(.+?)>'
    match = re.search(variable_fetch_pattern, roll_string)
    while match is not None:
        key = match.group(1)
        value = ""
        if key in variables.keys():
            value = variables[key]
        before = roll_string[:match.start()]
        after = roll_string[match.end():]
        roll_string = before + value + after
        match = re.search(variable_fetch_pattern, roll_string)
    
    table_pattern = '{(.+?)}'
    match = re.search(table_pattern, roll_string)
    while match is not None:
        table = match.group(1)
        result = parse_table_element(table)
        before = roll_string[:match.start()]
        after = roll_string[match.end():]
        roll_string = before + result + after
        #print("Roll string: " + roll_string)
        match = re.search(table_pattern, roll_string)

    dice_pattern = '\[(.+?)\]'
    match = re.search(dice_pattern, roll_string)
    while match is not None:
        dice_string = match.group(1)
        result = str(parse_dice_string(dice_string))
        before = roll_string[:match.start()]
        after = roll_string[match.end():]
        roll_string = before + result + after
        #print("Roll string: " + roll_string)
        match = re.search(dice_pattern, roll_string)
    return roll_string

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
        result = result.replace(r'\n', '\n')
        print(result)

@app.command()
def roll_dice(roll_string: str, iterations: int = typer.Argument(1)):
    for i in range(0,iterations):
        total = parse_dice_string(roll_string)
        print(total)


@app.command()
def list_tables():
    tables = init_tables()
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

