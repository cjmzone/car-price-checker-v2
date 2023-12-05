class User:
    def __init__(self):  
        self.firstName = ""
        self.lastName = ""
        self.password = ""
        self.wishlist = []
    
    def add_to_wishlist(self, item):
        self.wishlist.append(item)
        
    def remove_from_wishlist(self, item):
        if item in self.wishlist:
            self.wishlist.remove(item)   
     
    def getWishlist(self):
        return self.wishlist
    