#Imports
from Functions import *
import time


#Print welcome message and choice menu
print("Welcome to my calculator!\nChoose a operator:\n")

print("""1. Addition
2. Subtraction
3. Multiplikation
4. Division\n""")

#User input for choosing function
userChosenMethod = input()

#Simulating work
print("\nOperator chosen...")
time.sleep(1)

#User input for first number
print("\nEnter first numer: ")
userChosenNumber1 = input()

#User input for second number
print("\nEnter second number:")
userChosenNumber2 = input()

#Call off input matcher function  
userInputMatching(userChosenMethod, userChosenNumber1, userChosenNumber2)