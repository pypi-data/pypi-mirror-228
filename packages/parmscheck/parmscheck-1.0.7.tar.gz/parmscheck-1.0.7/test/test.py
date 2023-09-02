from check import check_args,  check_args_for_class
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Tuple,
    TypeVar,
    Type,
    Literal,
    Union,
    Optional, Generic,Callable)


T = TypeVar('T', int, float, Dict[int, str])
P = TypeVar('P')


@check_args
def test_int(a: int):
    return True


@check_args
def test_float(a: float):
    return True


@check_args
def test_bool(a: bool):
    return True


@check_args
def test_string(a: str):
    return True


@check_args
def test_args(a, *args):
    return True


@check_args
def test_kwargs(a, **kwargs):
    return True


@check_args
def test_list(a: list):
    return True


@check_args
def test_List(a: List[Optional[int]]):
    return True


@check_args
def test_Any(a: Any):
    return True


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


class C(object):
    def __init__(self):
        super(C, self).__init__()


class D(C, B):
    def __init__(self):
        super(D, self).__init__()


class Test_list(tuple):
    def __init__(self, *args):
        super(Test_list, self).__init__(*args)


@check_args
def test_extend(a: A):
    return True


@check_args
def test_Dict(a: Dict[str, List[int]]):
    return True


@check_args
def test_Union(a: Union[int, List[Optional[int]]]):
    return True


@check_args
def test_Tuple(a: Tuple[int or str]):
    return True


@check_args
def test_Literal(a: Literal['1', 2]):
    return True


@check_args
def test_TypeVar(a: T):
    return True


class Mapping(Generic[T, P]):
    @check_args
    def test(self, key: T) -> P:
        return False
@check_args



def test_call(a:Callable):
    return True

class Call_test():
    def __call__():
        return None

if __name__ == '__main__':
    test_int(1)
    try:
        test_int(2.2)
    except DetailedTypeError as e:
        print(e)
    test_float(2.2)
    try:
        test_float(1)
    except DetailedTypeError as e:
        print(e)
    test_bool(True)
    try:
        test_bool('False')
    except DetailedTypeError as e:
        print(e)
    test_string('aaa')
    try:
        test_bool(['a', 'a'])
    except DetailedTypeError as e:
        print(e)
    test_args(1, 2, 3)
    try:
        test_args(1, 2, b=5)
    except TypeError as e:
        print(e)
    test_kwargs(1, b=3, c=5)
    try:
        test_kwargs(1, {'a': 'B'})
    except TypeError as e:
        print(e)

    test_list([1, 2])
    try:
        test_list((1, 2))
    except DetailedTypeError as e:
        print(e)

    test_List([1, 2])
    try:
        test_List((1, 2))
    except DetailedTypeError as e:
        print(e)
    try:
        test_List(['1', 2])
    except DetailedTypeError as e:
        print(e)
    try:
        test_List({1: 2})
    except DetailedTypeError as e:
        print(e)
    try:
        test_List(set([1, 2]))
    except DetailedTypeError as e:
        print(e)
    test_Any(DeprecationWarning)
    test_Any(None)
    test_extend(A())
    test_extend(B())
    try:
        test_extend(C())
    except DetailedTypeError as e:
        print(e)
    test_Dict({'1': [1, 2]})
    try:
        test_Dict({1: 2, 3: 4})
    except DetailedTypeError as e:
        print(e)
    try:
        test_Dict([1, 2])
    except DetailedTypeError as e:
        print(e)
    test_Union(1)
    test_Union([1, None])
    try:
        test_Union(set([1, None]))
    except DetailedTypeError as e:
        print(e)
    test_Tuple((1, '2'))
    try:
        test_Tuple([1, '2'])
    except DetailedTypeError as e:
        print(e)
    test_Literal('1')
    try:
        test_Literal('2')
    except DetailedTypeError as e:
        print(e)
    test_TypeVar(1)
    test_TypeVar(1.1)
    test_TypeVar({1:'2'})
    try:
        test_TypeVar('2')
    except DetailedTypeError as e:
        print(e)
    try:
        test_TypeVar({1:1})
    except DetailedTypeError as e:
        print(e)
    a = A()
    b = B()
    a.func(1)
    try:
        a.func([1,2])
    except DetailedTypeError as e:
        print(e)
    b.func(1,[2])
    try:
        b.func(1,2)
    except DetailedTypeError as e:
        print(e)
    m = Mapping()
    m.test(1)
    try:
        m.test('111')
    except DetailedTypeError as e:
        print(e)
    test_call(Call_test())
    try:
        test_call(1)
    except DetailedTypeError as e:
        print(e)
