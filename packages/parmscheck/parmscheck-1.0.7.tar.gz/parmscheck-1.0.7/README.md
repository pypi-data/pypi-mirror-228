# parmscheck

#### Introduction:

A decorator that supports type checking for Python functions provides a convenient way to perform runtime type checking on function parameters. By using this decorator, developers can easily ensure that the input parameters of a function are of the expected types.

#### Features:

- Easy to use: Just apply a decorator to the function, and any function can be type-checked. No complex configuration or additional code is required.
- Supports type annotations: The decorator seamlessly integrates with Python's type annotations. Developers can easily add type annotations to the parameters of a function, and the decorator will automatically validate the types of the arguments at runtime.

#### Installation Guide:

Certainly! To install the decorator library using the Python package management tool `pip`：
`pip install parmscheck`

Instructions for Use:

```
from parmscheck import check_args,check_args_for_class

T = TypeVar('T', int, float, Dict[int, str])
P = TypeVar('P')
@check_args
def multiply(a: List[int], b: T) -> int:
    return a * b

result = multiply([2], 3)  # Running Successfully
result = multiply([2.5], (1,2))  # Throwing a TypeError Exception Due to Type Mismatch

@check_args_for_class
class A(object):
    def __init__(self):
        super(A, self).__init__()

    def func(self, a: T):
        return a


@check_args_for_class
class B(A):
    def __init__(self):
        super(B, self).__init__()

    def func(self, a: T, b: List[int]):
        return a

a = A()
b = B()
a.func(1)    # Running Successfully
a.func([1,2])    # Throwing a TypeError Exception Due to Type Mismatc
b.func(1,[2])    # Running Successfully
b.func(1,2)    # Throwing a TypeError Exception Due to Type Mismatc
   

```
