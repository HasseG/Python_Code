#!/usr/bin/env python3
import re
# Part 1
#------------------------------------------------------------------------
# Elf game. Blue, Green and Red cubes.
# Every game has a ID follows by a ':' and then the cubes that was showed.
# Every game has sets seperated with ';' 

# In every game random number of colored cubes show
# Number of cubes -> 12 RED, 13 GREEN, 14 BLUE

# If one or more of the sets include more than the set number of cubes
#   Then the game ID is ignored
# Else we add the game ID to the total SUM,
#   return the SUM


RED_CUBES = 12
GREEN_CUBES = 13
BLUE_CUBES = 14

def retrieve_data():
    with open("/home/hgs/TrainingCode/Python_Code/AdventOfCode/Day_2/input.txt", "r") as input_data:
        data = input_data.read().split("\n")
    return data


def determin_set(sets = list):
    result = False
    for set in sets:
        set = set.split(",")
        for cubes in set:
            if cubes.find("red") > 0:
                num_cubes = int(cubes.replace("red", ""))
                if num_cubes <= RED_CUBES:
                    print("Passed: " + cubes)
                    result = True
                else:
                    print("Failed: " + cubes)
                    return False
            elif cubes.find("green") > 0:
                num_cubes = int(cubes.replace("green", ""))
                if num_cubes <= GREEN_CUBES:
                    print("Passed: " + cubes)
                    result = True
                else:
                    print("Failed: " + cubes)
                    return False
            elif cubes.find("blue") > 0:
                num_cubes = int(cubes.replace("blue", ""))
                if num_cubes <= BLUE_CUBES:
                    print("Passed: " + cubes)
                    result = True
                else:
                    print("Failed: " + cubes)
                    return False
    return result

def prepare_set(split_line):
    result = []
    for line in split_line:
        result.append(line.replace(" ", ""))
    return result          

def main():
    sum = 0
    data  = retrieve_data()
    for raw_line in data:
        split_line = re.split(";|:", raw_line)[1:]
        if determin_set(prepare_set(split_line)):
            game_id = int(raw_line.split(":")[0].replace("Game ", ""))
            sum += game_id
            print("Possible: " + str(game_id) + "\n")
        else:
            game_id = int(raw_line.split(":")[0].replace("Game ", ""))
            print("Impossible: " + str(game_id) + "\n")
            
    print(sum)
            
        
main()

