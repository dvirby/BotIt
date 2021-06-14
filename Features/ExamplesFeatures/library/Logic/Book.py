class Book:
    def __init__(self, nameBook, numOfCopies, author, listOfBorrow, row):
        self.author = author
        self.row = row
        self.numOfCopies = numOfCopies
        self.nameBook = nameBook
        self.listOfBorrow = listOfBorrow
