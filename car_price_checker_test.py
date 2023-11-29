import requests
from bs4 import BeautifulSoup

def main():
    while True:
        print("-" * 50)
        print("Top Popular Categories for Cars.Com:")
        print("1. Tesla Model 3")
        print("2. Tesla Model S")
        print("3. Nissan Leaf")
        print("4. Tesla Model Y")
        print("5. Ford Mustang Mach-E")
        print("6. Ford F-150 Lightning")
        print("7. BMW i3")
        print("8. Porsche Taycan")
        print("9. Volkswagen ID.4")
        print("Q. Quit")
        print("-" * 50)
        user_in = input("Enter the number of the car you want to check prices for on Cars.com (1-9), or 'Q' to quit: ").strip()
        if user_in == '1':
            scrape_car_prices('https://www.cars.com/shopping/all/tesla-model_3/')
        elif user_in == '2':
            scrape_car_prices('https://www.cars.com/shopping/all/tesla-model_s/')
        elif user_in == '3':
            scrape_car_prices('https://www.cars.com/shopping/all/nissan-leaf/')
        elif user_in == '4':
            scrape_car_prices('https://www.cars.com/shopping/all/tesla-model_y/')
        elif user_in == '5':
            scrape_car_prices('https://www.cars.com/shopping/all/ford-mustang_mach_e/')
        elif user_in == '6':
            scrape_car_prices('https://www.cars.com/shopping/all/ford-f_150_lightning/')
        elif user_in == '7':
            scrape_car_prices('https://www.cars.com/shopping/all/bmw-i3/')             
        elif user_in == '8':
            scrape_car_prices('https://www.cars.com/shopping/all/porsche-taycan/')
        elif user_in == '9':
            scrape_car_prices('https://www.cars.com/shopping/all/volkswagen-id.4/')                                                                   
        elif user_in.upper() == 'Q':
            break
        else:
            print("Invalid selection.  Please try again.\n")

def scrape_car_prices(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    prices = soup.select('.primary-price')
    carnames = soup.select('h2.title')

    cars = [{'name': carname.text.strip(), 'price': price.text.strip()} for carname, price in zip(carnames, prices)]
    sorted_cars = sorted(cars, key=lambda x: string2float(x['price']))
    for car in sorted_cars:
        print(f"Car Name: {car['name']}\nCar Price: {car['price']}\n")

def string2float(value):
    try:
        return float(value.replace('$', '').replace(',', ''))
    except ValueError:
        return float('inf')
    
if __name__ == "__main__":
    main()