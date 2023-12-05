import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup as bs
import webbrowser
import requests
from requests_html import HTMLSession

from user import User

class CreateLayout:
    def __init__(self, window):
        self.window = window
        window.title('Car Price Checker')
        window.geometry("1350x900")
        
class WebScraper:
    def __init__(self):
        self.request = ""
        self.session = HTMLSession()
        self.trueCar_URL = ""
        self.soup = ""
        self.price = 0
        self.carList = []
    
    def getTrueCarData(self, zipcode, year, make, model):
        print("Selected Zip Code:", zipcode)
        print("Selected Year:", year)
        print("Selected vehicle make:", make)
        print("Selected vehicle model:", model)
        
        trueCar_URL = "https://www.truecar.com/used-cars-for-sale/listings/" + make.lower() + "/" + model.lower() + "/year-" + str(year) + "/"
        #webbrowser.open(trueCar_URL, new=2)
    
        r = self.session.get(trueCar_URL)
        soup = bs(r.text, 'html.parser')
        
        v_years = [element.text for element in soup.find_all("span", class_="vehicle-card-year text-xs")]
        v_makeAndModels = make + " " + model
        v_trims = [element.text for element in soup.find_all("div", class_="truncate text-xs", attrs={"data-test": "vehicleCardTrim"})]
        v_prices = [element.text for element in soup.find_all("span", {"data-test": "vehicleListingPriceAmount"})]

        # Create a list of dictionaries representing cars
       
        for i in range(len(v_years)):
            vehicle = {
                "Year": v_years[i],
                "MakeAndModel": v_makeAndModels,
                "Trim": v_trims[i],
                "Price": v_prices[i]
            }
            self.carList.append(vehicle)

        print("Cars Information:")
        for vehicle in self.carList:
            print(vehicle)
        
        return self.carList
    
    def getVroomData(self, zipcode, year, make, model):
        vroom_URL = "https://www.vroom.com/cars/" + make.lower() + "/" + model.lower() + "?year=" + str(year) + "&zip=" + str(zipcode)
        # webbrowser.open(vroom_URL, new=2)
        r = self.session.get(vroom_URL)
        soup = bs(r.text, 'html.parser')
        
        
        v_trimAndMiles = [element.text.strip() for element in soup.select('.details-wrap > div > div')]
       
        v_prices = [element.text.strip() for element in soup.find_all('div', attrs={'data-v-2b97cf53': '', 'class': 'price'})]
        
        for i in range(len(v_prices)):
            vehicle = {
                "Year": year,
                "MakeAndModel": make + " " + model,
                "Trim": v_trimAndMiles[i],
                "Price": v_prices[i]
            }
            self.carList.append(vehicle)
        
        print("Vroom Information:")
        for vehicle in self.carList:
            print(vehicle)
        
        return self.carList

    def getautoTempestData(self, zipCode, year, make, model):
        
        autoTempest_URL = "https://www.autotempest.com/results?make=" + make.lower().replace("-", "").replace(" ", "") +"&model="+model.lower().replace("-", "") + "&minyear="+str(year)+"&maxyear="+str(year)
        
        #webbrowser.open(autoTempest_URL, new=2)
        r = self.session.get(autoTempest_URL)
        soup = bs(r.text, 'html.parser')

# class User:
#     def __init__(self):  
#         self.firstName = ""
#         self.lastName = ""
#         self.password = ""
#         self.wishlist = []
    
#     def add_to_wishlist(self, item):
#         self.wishlist.append(item)
        
#     def getWishlist(self):
#         return self.wishlist
   
