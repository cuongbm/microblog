import unittest


class PythonLearnTest(unittest.TestCase):
    number2 = 5

    def test_expression(self):
        self.assertTrue(True)

    def test_tuple(self):
        a = (1,2,3,4)
        print(list(a))

    def test_arg(self):
        self.arg_method("test1", "test2", "test3", arg5="test4")

    def arg_method(self, arg1, arg2, *args, **kwargs):
        arg4 = kwargs.pop("arg4", None)
        print(args)
        print(kwargs)