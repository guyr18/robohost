import PersonalInformation as PerInfo
import TableInformation as TableInfo
from queue import Queue
import firebase_admin
from firebase_admin import credentials, firestore
from time import sleep
from wait import computeWaitTime
import smtplib, ssl

# Queue object to hold all the awaiting customers
q = Queue(maxsize=0)

# List to hold onto the tables
tableList = []

needToGetNextCustomer = True

savedCust = -1

#Email Stuff
emailServer = smtplib.SMTP('smtp.gmail.com', 587)
emailServer.starttls()
roboEmail = "robohostnoreply@gmail.com"
roboPass = "Csci4230!"
emailServer.login(roboEmail, roboPass)



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
Function to get the wait time in minutes of the queue at the queue's current size

@:return    the wait time given the queue
"""
def getWaitTime():
    return computeWaitTime(q)

"""
Will get the next person in the queue

RETURNS the next PersonalInfo object from the queue
"""
def getNextPerson():
    if q.empty():
        return -1
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
This is the testing function to test out the creation of the table list
"""
def testTableStuff():
    tableCount = int(input("Please enter the number of tables you plan to test"))
    while tableCount > 0:
        print("Please enter the next table's information")
        tableID = input("Please enter in the table's ID\n")
        seatCount = input("Please enter the seat count for the table\n")
        status = input("Please enter the table's status\n")
        print(f"Adding Table {tableID} to the table list\n")
        addTable(tableID, seatCount, status)
        tableCount -= 1

    printTableList()

"""
This function is used to test out the two case of check can sit
"""

def testCheckCanSit(table1, cust1, table2, cust2):
    print(f"Testing the check can sit function with table: {table1.getID()} and customer: {cust1.getName()}")
    if checkCanSit(table1, cust1):
        print(f"The first go around of function returned true, test one passed.")
    else:
        print(f"The first go around of the function returned false, test failed.")
    print(f"Testing the check can sit function with table: {table2.getID()} and customer: {cust2.getName()}")
    if not checkCanSit(table2, cust2):
        print(f"The second go around of the function returned false, test two passed.")
    else:
        print(f"The second go around of the function returned true, test two failed.")

"""
Finds a table based on the the submitted ID to search for
@return The table object associated with the ID if one is found
"""
def FindTableInList (searchID):
    print(f"Looking for table {searchID}...")
    for table in tableList:
        print(f"checking {table.getID()}...")
        if table.checkID(searchID):
            print(f"Found table {table.tableID}\n")
            return table
    print(f"Found no table matching {searchID}...sorry...")

"""
This is a function to find a table within the list of the tables and update its status
@:param     searchID        The table ID that is being looked for
@:param     newStatus       The new status that is being updated to for the table
"""
def updateStatusTableID(searchID, newStatus):
    for table in tableList:
        if table.checkID(searchID):
            table.updateStatus(newStatus)

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
Function to add a table to the list of tables

@param      tableID     The ID associated with a table
@param      seatCount   The number of seats at a table
@:param     status      The tables status
"""
def addTable(tableID, seatCount, status):
    tempTable = TableInfo.TableInfo(tableID, seatCount, status)
    tableList.append(tempTable)

"""
This is the function used to display the contents of the table List
"""
def printTableList():
    for table in tableList:
        table.printTableInfo()

"""
This is the function for comparing a table's seat capacity to the customer party size to determine if the customer can be seated at that table

@:param     table       The table object being looked at
@:param     cust        The customer object being looked at

@:return    bool based on if customer can sit
"""
def checkCanSit(table, cust):
    return table.canSit(cust.getPartySize())

"""
This is a function to check all the tables within the tables list and add the ones whose status is marked as available
to a list of available tables.

@:return list of all available tables
"""
def allAvailableTableList():
    availableTables = []
    print("Getting a list of available tables...")
    for table in tableList:
        if table.isAvailable():
            print(f"Table {table.getID()} was marked as available adding to the list...")
            availableTables.append(table)
            print("Table was added...")
    print(f"There are a total of {len(availableTables)}")
    return availableTables

"""
Function to determine if a customer can sit at one of the tables within the list, returning the table id of that table.

@param      cust        the customer being looked at
@param      tables      the list of tables being check

@:return    A table ID associated with a table that the customer can sit at, an ID of -1 marks that no table was found
"""
def tableMarker(cust, tables):
    if cust == -1:
        return cust
    for table in tables:
        if checkCanSit(table, cust):
            print(f"A table has been found, table {table.getID()}")
            return table.getID()
    return -1

"""
Function that will set an available table to the waiting state because a new customer has been added to it

@:param     tableID     the table ID that corresponds to the table that needs to be updated
@:return    the table the was found
"""
def setTableWaiting(tableID):
    tempTable = FindTableInList(tableID)
    print(f"Setting table {tempTable.getID()} to waiting...")
    tempTable.changeWaitingForCust()
    print(f"New status for {tempTable.getID()} is {tempTable.getStatus()}")
    return tempTable

"""
Sends an email once a person is added to the queue telling the person their estimated wait time

