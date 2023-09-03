from bs4 import BeautifulSoup
import json
from urllib.parse import unquote_plus

from ir_client.cars.models import Car, Cars


def map_cars(data) -> Cars:
    car_listing = __get_car_listing(data)
    cars = [map_car(car) for car in car_listing]
    return Cars(cars=cars)


def __get_car_listing(data):
    soup = BeautifulSoup(data, "html.parser")
    script_tags = soup.find_all("script")
    listings_line = next(line for tag in script_tags for line in tag.text.splitlines() if "CarListing" in line)
    return json.loads(listings_line[30:-3])


def map_car(car_data) -> Car:
    return Car(
        id=car_data['id'],
        name=unquote_plus(car_data['name'])
    )
