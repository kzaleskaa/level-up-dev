import unittest

from decorators.decorators_task import format_output


class TaskFirstUnitTest(unittest.TestCase):
    @format_output("first_name__last_name")
    def first_func(self):
        return {
            "first_name": "Jan",
            "last_name": "Kowalski"
        }

    @format_output("city")
    def second_func(self):
        return {
            "first_name": "Jan",
            "last_name": "Kowalski"
        }

    @format_output("first_name__last_name", "city")
    def third_func(self):
        return {
            "first_name": "Jan",
            "last_name": "Kowalski",
            "city": ""
        }

    def test_first_func(self):
        assert self.first_func() == {
            "first_name__last_name": "Jan Kowalski"
        }

    def test_second_func(self):
        with self.assertRaises(ValueError):
            self.second_func()

    def test_third_func(self):
        assert self.third_func() == {
            "first_name__last_name": "Jan Kowalski",
            "city": "Empty value"
        }


if __name__ == '__main__':
    unittest.main()
