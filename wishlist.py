from pricechecker import CreateLayout
from pricechecker import PriceChecker                

class Wishlist(CreateLayout):
    def __init__(self, window, user):
        super().__init__(window)
        # Use the same tab_control created in Tab1
        self.tab_control = priceChecker.tab_control
        wishlistTab      = ttk.Frame(self.tab_control)
        self.tab_control.add(wishlistTab, text='     Wishlist     ')
        # Add Tab2-specific widgets and logic here
        ttk.Label(wishlistTab, text='Your favs >.<').pack()
        self.currentUser = user
        self.createWishListBox(wishlistTab)    
        
    def createWishListBox(self, parent):
        self.wishListbox = tk.Listbox(parent, height=20, width=120, font=("Helvetica", 12))
        self.wishListbox.pack(side="right", expand="false",padx=20, pady=100,anchor=tk.NE)
        #self.carListbox.bind("<<ListboxSelect>>", self.onCarSelect)
    
    def displayWL(self):
        # Clear existing content
        # self.wishListbox.delete(0, tk.END)
        wl = self.currentUser.getWishlist()
        print("WIISSHHH: ", wl)

        # Display car information with a button to add to wishlist
        for i, car in enumerate(wl):
            car_info = f"Year: {car['Year']}, Make and Model: {car['MakeAndModel']}, Trim: {car['Trim']}, Price: {car['Price']}"
            self.wishListbox.insert(tk.END, car_info)
  