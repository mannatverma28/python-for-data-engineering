class Equipment:
    def __init__(self, name):
        self.name = name

    def use(self):
        print("Using the " + self.name + ".")


class Beaker(Equipment):
    def use(self):
        print("Pouring the chemicals into the " + self.name + ".")


class Burner(Equipment):
    def use(self):
        print("Lighting the " + self.name + " and heating the mixture.")


class Scale(Equipment):
    def use(self):
        print("Weighing the chemicals on the " + self.name + ".")


class Chemical:
    def __init__(self, name, hazard_level):
        if hazard_level < 1 or hazard_level > 5:
            raise ValueError("Hazard level must be from 1 to 5: " + name)
        self.name = name
        self.hazard_level = hazard_level


def parse_chemical(text):
    # "Water (1)" -> Chemical("Water", 1)
    text = text.strip()
    if not text.endswith(")") or "(" not in text:
        raise ValueError("Write a chemical like Water (1): " + text)
    name, level = text[:-1].rsplit("(", 1)
    return Chemical(name.strip(), int(level))


def make_equipment(name):
    name = name.strip()
    kinds = {"beaker": Beaker, "burner": Burner, "scale": Scale}
    kind = kinds.get(name.lower(), Equipment)
    return kind(name)


def check_safety(chemicals, equipment, heating):
    problems = []
    for chemical in chemicals:
        if chemical.hazard_level > 3:
            problems.append(chemical.name + " is too hazardous (level "
                            + str(chemical.hazard_level) + ").")
    if not any(isinstance(item, Beaker) for item in equipment):
        problems.append("A beaker is required.")
    if heating and not any(isinstance(item, Burner) for item in equipment):
        problems.append("Heating needs a burner.")
    return problems


def run_experiment(chemicals, equipment, heating):
    print("--- Experiment steps ---")
    for item in equipment:
        item.use()
    problems = check_safety(chemicals, equipment, heating)
    for problem in problems:
        print("Problem: " + problem)
    if problems:
        print("Experiment is unsafe to run.")
    else:
        print("Experiment is safe to run.")
    return not problems


def main():
    chemical_text = input("Chemicals (comma-separated, e.g. Water (1), Salt (2)): ")
    equipment_text = input("Equipment (comma-separated, e.g. Beaker, Scale): ")
    heating_text = input("Heating step? (yes/no): ")
    chemicals = [parse_chemical(part) for part in chemical_text.split(",") if part.strip()]
    equipment = [make_equipment(part) for part in equipment_text.split(",") if part.strip()]
    heating = heating_text.strip().lower() == "yes"
    run_experiment(chemicals, equipment, heating)


if __name__ == "__main__":
    main()
    
# This module simulates laboratory experiment steps and safety checks.