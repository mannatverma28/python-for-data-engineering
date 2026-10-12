def days_until_watering(last_watered, interval):
    # last_watered = how many days ago the plant was watered (today is day 0).
    # The schedule repeats every `interval` days, so we use the remainder.
    # An interval of 0 raises ZeroDivisionError here, on purpose.
    return interval - last_watered % interval


def water_all(plants):
    for plant in plants:
        name = plant["name"]
        try:
            days = days_until_watering(plant["last_watered"], plant["interval"])
            print("Water " + name + " in " + str(days) + " days.")
        except ZeroDivisionError:
            print("Cannot calculate watering for " + name + ": interval cannot be zero.")


def ask_for_plant():
    name = input("Plant name: ")
    text = input("Watering interval in days: ")
    try:
        interval = int(text)
    except ValueError:
        print("Invalid interval")
        return None
    return {"name": name, "last_watered": 0, "interval": interval}


sample_plants = [
    {"name": "Tomato", "last_watered": 2, "interval": 5},
    {"name": "Basil", "last_watered": 1, "interval": 2},
    {"name": "Cactus", "last_watered": 3, "interval": 0},
]

if __name__ == "__main__":
    print("Tomato needs water in " + str(days_until_watering(2, 5)) + " days.")
    water_all(sample_plants)
    new_plant = ask_for_plant()
    if new_plant is not None:
        water_all([new_plant])