import unittest

import billing_utils
import bill_notice


class HelperModuleTests(unittest.TestCase):
    def test_units_used_subtracts_previous_from_current(self):
        self.assertEqual(billing_utils.units_used(1200, 1350), 150)

    def test_units_used_is_negative_when_meter_goes_backwards(self):
        self.assertEqual(billing_utils.units_used(1500, 1450), -50)

    def test_residential_charge_uses_the_constant(self):
        self.assertEqual(billing_utils.charge_cents(150, "residential"),
                         150 * billing_utils.RESIDENTIAL_RATE)

    def test_business_charge_is_double_the_residential_rate(self):
        self.assertEqual(billing_utils.charge_cents(10, "business"),
                         10 * billing_utils.RESIDENTIAL_RATE * 2)

    def test_unknown_meter_type_raises(self):
        with self.assertRaises(ValueError):
            billing_utils.charge_cents(10, "farm")


class BillNoticeTests(unittest.TestCase):
    def test_ada_residential_notice(self):
        notice = bill_notice.build_notice("ada|1200|1350|30|residential")
        self.assertIn("Customer: ada", notice)
        self.assertIn("Units used: 150", notice)
        expected = 150 * billing_utils.RESIDENTIAL_RATE
        self.assertIn("Charge: " + str(expected) + " cents", notice)
        self.assertNotIn("WARNING", notice)

    def test_bob_backwards_reading_warns_and_has_no_charge(self):
        notice = bill_notice.build_notice("bob|1500|1450|30|business")
        self.assertIn("Customer: bob", notice)
        self.assertIn("WARNING: meter reading went backwards", notice)
        self.assertNotIn("Charge:", notice)

    def test_unknown_meter_type_is_rejected(self):
        notice = bill_notice.build_notice("cy|100|200|30|farm")
        self.assertEqual(notice, "Rejected: unknown meter type 'farm'")

    def test_wrong_number_of_fields_is_rejected(self):
        notice = bill_notice.build_notice("ada|1200|1350")
        self.assertTrue(notice.startswith("Rejected:"))

    def test_non_number_reading_is_rejected(self):
        notice = bill_notice.build_notice("ada|lots|1350|30|residential")
        self.assertTrue(notice.startswith("Rejected:"))

    def test_line_with_windows_line_ending_still_works(self):
        notice = bill_notice.build_notice("ada|1200|1350|30|residential\r\n")
        self.assertIn("Units used: 150", notice)


class ChangingTheRateTests(unittest.TestCase):
    def setUp(self):
        self.saved_rate = billing_utils.RESIDENTIAL_RATE

    def tearDown(self):
        billing_utils.RESIDENTIAL_RATE = self.saved_rate

    def test_notice_follows_a_new_residential_rate(self):
        billing_utils.RESIDENTIAL_RATE = 20
        notice = bill_notice.build_notice("ada|1200|1350|30|residential")
        self.assertIn("Charge: 3000 cents", notice)


if __name__ == "__main__":
    unittest.main()