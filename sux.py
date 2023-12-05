class User:
    def __init__(self):
        self.array = [3]

    def appendArray(self, item):
        self.array.append(item)

    def getArray(self):
        return self.array

class PriceCheck:
    def __init__(self, user):
        self.currentUser = user
        self.wishlist = Wishlist(self.currentUser)

    def addArr(self):
        self.currentUser.appendArray(4)

class Wishlist:
    def __init__(self, user):
        self.currentUser = user

    def display(self):
        items = self.currentUser.getArray()
        for i in items:
            print(i)

if __name__ == "__main__":
    user = User()
    priceCheck = PriceCheck(user)

    # Add an item to the array through PriceCheck
    priceCheck.addArr()

    # Display the array from Wishlist
    priceCheck.wishlist.display()
    
    