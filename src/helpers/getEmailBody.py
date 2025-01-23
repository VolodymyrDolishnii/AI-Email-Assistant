def getEmailBody(array1, array2):
    for elem1 in array1:
        if array2[0] == elem1[0]:
            return elem1[1]