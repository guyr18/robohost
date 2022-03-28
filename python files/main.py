import PersonalInformation as PerInfo
from queue import Queue
import firebase_admin
from firebase_admin import credentials, firestore
import threading
from time import sleep


#Queue object to hold all the awaiting customers
q = Queue(maxsize=0)

callback_done = threading.Event()
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

    printQueue()

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
        print("Adding {} to the queue\n".format(name))
        addPerson(name, num, partySize)
        numPeople -= 1

    printQueue()

"""
This is the testing function to display the contents of the queue
"""
def printQueue():
    print("Printing queue\n")
    while not q.empty():
        print("The queue's current size {}".format(q.qsize()))
        print("Next person in queue information")
        nextPerson = getNextPerson()
        nextPerson.printInfo()
        print("\n")

"""
This is a listener function for determining when a change is made to the database
"""
def on_snapshot_cust_info(col_snapshot, changes, readtime):
    print("Listener got new data")
    print("New documents within the collection\n")
    for change in changes:
        if change.type.name == "ADDED":
            print(f"New document {change.document.id} was added to the database")
            docDict = change.document.to_dict()
            name = docDict['name']
            partySize = docDict['partySize']
            phone = docDict['phone']
            print(f"Information for {change.document.id}\nName: {name}\nPhone: {phone}\nParty Size: {partySize}")
            print(f"Adding {name} to the queue...")
            addPerson(name, phone, partySize)
            print(f"{name} has been added to the queue.")
            print(f"New queue size {q.qsize()}\n")
        elif change.type.name == "MODIFIED":
            print(f"Document {change.document.id} has been modified in the database")
            docDict = change.document.to_dict()
            name = docDict['name']
            partySize = docDict['partySize']
            phone = docDict['phone']
            print(f"New information for {change.document.id}\nName: {name}\nPhone: {phone}\nParty Size: {partySize}\n")
    callback_done.set()

"""
main function of this file
"""
def main():

    print("Getting connection to FireStore database...")
    #Auth us into the firebase
    cred = credentials.Certificate("firebase_private_key.json")
    firebase_admin.initialize_app(cred)

    #connect to the the database, this is the entire database
    db = firestore.client()
    print("Connection made")

    #navigate to the outer collection of the database, need both custInfo and tables
    print("Getting reference to custInfo collection")
    custInfo_col_ref = db.collection('custInfo')

    #Setting up a watcher for changes
    cust_col_watch = custInfo_col_ref.on_snapshot(on_snapshot_cust_info)

    print("Getting reference to table collection")
    table_col_ref = db.collection('tables')


    while True:
        try:
            print("Listening...")
            sleep(10)
        except KeyboardInterrupt:
            break

    # Old Menu for queue testing. Leaving here for testing purposes.
    # print("Please enter the corrisponding number for the menu selection for testing.")
    # optionNum = int(input("1. Enter in single person information\n2. Enter in multiple people information\n"))
    # if optionNum == 1:
    #     testEnterSingle()
    # if optionNum == 2:
    #     testEnterMulti()

    printQueue()
    cust_col_watch.unsubscribe()
    print("Exiting")

"""
Causes the main function to run
"""
if __name__ == "__main__":
    main()
