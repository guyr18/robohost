
# [1, 2, 3, 5, 6, 7]
def findMissingX(L):

    n = len(L)

    for i in range(1, n):
        if L[i] - L[i - 1] != 1:
            return L[i - 1] + 1

    return -1

print(findMissingX([1, 2, 3, 5, 6, 7]))
