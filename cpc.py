import tkinter as tk
import requests
import webbrowser
from requests_html import HTMLSession
from tkinter import ttk
from bs4 import BeautifulSoup as bs

class carBuyer:
    def __init__(self):  
        self.firstName = ""
        self.lastName = ""
        self.password = ""
        self.wishlist = []
    
class WebScraper:
    def __init__(self):
        self.request = ""
        self.session = HTMLSession()
        self.trueCar_URL = ""
        self.soup = ""
        self.price = 0
    
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
        carList = []
        for i in range(len(v_years)):
            vehicle = {
                "Year": v_years[i],
                "MakeAndModel": v_makeAndModels,
                "Trim": v_trims[i],
                "Price": v_prices[i]
            }
            carList.append(vehicle)

        print("Cars Information:")
        for vehicle in carList:
            print(vehicle)
        
        return carList
        
class CarPriceChecker:
    def __init__(self, master):
        self.master = master
        self.master.title("Car Price Checker")
        self.master.geometry("1350x1000")

        self.vehicleYear = tk.StringVar(self.master)
        self.vehicleMake = tk.StringVar(self.master)
        self.vehicleModel = tk.StringVar(self.master)
        self.zipCode = tk.StringVar(self.master)
        self.wishlist = []

        self.populateYearDropdown()
        self.populateMakeDropdown()
        self.populateModelDropdown()
        self.populateZipCodeDropdown()
        self.createSearchButton()
        self.createWishlistButton()
        
        self.webScraper = WebScraper()
        
        self.carListbox = tk.Listbox(self.master, height=20, width=120, font=("Helvetica", 12))
        self.carListbox.grid(row=0, column=1, rowspan=4, columnspan=3)
        self.carListbox.bind("<<ListboxSelect>>", self.onCarSelect)
        self.addToWishlist()
        
    def populateZipCodeDropdown(self):
        startZip = 90001
        endZip = 96162
        zipCodes = [str(zipcode) for zipcode in range(startZip, endZip + 1)]

        self.zipcode_dropdown = ttk.Combobox(self.master, textvariable=self.zipCode, values=zipCodes, state="readonly", font=("Helvetica", 12))
        self.zipcode_dropdown.grid(row=0, column=0, padx=10, pady=10)
        self.zipCode.set("Select Zip Code")

    def populateYearDropdown(self):
        startYear = 2023
        endYear = 1990
        years = [year for year in range(startYear, endYear - 1, -1)]

        self.yearDropdown = ttk.Combobox(self.master, textvariable=self.vehicleYear, values=years, state="readonly", font=("Helvetica", 12))
        self.yearDropdown.grid(row=1, column=0, padx=10, pady=10)
        self.vehicleYear.set("Select Year")

    def populateMakeDropdown(self):
        vehicle_makes = ["Audi", "Chevrolet", "Ford", "Honda", "Jeep", "Mercedes Benz", "Porsche", "Subaru", "Toyota", "Volkswagen"]

        self.make_dropdown = ttk.Combobox(self.master, textvariable=self.vehicleMake, values=vehicle_makes, state="readonly", font=("Helvetica", 12))
        self.make_dropdown.grid(row=2, column=0, padx=10, pady=10)
        self.make_dropdown.bind("<<ComboboxSelected>>", self.onMakeSelect)
        self.vehicleMake.set("Select Make")

    def populateModelDropdown(self):
        self.models_dropdown = ttk.Combobox(self.master, textvariable=self.vehicleModel, state="readonly", font=("Helvetica", 12))
        self.models_dropdown.grid(row=3, column=0, padx=10, pady=10)
        self.models_dropdown.set("Select Model")
    
    def createSearchButton(self):
        search_button = tk.Button(self.master, text="Search", command=self.onSearch, font=("Helvetica", 12))
        search_button.grid(row=4, column=0, pady=10)
    
    def createWishlistButton(self):
        wishlistButton = tk.Button(self.master, text="Add to Wishlist", command=self.addToWishlist, font=("Helvetica", 12))
        wishlistButton.grid(row=4,column=2,pady=10)

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

    def displayResults(self, cars):
        # Clear existing content
        self.carListbox.delete(0, tk.END)

        # Display car information with a button to add to wishlist
        for i, car in enumerate(cars):
            car_info = f"Year: {car['Year']}, Make and Model: {car['MakeAndModel']}, Trim: {car['Trim']}, Price: {car['Price']}"
            self.carListbox.insert(tk.END, car_info)

    def addToWishlist(self):
        index = self.carListbox.curselection()
        if index:
            selectedVehicle = self.carListbox.get(index)
            self.wishlist.append(selectedVehicle)
            print(f"Added to Wishlist: {selectedVehicle}")
        else:
            print("Please select a car from the list.")
            
    def onCarSelect(self, carIndex):
        # Get the index of the selected item

            # Perform actions with the selected car information
            print("Selected Car:", carIndex)
    
    def onSearch(self):
        selectedZipCode = self.zipCode.get()
        selectedYear = int(self.vehicleYear.get())
        selectedMake = self.vehicleMake.get()
        selectedModel = self.vehicleModel.get()
        cars = self.webScraper.getTrueCarData(selectedZipCode, selectedYear,selectedMake,selectedModel)
        self.displayResults(cars)


if __name__ == "__main__":
    root = tk.Tk()
    app = CarPriceChecker(root)
    root.mainloop()
    