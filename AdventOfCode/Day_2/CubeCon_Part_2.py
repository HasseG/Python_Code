#!/usr/bin/env python3
import re
# Part 2
#------------------------------------------------------------------------
# Find the lowest number of cubes needed to make a game possible.
#   What number of green, blue and red cubes are needed.
#   Find the highest number for each of the cubes.
#   If a game has 20 red, 25 red, 5 blue, 12, blue, 24 green, 9 green
#       Then a the lowest number of cubes required to make the game possible is:
#           25 red, 12 blue, 24 green
#       That equals to 25 * 12 * 24 = 7.200
#       Take that number at add it to the total sum



def retrieve_data():
    with open("/home/hgs/TrainingCode/Python_Code/AdventOfCode/Day_2/input.txt", "r") as input_data:
        data = input_data.read().split("\n")
    return data


def determin_nums(game = [], color = str):
    result = []
    for set in game:
        splittet_set = set.split(",")
        for cube in splittet_set:
            if cube.find(color) > 0:
                extracted_num = int(cube.replace(color, "").strip())
                result.append(extracted_num)
    result.sort()
    result = result[-1]
    return result      

                     


def prepare_set(split_line):
    result = []
    for line in split_line:
        result.append(line.strip())
    return result          

def main():
    sum = 0
    blue_num = ""
    red_num = ""
    green_num = ""
    data  = retrieve_data()
    counter = 1
    for raw_line in data:
        split_line = re.split(";|:", raw_line)[1:]
        
        blue_num = determin_nums(split_line, "blue")
        red_num = determin_nums(split_line, "red")
        green_num = determin_nums(split_line, "green")
        print(f"Game {counter}: {str(green_num)} green, {str(red_num)} red, {str(blue_num)} blue")
        result = blue_num * red_num * green_num
        sum += result
        counter += 1
    print(sum)
            
main()
