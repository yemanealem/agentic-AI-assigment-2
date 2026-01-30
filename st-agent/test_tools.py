import unittest
from tool_implementation import get_time, calc, lookup_faq

class TestTools(unittest.TestCase):

    # -----------------------------
    # Test get_time
    # -----------------------------
    def test_get_time_valid(self):
        result = get_time("Cape Town")
        self.assertIn("time", result)
        self.assertEqual(result["location"], "Cape Town")

    def test_get_time_invalid(self):
        result = get_time("Paris")
        self.assertIn("error", result)

    # -----------------------------
    # Test calc
    # -----------------------------
    def test_calc_valid(self):
        result = calc("2 + 3 * 5")
        self.assertEqual(result["result"], 17)

    def test_calc_invalid(self):
        result = calc("2 +")
        self.assertIn("error", result)

    # -----------------------------
    # Test lookup_faq
    # -----------------------------
    def test_lookup_faq_found(self):
        result = lookup_faq("forgot password")
        self.assertEqual(result["answer"], "Click 'Forgot Password'.")
    
    def test_lookup_faq_not_found(self):
        result = lookup_faq("how to fly?")
        self.assertEqual(result["answer"], "Sorry, no matching FAQ was found.")

if __name__ == "__main__":
    unittest.main()
