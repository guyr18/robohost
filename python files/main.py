import PersonalInformation as PerInfo
from queue import Queue

#Queue object to hold all the awaiting customers
q = Queue(maxsize=0)


"""
Function to add a person to the queue

@param name         Name associated with a person
@param number       Number associated with a person
@param partySize    The party size that is associate with a person
"""
def addPerson(name, number, partySize):
    tempPerson = PerInfo.PersonalInfo(name, number, partySize)
    q.put(tempPerson)

"""
Will get the next person in the queue

RETURNS the next PersonalInfo object from the queue
"""
def getNextPerson():
    nextPerson = q.get()
    return nextPerson

"""
This is the testing function that is meant to test out the personal information entering manually for a single person
"""
def testEnterSingle():
    name1 = input("Please enter person 1's name\n")
    num1 = input("Please enter person 1's number\n")
    ps1 = int(input("Please enter person 1's party size\n"))

    addPerson(name1, num1, ps1)

    print("The queue's current size {}".format(q.qsize()))

    tempPerson = getNextPerson()

    print("Person at the top of queue")
    tempPerson.printInfo()

"""
This is the testing function that is meant to test out entering multiple person
"""
def testEnterMulti():
    numPeople = int(input("Please enter the number of people to enter in\n"))
    while numPeople > 0:
        print("Please enter the next person's information")
        name = input("Please enter in the name\n")
        num = input("Please enter in the phone number\n")
        partySize = int(input("Please enter in the party size\n"))

        addPerson(name, num, partySize)
        numPeople -= 1

    while not q.empty():
        print("Next person in queue information")
        nextPerson = getNextPerson()
        nextPerson.printInfo()


"""
main function of this file
"""

def main():
    print("Please enter the corrisponding number for the menu selection for testing.")
    optionNum = int(input("1. Enter in single person information\n2. Enter in multiple people information\n"))
    if optionNum == 1:
        testEnterSingle()
    if optionNum == 2:
        testEnterMulti()

"""
Causes the main function to run
"""
if __name__=="__main__":
    main()
