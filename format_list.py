#!/usr/bin/env python3

newlines = []
with open("./list.txt", 'r') as f:
    lines = f.readlines()
    first_line = f",\"{lines[0].strip()}\":[\n"  
    newlines += first_line  
    for line in lines[1:]:
        newlines += f"\"{line.strip()}\",\n"
newlines = newlines[:-2]
newlines += "\n]"
with open("./list.txt", 'w') as f:
    f.writelines(newlines)