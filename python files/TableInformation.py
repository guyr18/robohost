"""
This file is for the table information objects

These objects hold information for each table. The included information is the table's ID, number of seats, and status
"""


class TableInfo(object):
    """
    All table objects must contain a table ID, seat count/number, and a status
    """
    def __init__(self, tableID, seatCount, status):
        self.tableID = tableID
        self.seatCount = seatCount
        self.status = status

    """
    Get function that returns id
    """
    def getID(self):
        return self.tableID

    """
    Get function that returns seatcount
    """
    def getSeatCount(self):
        return self.seatCount

    """
    Get function that returns the status of the table object
    """
    def getStatus(self):
        return self.status

    """
    Function to print out information regarding the table
    """
    def printTableInfo(self):
        print(f"Table ID: {self.tableID}\nNumber of Seats at Table: {self.seatCount}\nTable Status: {self.status}")

    """
    A set function to manually the status of a table object to any of the statuses
    
    @param      newStatus       the status that the table should be set to manually
    """
    def updateStatus(self, newStatus):
        self.status = newStatus
        print(f"Status changed to {self.status}")

    """
    Helper function to determine if the table's status is currently available or not
    
    return      True if the status of the table is available, False otherwise
    """
    def isAvailable(self):
        if str(self.status).lower() == "available":
            return True
        return False

    """
    A special set function that will change the status of a table object to Waiting for Customer
    """
    def changeInUse(self):
        self.status = "In Use"

    """
    A function to determine if a person can sit at this table based on if their party size can fit within the table's set count
    
    return      True if the party size is less than or equal to the table's seat count, False otherwise
    """
    def canSit(self, partySize):
        if partySize <= self.seatCount:
            return True
        return False

    """
    A function to check checkID against a table's ID
    @param      checkID     an ID that is to be checked against the tables assigned ID
    Return      bool based on if the IDs match
    """
    def checkID(self, checkID):
        if self.tableID == checkID:
            return True
        return False
