import unittest

from decorators.decorators_task import sums_of_str_elements_are_equal

class TaskThirdUnitTest(unittest.TestCase):
    @sums_of_str_elements_are_equal
    def calculate_first(self):
        return "-11 -2"

    @sums_of_str_elements_are_equal
    def calculate_second(self):
        return "1117 -19"

    def test_first_func(self):
        assert self.calculate_first() == "-2 == -2"

    def test_second_func(self):
        assert self.calculate_second() == "10 != -10"


if __name__ == '__main__':
    unittest.main()
