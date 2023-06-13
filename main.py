from sources import display_dishes
from sources.garden_restaurant import GardenRestaurant

if __name__ == "__main__":
    restaurant = GardenRestaurant()

    print("---lunch--")
    print(display_dishes(restaurant.get_lunch()))
    print("---dinner--")
    print(display_dishes(restaurant.get_dinner()))
