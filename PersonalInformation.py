"""
This file is for the personal information objects

These objects are made from the information that people will enter
"""


class PersonalInfo(object):
    """
    All personal info objects must contain a name, number, and party size associated with the object.
    These will be given by the submitted data
    """

    def __init__(self, docId, name, email, partySize, pos):
        self.docId = docId
        self.name = name
        self.email = email
        self.partySize = partySize
        self.queuePos = pos

    """
    Simple get function to a return a document id if needed
    """
    def getDocId(self):
        return self.docId
        
    """
    Simple get function to return a name if needed
    """

    def getName(self):
        return self.name

    """
    Simple get function to return a number if needed
    """

    def getEmail(self):
        return self.email

    """
    Simple get function to return party size if needed
    """

    def getPartySize(self):
        return self.partySize

    """
    Simple get function to return queue position if needed
    """
    def getQueuePos(self):
        return self.queuePos

    """
    Display the information of the object to the console
    """

    def printInfo(self):
        print("Name: {}\nEmail: {}\nParty Size {}".format(self.name, self.email, self.partySize))