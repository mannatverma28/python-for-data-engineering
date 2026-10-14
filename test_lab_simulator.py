import io
import unittest
from contextlib import redirect_stdout

from lab_simulator import (Beaker, Burner, Chemical, Equipment, Scale,
                           check_safety, make_equipment, parse_chemical,
                           run_experiment)


def captured(func, *args):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        result = func(*args)
    return result, buffer.getvalue()


class TestEquipment(unittest.TestCase):
    def test_base_use(self):
        _, out = captured(Equipment("Funnel").use)
        self.assertEqual(out, "Using the Funnel.\n")

    def test_subclasses_override_use(self):
        _, out = captured(Beaker("Beaker").use)
        self.assertEqual(out, "Pouring the chemicals into the Beaker.\n")
        _, out = captured(Burner("Burner").use)
        self.assertEqual(out, "Lighting the Burner and heating the mixture.\n")
        _, out = captured(Scale("Scale").use)
        self.assertEqual(out, "Weighing the chemicals on the Scale.\n")

    def test_subclass_is_equipment(self):
        self.assertIsInstance(Burner("Burner"), Equipment)

    def test_make_equipment_picks_class(self):
        self.assertIsInstance(make_equipment(" beaker "), Beaker)
        self.assertEqual(make_equipment(" beaker ").name, "beaker")
        self.assertIsInstance(make_equipment("BURNER"), Burner)
        self.assertIsInstance(make_equipment("Scale"), Scale)
        funnel = make_equipment("Funnel")
        self.assertIs(type(funnel), Equipment)


class TestChemical(unittest.TestCase):
    def test_parse(self):
        chemical = parse_chemical(" Water (1) ")
        self.assertEqual(chemical.name, "Water")
        self.assertEqual(chemical.hazard_level, 1)

    def test_parse_name_with_brackets(self):
        chemical = parse_chemical("Copper (II) sulfate (3)")
        self.assertEqual(chemical.name, "Copper (II) sulfate")
        self.assertEqual(chemical.hazard_level, 3)

    def test_parse_bad_format(self):
        with self.assertRaises(ValueError):
            parse_chemical("Water")

    def test_hazard_out_of_range(self):
        with self.assertRaises(ValueError):
            Chemical("Mystery", 6)
        with self.assertRaises(ValueError):
            Chemical("Mystery", 0)


class TestSafety(unittest.TestCase):
    def test_example_is_safe(self):
        chemicals = [Chemical("Water", 1), Chemical("Salt", 2)]
        equipment = [Beaker("Beaker")]
        safe, out = captured(run_experiment, chemicals, equipment, False)
        self.assertTrue(safe)
        self.assertEqual(out, "--- Experiment steps ---\n"
                              "Pouring the chemicals into the Beaker.\n"
                              "Experiment is safe to run.\n")

    def test_hazard_level_three_is_allowed(self):
        self.assertEqual(check_safety([Chemical("Vinegar", 3)], [Beaker("Beaker")], False), [])

    def test_hazard_level_four_is_unsafe(self):
        problems = check_safety([Chemical("Acid", 4)], [Beaker("Beaker")], False)
        self.assertEqual(problems, ["Acid is too hazardous (level 4)."])

    def test_missing_beaker(self):
        problems = check_safety([Chemical("Water", 1)], [Scale("Scale")], False)
        self.assertEqual(problems, ["A beaker is required."])

    def test_heating_without_burner(self):
        problems = check_safety([Chemical("Water", 1)], [Beaker("Beaker")], True)
        self.assertEqual(problems, ["Heating needs a burner."])

    def test_heating_with_burner(self):
        equipment = [Beaker("Beaker"), Burner("Burner")]
        self.assertEqual(check_safety([Chemical("Water", 1)], equipment, True), [])

    def test_unsafe_still_prints_steps_in_order(self):
        equipment = [Scale("Scale"), Beaker("Beaker")]
        safe, out = captured(run_experiment, [Chemical("Acid", 5)], equipment, True)
        self.assertFalse(safe)
        self.assertEqual(out, "--- Experiment steps ---\n"
                              "Weighing the chemicals on the Scale.\n"
                              "Pouring the chemicals into the Beaker.\n"
                              "Problem: Acid is too hazardous (level 5).\n"
                              "Problem: Heating needs a burner.\n"
                              "Experiment is unsafe to run.\n")


if __name__ == "__main__":
    unittest.main()