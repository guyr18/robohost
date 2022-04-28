from queue import Queue
from PersonalInformation import PersonalInfo as PersonalInformation

"""
ComputeWaitTime(Q) takes a queue.Queue object that is assumed to contain 
an arbritrary number of PersonalInformation objects as input. It returns
the corresponding wait time (in minutes as an integer).

"""
def computeWaitTime(Q):

    # Queue is empty; return wait time of zero.
    if Q.qsize() == 0:
        return 0

    # Queue only has one element; return 10 if
    # the party size is >= 5 and 5 otherwise.
    if Q.qsize() == 1:
        return 5 if Q.queue[Q.qsize() - 1].getPartySize() < 5 else 10

    # Queue has between 2 and 5 elements (inclusively);
    # Return 10 if the party size is < 5 and 20 otherwise.
    if Q.qsize() >= 2 and Q.qsize() <= 5:
        return 10 if Q.queue[Q.qsize() - 1].getPartySize() < 5 else 20

    divisibleByFive = Q.qsize() % 5 == 0
    t = Q.qsize() * 5
    mins =  t if divisibleByFive else t - 5
    return mins if Q.queue[Q.qsize() - 1].getPartySize() < 5 else mins + 10