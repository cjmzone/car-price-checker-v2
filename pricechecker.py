from createlayout import CreateLayout
from webscraper import WebScraper

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
        self.populateZipCodeDropdown(priceCheckerTab)
        self.populateYearDropdown(priceCheckerTab)
        self.populateMakeDropdown(priceCheckerTab)
        self.populateModelDropdown(priceCheckerTab)
        self.createSearchButton(priceCheckerTab)
        self.createWishlistButton(priceCheckerTab)
        self.addToWishlist()
        
        self.webScraper = WebScraper()
        self.currentUser = user
        
    def createListBox(self, parent):
        self.carListbox = tk.Listbox(parent, height=20, width=120, font=("Helvetica", 12))
        self.carListbox.pack(side="right", expand="false",padx=20, pady=100,anchor=tk.NE)
        #self.carListbox.bind("<<ListboxSelect>>", self.onCarSelect)
        
    def populateZipCodeDropdown(self, parent):
        startZip = 90001
        endZip = 96162
        zipCodes = [str(zipcode) for zipcode in range(startZip, endZip + 1)]

        self.zipcode_dropdown = ttk.Combobox(parent, textvariable=self.zipCode, values=zipCodes, state="readonly", font=("Helvetica", 12))
        self.zipcode_dropdown.pack(side="top",padx=10, pady=10)
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

    def addToWishlist(self):
        index = self.carListbox.curselection()
        if index:
            selectedVehicle = self.carListbox.get(index)
            self.currentUser.add_to_wishlist(selectedVehicle)
            print(f"Added to Wishlist: {selectedVehicle}")
            self.displayWishlist()
        else:
            print("Please select a car from the list.")
            
    def displayWishlist(self):
        wl = self.currentUser.getWishlist()
        print("Current Wishlist:", wl)
        # for item in wl:
        #     print("Wishlist: ", item)

    def onSearch(self):
        selectedZipCode = self.zipCode.get()
        selectedYear = int(self.vehicleYear.get())
        selectedMake = self.vehicleMake.get()
        selectedModel = self.vehicleModel.get()
        cars = self.webScraper.getTrueCarData(selectedZipCode, selectedYear,selectedMake,selectedModel)
        self.displaySearchResults(cars)
    
    def displaySearchResults(self, cars):
        # Clear existing content
        self.carListbox.delete(0, tk.END)

        # Display car information with a button to add to wishlist
        for i, car in enumerate(cars):
            car_info = f"Year: {car['Year']}, Make and Model: {car['MakeAndModel']}, Trim: {car['Trim']}, Price: {car['Price']}"
            self.carListbox.insert(tk.END, car_info)
 