@:param     cust        a customer object that hold personal information
"""
def sendWaitEmail(custName, custEmail):
    print(f"Got customer {custName}...")
    try:
        message = "Hey there " + custName + ". You have been added to the queue. Your current wait time is " + \
                    str(computeWaitTime(q)) + " minutes."
        emailServer.sendmail(roboEmail, custEmail, message)
        print("Customer added email sent...")
    except BaseException as error:
        print(f"Something didn't work...\n{error=}, {type(error)=}")


def sendTableInfoEmail(cust, table):
    print(f"Preparing to send an email to {cust.getName()} letting them know they have been seated at {table.getID()}")
    try:
        custName = cust.getName()
        custEmail = cust.getEmail()
        tableID = table.getID()
        message = "Hey there " + custName + ".\n" + \
                  "Your table is ready. Please report to table " + str(tableID) + ".\n" + \
                  "Enjoy your meal!"
        emailServer.sendmail(roboEmail, custEmail, message)
        print("Customer table assign email sent...")
    except BaseException as error:
        print(f"Something didn't work...\n{error=}, {type(error)=}")

"""
This is a listener function for determining when a change is made to the database
"""
def on_snapshot_cust_info(col_snapshot, changes, readtime):
    print("Customer listener got new data")
    print("New information within the collection\n")
    for change in changes:
        docDict = change.document.to_dict()
        name = docDict['name']
        partySize = int(docDict['partySize'])
        email = docDict['email']
        if change.type.name == "ADDED":
            print(f"New document {change.document.id} was added to the database")
            print(f"Information for {change.document.id}\nName: {name}\nEmail: {email}\nParty Size: {partySize}")
            print(f"Adding {name} to the queue...")
            addPerson(name, email, partySize)
            print(f"{name} has been added to the queue.")
            print(f"New queue size {q.qsize()}\n")
            print("Attempting to send email...")
            sendWaitEmail(name, email)
    #callback_cust_done.set()

def on_snapshot_table_info(col_snapshot, changes, readtime):
    print("Table listener got new data")
    print("New information within the collection\n")
    for change in changes:
        docDict = change.document.to_dict()
        tableID = int(change.document.id)
        seatCount = int(docDict['numSeats'])
        status = docDict['strState']
        if change.type.name == "ADDED":
            print(f"New document {change.document.id} was added to the database")
            addTable(tableID, seatCount, status)
            print(f"Table {tableID} has been added to the list of tables")
        elif change.type.name == 'MODIFIED':
            print(f"Document {change.document.id} was modified...\nUpdating information related to table: {change.document.id}...")
            updateStatusTableID(tableID, status)
            print(f"New information for {tableID}...")
            tempTable = FindTableInList(tableID)
            tempTable.printTableInfo()
    #callback_table_done.set()

"""
main function of this file
"""
def main():

    print("Getting connection to FireStore database...")
    # Auth us into the firebase
    cred = credentials.Certificate("firebase_private_key.json")
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(cred)

    # connect to the the database, this is the entire database
    db = firestore.client()
    print("Connection made")

    # Navigate to the outer collection of the database
    print("Getting reference to custInfo collection")
    custInfo_col_ref = db.collection('custInfo')
    # Setting up the listeners customer information
    cust_col_watch = custInfo_col_ref.on_snapshot(on_snapshot_cust_info)

    print("Getting reference to table collection")
    table_col_ref = db.collection('tables')
    # Setting up the listener for table information
    table_col_watch = table_col_ref.on_snapshot(on_snapshot_table_info)

    # Loop causes this to keep running allowing the listener to constantly be active
    # Without the loop function will exit causing an exit to the code
    while True:
        tempAvaList = allAvailableTableList()
        global needToGetNextCustomer
        global savedCust
        if needToGetNextCustomer:
            print("Checking the queue for next customer")
            if not q.empty():
                print("Queue was not empty")
                curCust = getNextPerson()
                print(f"Found {curCust.getName()}")
                needToGetNextCustomer = False
                savedCust = curCust
            else:
                print("Waiting for another customer to enter queue")
        if savedCust != -1:
            print(f"Looking at the available tables for {savedCust.getName()}")
            tempTableID = tableMarker(savedCust, tempAvaList)
            if tempTableID != -1:
                tempTable = setTableWaiting(tempTableID)
                table_col_ref.document(str(tempTable.getID())).update({"strState": tempTable.getStatus()})
                print("Update was made")
                print("Attempting to send an email to the customer...")
                sendTableInfoEmail(savedCust, tempTable)
                needToGetNextCustomer = True
                savedCust = -1

        print("Listening for changes...")
        sleep(10)

"""
Causes the main function to run if this script is running
"""
if __name__ == "__main__":
    main()