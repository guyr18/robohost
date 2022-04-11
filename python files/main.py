import PersonalInformation as PerInfo
import TableInformation as TableInfo
from queue import Queue
import firebase_admin
from firebase_admin import credentials, firestore
#import threading
from time import sleep


# Queue object to hold all the awaiting customers
q = Queue(maxsize=0)

# List to hold onto the tables
tableList = []

NewAssignment = False

global needToGetNextCustomer
needToGetNextCustomer = True

# callback_cust_done = threading.Event()
# callback_table_done = threading.Event()

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
        # elif change.type.name == "MODIFIED":
        #     print(f"Document {change.document.id} has been modified in the database")
        #     print(f"New information for {change.document.id}\nName: {name}\nEmail: {email}\nParty Size: {partySize}\n")
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
        try:
            tempAvaList = allAvailableTableList()
            global needToGetNextCustomer
            if needToGetNextCustomer:
                print("Getting next customer from the queue...")
                curCust = getNextPerson()
                print(f"Got {curCust.getName()} from the queue...")
                needToGetNextCustomer = False
            tempTableID = tableMarker(curCust, tempAvaList)
            if tempTableID != -1:
                tempTable = setTableWaiting(tempTableID)
                table_col_ref.document(str(tempTable.getID())).update({"strState": tempTable.getStatus()})
                print("Update was made")
                needToGetNextCustomer = True
            print("Listening for changes...")
            sleep(10)
        except KeyboardInterrupt:
            break

    # #Old Menu for queue testing. Leaving here for testing purposes.
    # print("Please enter the corrisponding number for the menu selection for testing.")
    # optionNum = int(input("1. Enter in single person information\n2. Enter in multiple people information\n"
    #                       "3. Enter the table information test\n4. Enter the table and cust compare info\n"
    #                       "5. Test the available status list\n6.Enter the table marker test\n"))
    # if optionNum == 1:
    #     testEnterSingle()
    # if optionNum == 2:
    #     testEnterMulti()
    # if optionNum == 3:
    #     testTableStuff()
    # if optionNum == 4:
    #     print("Testing the customer party size checker and the table seat\nFollow the prompts")
    #     cust1Name = input("Enter in customer 1 name\n")
    #     cust1email = "fake@email.com"
    #     cust1PartySize = int(input("Enter customer 1 party size\n"))
    #     cust1 = PerInfo.PersonalInfo(cust1Name, cust1email, cust1PartySize)
    #     print(f"Customer {cust1.getName()} created...")
    #     table1ID = int(input("Enter in table 1 ID\n"))
    #     table1SeatCount = int(input("Enter in table 1 seat count\n"))
    #     table1Status = "Status dont matter"
    #     table1 = TableInfo.TableInfo(table1ID, table1SeatCount, table1Status)
    #     print(f"Table {table1.getID()} created...")
    #     cust2Name = input("Enter in customer 2 name\n")
    #     cust2email = "fake@email.com"
    #     cust2PartySize = int(input("Enter customer 2 party size\n"))
    #     cust2 = PerInfo.PersonalInfo(cust2Name, cust2email, cust2PartySize)
    #     print(f"Customer {cust2.getName()} created...")
    #     table2ID = int(input("Enter in table 2 ID\n"))
    #     table2SeatCount = int(input("Enter in table 2 seat count\n"))
    #     table2Status = "Status dont matter"
    #     table2 = TableInfo.TableInfo(table2ID, table2SeatCount, table2Status)
    #     print(f"Table {table2.getID()} created...")
    #     testCheckCanSit(table1, cust1, table2, cust2)
    # if optionNum == 5:
    #     print(f"Creating 10 tables, 4 are available, 2 is waiting, 2 are In Use, and 2 are Needs Cleaning...")
    #     addTable(1, 1, "Available")
    #     addTable(10, 2, "available")
    #     addTable(6, 3, "available")
    #     addTable(4, 4, "Available")
    #     addTable(5, 5, "In Use")
    #     addTable(3, 6, "in use")
    #     addTable(7, 1, "Waiting")
    #     addTable(8, 2, "waiting")
    #     addTable(9, 3, "Needs Cleaning")
    #     addTable(2, 4, "needs cleaning")
    #     print("Printing table list...")
    #     printTableList()
    #     print("Testing the available table list function")
    #     tempList = allAvailableTableList()
    #     if len(tempList) == 4:
    #         print("Test passed got a list of 4 available tables...")
    #         for table in tempList:
    #             print(f"Table {table.getID()}")
    #     else:
    #         print(f"Test failed the returned list is of size {len(tempList)}\nThe tables within the list are...")
    #         for table in tempList:
    #             print(f"Table {table.getID()}")
    # if optionNum == 6:
    #     print(f"Creating 10 tables, 4 are available, 2 is waiting, 2 are In Use, and 2 are Needs Cleaning...")
    #     addTable(1, 1, "Available")
    #     addTable(10, 2, "available")
    #     addTable(6, 3, "available")
    #     addTable(4, 4, "Available")
    #     addTable(5, 5, "In Use")
    #     addTable(3, 6, "in use")
    #     addTable(7, 1, "Waiting")
    #     addTable(8, 2, "waiting")
    #     addTable(9, 3, "Needs Cleaning")
    #     addTable(2, 4, "needs cleaning")
    #     tempList = allAvailableTableList()
    #     print("Creating customer Bob with an email of bob@email.com and a party size of 2")
    #     tempCust1 = PerInfo.PersonalInfo("Bob", "bob@email.com", 2)
    #     print("Creating customer Charlie with an email of charlie@email.com and a party size of 6")
    #     tempCust2 = PerInfo.PersonalInfo("Charlie", "charlie@email.com", 6)
    #     print("Creating customer Sara with an email of sara@email.com and a party size of 1")
    #     tempCust3 = PerInfo.PersonalInfo("Sara", "sara@email.com", 1)
    #     print("Testing the table marker with Bob, he should match with any table that has a seat cap of 2 or more...")
    #     tempTableID = tableMarker(tempCust1, tempList)
    #     if tempTableID != -1 and tempTableID != 1:
    #         print("The first test was a success")
    #     else:
    #         print("The first test was a failure")
    #     print("Testing the table marker with Charlie, he should not match with any table...")
    #     tempTableID = tableMarker(tempCust2, tempList)
    #     if tempTableID == -1:
    #         print("The second test was a success")
    #     else:
    #         print("The second test was a failure")
    #     print("Testing the table marker with Sara, she should only be matched with with a table that has a set cap of 1, which is only table 1 in the list...")
    #     tempTableID = tableMarker(tempCust3, tempList)
    #     if tempTableID == 1:
    #         print("The third test was a success")
    #     else:
    #         print("The third test was a failure")





    # printQueue()
    # printTableList()

    # A check to make sure can find tables based on an ID
    # testTableListChecker(8)

    cust_col_watch.unsubscribe()
    table_col_watch.unsubscribe()
    print("Exiting")

"""
Causes the main function to run
"""
if __name__ == "__main__":
    main()
