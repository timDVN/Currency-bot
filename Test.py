import unittest
from main import checking_command_currency_input


class TestInputChecker(unittest.TestCase):
    def setUp(self):
        self.message = "/rate USD"
        self.waited_res = False
        self.function = checking_command_currency_input

    def test(self):
        self.assertEqual(self.function(self.message), self.waited_res)


if __name__ == '__main__':
    unittest.main()
