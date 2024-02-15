#This is my functions for basic math calculations
def Addition(number1, number2):
    return int(number1) + int(number2)

def Subtraction(number1, number2):
    return int(number1) - int(number2)

def Multiplikation(number1, number2):
    return int(number1) * int(number2)

def Division(number1, number2):
    return int(number1) / int(number2)

#Function for matching user input with propper math function
def userInputMatching(argument, number1, number2):
    #Variable for capturing result
    result = 0

    #Switch case
    match argument:
        case "1":
            print("Chosen operator is addition:\n")
            result = Addition(number1, number2)

        case "2":
            print("Chosen operator is subtraction:\n")
            result = Subtraction(number1, number2)

        case "3":
            print("Chosen operator is multiplikation:\n")
            result = Multiplikation(number1, number2)

        case "4":
            print("Chosen operator is division:\n")
            result = Division(number1, number2)

        case default:
            result = "No match found"
    #End of switch case

    #Printing result
    print("Result is: " + str(result))