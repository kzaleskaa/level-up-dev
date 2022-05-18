import unittest

from decorators.decorators_task import add_method_to_instance

class TempClass:
    pass

@add_method_to_instance(TempClass)
def func():
    return "Hello"

class TaskFourthUnitTest(unittest.TestCase):
    def test_method(self):
        self.assertEqual(TempClass().func(), func())

if __name__ == '__main__':
    unittest.main()
