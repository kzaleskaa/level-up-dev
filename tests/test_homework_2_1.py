import unittest

from decorators.decorators_task import greeter

class TaskFirstUnitTest(unittest.TestCase):
    @greeter
    def first_func(self):
        return "user"

    @greeter
    def second_func(self):
        return "NEW USER"

    def test_first_func(self):
        assert self.first_func() == "Aloha User"

    def test_second_func(self):
        assert self.second_func() == "Aloha New User"

if __name__ == '__main__':
    unittest.main()
