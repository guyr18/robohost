"""
This file is for the personal information objects

These objects are made from the information that people will enter
"""

class PersonalInfo(object):

    """
    All personal info objects must contain a name, number, and party size associated with the object.
    These will be given by the submitted data
    """
    def __init__(self, name, number, partySize):
        self.name = name
        self.number = number
        self.partySize = partySize

    """
    Simple get function to return a name if needed
    """
    def getName(self):
        return self.name

    """
    Simple get function to return a number if needed
    """
    def getNumber(self):
        return self.number

    """
    Simple get function to return party size if needed
    """
    def getPartySize(self):
        return self.partySize

    """
    Display the information of the object to the console
    """
    def printInfo(self):
        print("Name: {}\nNumber: {}\nParty Size {}".format(self.name, self.number, self.partySize))