class PriceChecker(CreateLayout):
    def __init__(self, window, user):
        super().__init__(window)
        # Create a single ttk.Notebook for both tabs
        self.tab_control = ttk.Notebook(window)
        # Tab1
        priceCheckerTab = ttk.Frame(self.tab_control)
        self.tab_control.add(priceCheckerTab, text='Price Checker')

        # Add Tab1-specific widgets and logic here
        ttk.Label(priceCheckerTab, text='Vehicle Value Hub').pack()
        
        self.vehicleYear = tk.StringVar(self.window)
        self.vehicleMake = tk.StringVar(self.window)
        self.vehicleModel = tk.StringVar(self.window)
        self.zipCode = tk.StringVar(self.window)
        
        self.createListBox(priceCheckerTab)
        self.createWishListBox(priceCheckerTab)
        self.populateZipCodeDropdown(priceCheckerTab)
        self.populateYearDropdown(priceCheckerTab)
        self.populateMakeDropdown(priceCheckerTab)
        self.populateModelDropdown(priceCheckerTab)
        self.createSearchButton(priceCheckerTab)
        self.removeFromWL_Button(priceCheckerTab)
        self.removeFromWishlist()
        self.createWishlistButton(priceCheckerTab)
        self.addToWishlist()
        
        self.webScraper = WebScraper()
        self.currentUser = user
        
    def createListBox(self, parent):
        self.carListbox = tk.Listbox(parent, height=20, width=120, font=("Helvetica", 12))
        self.carListbox.pack(side="top", expand="false", padx=20, pady=10,anchor=tk.NE)
    
    def createWishListBox(self, parent):
        self.wishListbox = tk.Listbox(parent, height=20, width=120, font=("Helvetica", 12))
        self.wishListbox.pack(side="right", expand="false", padx=20, pady=40,anchor=tk.NE)
            
    def populateZipCodeDropdown(self, parent):
        startZip = 90001
        endZip = 96162
        zipCodes = [str(zipcode) for zipcode in range(startZip, endZip + 1)]

        self.zipcode_dropdown = ttk.Combobox(parent, textvariable=self.zipCode, values=zipCodes, state="readonly", font=("Helvetica", 12))
        self.zipcode_dropdown.pack(side="top", padx=10, pady=10)
        self.zipCode.set("Select Zip Code")

    def populateYearDropdown(self, parent):
        startYear = 2023
        endYear = 1990
        years = [year for year in range(startYear, endYear - 1, -1)]

        self.yearDropdown = ttk.Combobox(parent, textvariable=self.vehicleYear, values=years, state="readonly", font=("Helvetica", 12))
        self.yearDropdown.pack(side="top",padx=10, pady=10)
        self.vehicleYear.set("Select Year")
    
    def populateMakeDropdown(self,parent):
        vehicle_makes = ["Audi", "Chevrolet", "Ford", "Honda", "Jeep", "Mercedes Benz", "Porsche", "Subaru", "Toyota", "Volkswagen"]

        self.make_dropdown = ttk.Combobox(parent, textvariable=self.vehicleMake, values=vehicle_makes, state="readonly", font=("Helvetica", 12))
        self.make_dropdown.pack(side="top",padx=10, pady=10)
        self.make_dropdown.bind("<<ComboboxSelected>>", self.onMakeSelect)
        self.vehicleMake.set("Select Make")

    def populateModelDropdown(self, parent):
        self.models_dropdown = ttk.Combobox(parent, textvariable=self.vehicleModel, state="readonly", font=("Helvetica", 12))
        self.models_dropdown.pack(side="top",padx=10, pady=10)
        self.models_dropdown.set("Select Model")
    
    def onMakeSelect(self, event):  
        vehicle_models = {
            "Audi": ["A3", "A4", "Q3", "Q4", "R8"],
            "Chevrolet": ["Blazer", "Camaro", "Colorado", "Malibu", "Silverado"],
            "Ford": ["Explorer", "F-150", "Focus", "Mustang", "Ranger"],
            "Honda": ["Accord", "Civic", "CR-V", "Element", "Pilot"],
            "Jeep": ["Cherokee", "Gladiator", "Rubicon", "Wrangler"],
            "Mercedes Benz": ["A-Class", "C-Class", "E-Class", "G-Class", "S-Class"],
            "Porsche": ["911", "Boxster", "Cayenne", "Cayman", "Panamera"],
            "Subaru": ["Ascent", "Crosstrek", "Forester", "Impreza", "Outback"],
            "Toyota": ["Corolla", "Land Cruiser", "Prius", "Rav4", "Tacoma"],
            "Volkswagen": ["Beetle", "Golf", "Jetta", "Passat", "Tiguan"]
        }
        
        selected_make = self.vehicleMake.get()
        self.models_dropdown["values"] = []
        
        if selected_make in vehicle_models:
            self.models_dropdown["values"] = vehicle_models[selected_make]
            self.models_dropdown.set("Select Model")
        else:
            self.models_dropdown.set("No Models")
        
    def createSearchButton(self, parent):
        search_button = tk.Button(parent, text="Search", command=self.onSearch, font=("Helvetica", 12))
        search_button.pack(side="top",padx=10, pady=10)
    
    def createWishlistButton(self, parent):
        wishlistButton = tk.Button(parent, text="Add to Wishlist", command=self.addToWishlist, font=("Helvetica", 12))
        wishlistButton.pack(side="bottom",padx=10, pady=10)

    def removeFromWL_Button(self, parent):
        wishlistButton = tk.Button(parent, text="Remove from Wishlist", command=self.removeFromWishlist, font=("Helvetica", 12))
        wishlistButton.pack(side="bottom",padx=10, pady=10)
    
    def addToWishlist(self):
        index = self.carListbox.curselection()
        if index:
            selectedVehicle = self.carListbox.get(index)
            self.currentUser.add_to_wishlist(selectedVehicle)
            print(f"Added to Wishlist: {selectedVehicle}")
            self.displayWishlist()
        else:
            print("Please select a car from the list.")
            
    def removeFromWishlist(self):
        index = self.wishListbox.curselection()
        if index:
            selectedVehicle = self.wishListbox.get(index)
            self.currentUser.remove_from_wishlist(selectedVehicle)
            print(f"Removed from Wishlist: {selectedVehicle}")
            self.displayWishlist()
        else:
            print("Please select a car from the list.")
            
    def displayWishlist(self,):
        # Get the wishlist from currentUser
        self.wishListbox.delete(0, tk.END)
        wishlist = self.currentUser.getWishlist()

        # Add each item from the wishlist to the Listbox
        for item in wishlist:
            self.wishListbox.insert(tk.END, item)

    def onSearch(self):
        selectedZipCode = self.zipCode.get()
        selectedYear = int(self.vehicleYear.get())
        selectedMake = self.vehicleMake.get()
        selectedModel = self.vehicleModel.get()
        
        truecar_data = self.webScraper.getTrueCarData(selectedZipCode, selectedYear,selectedMake,selectedModel)
        vroom_data = self.webScraper.getVroomData(selectedZipCode, selectedYear, selectedMake, selectedModel)
        # autoTempest_data = self.webScraper.getautoTempestData(selectedZipCode, selectedYear, selectedMake, selectedModel)
        
        self.displaySearchResults(truecar_data)
        self.displaySearchResults(vroom_data)
        
    def displaySearchResults(self, cars):
        # Clear existing content
        self.carListbox.delete(0, tk.END)

        # Display car information with a button to add to wishlist
        for i, car in enumerate(cars):
            car_info = f"Year: {car['Year']}, Make and Model: {car['MakeAndModel']}, Trim: {car['Trim']}, Price: {car['Price']}"
            self.carListbox.insert(tk.END, car_info)
                
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

class History(CreateLayout):
    def __init__(self, window, user):
        super().__init__(window)
        # Use the same tab_control created in Tab1
        self.tab_control = priceChecker.tab_control
        historyTab      = ttk.Frame(self.tab_control)
        self.tab_control.add(historyTab, text='     History     ')
        # Add Tab2-specific widgets and logic here
        ttk.Label(historyTab, text='Your History >.<').pack()
        self.currentUser = user
        
if __name__ == "__main__":  
    root = tk.Tk()
    user = User()
    priceChecker = PriceChecker(root, user)
    wishlist = Wishlist(root, priceChecker.currentUser)
    history = History(root, priceChecker.currentUser)

    # Pack the tab_control to display the tabs
    priceChecker.tab_control.pack(expand=1, fill="both")
    root.mainloop()