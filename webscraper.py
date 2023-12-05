import webbrowser
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs

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