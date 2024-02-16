import random
import string


def GenerateGuess():
    findingPassword = True
    result = 0
    while(findingPassword):
        for x in range(len(string.printable)):
            randomResult = "".join(random.sample(string.printable, k=x))
            randomResult = list(randomResult)
            listedPasswordToFind = list(passwordToFind)

            if randomResult[x] == listedPasswordToFind[x]:
                result[x] == randomResult[x]

            if len(result) == len(passwordToFind):
                findingPassword = False
                print(result)

        
passwordLength = 5
passwordToFind = "".join(random.sample(string.printable, k=passwordLength))

GenerateGuess()