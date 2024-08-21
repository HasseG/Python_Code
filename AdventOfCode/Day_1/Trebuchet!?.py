#!/usr/bin/env python3
spelledNumbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]



result = 0
data = ""
with open("/home/hgs/TrainingCode/Python_Code/AdventOfCode/Day_1/puzzle_input.txt", "r") as calibrations:
    data = calibrations.read().split("\n")


def spelledNumberMatcher(matcher = str):
    if matcher.isdigit():
        return matcher
    match matcher:
        case "one":
            return "1"
        case "two":
            return "2"
        case "three":
            return "3"
        case "four":
            return "4"
        case "five":
            return "5"
        case "six":
            return "6"
        case "seven":
            return "7"
        case "eight":
            return "8"
        case "nine":
            return "9"
        

for line in data:
    foundNumbers = {}
    if line == "":
        continue    
    lineEndIndex = line.index(line[-1])

    for matcher in spelledNumbers:
        matchIndex = 0
        while matchIndex < len(line):
            matchIndex = line.find(matcher, matchIndex)
            if matchIndex == -1:
                break
            foundNumbers[matchIndex] = matcher
            matchIndex += len(matcher)

        
            
    for char in line:
        if char.isdigit():
            
            charIndex = line.index(char)
            
            stepper = 1
            searching = True
            
            while searching:
                if charIndex in foundNumbers:
                    charIndex = line.index(char, stepper)
                    stepper += 1
                    continue
                
                searching = False
            
            foundNumbers[charIndex] = char
    fKeys = list(foundNumbers.keys())
    fKeys.sort()
        
    firstNumberPre = foundNumbers[fKeys[0]]
    lastNumberPre = foundNumbers[fKeys[-1]]
    
    firstNumberPost = spelledNumberMatcher(firstNumberPre)
    lastNumberPost = spelledNumberMatcher(lastNumberPre)
    
    result += int(f"{firstNumberPost}{lastNumberPost}")

print(f"\nResult: {result}")
