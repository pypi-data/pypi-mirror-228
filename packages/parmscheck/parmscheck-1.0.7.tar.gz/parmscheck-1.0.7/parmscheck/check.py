from functools import wraps
import inspect
import typing
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Tuple,
    TypeVar,
    Type,
    Literal,
    Union)


def check_args(func):
    """
    The decorator that checks types at runtime in a function.
    """

    @wraps(func)
    def check(*args, **kwargs):
        sig = inspect.signature(func)
        binding = None
        try:
            binding = sig.bind(*args, **kwargs)
        except TypeError as te:
            raise DetailedTypeError(
                [Description(func.__name__, f'a TypeError is raised: {te}')])
        errors = []
        for name, value in binding.arguments.items():
            if not check_type(value, sig.parameters[name].annotation):
                errors.append(Description(
                    func.__name__, f'the type of variable "{name}" is not {sig.parameters[name].annotation}. Instead, it is {type(value)}'))
        if errors:
            raise DetailedTypeError(errors)
        return func(*args, **kwargs)
    return check


def check_args_for_class(cls):
    """
    The decorator that checks types at runtime for a class
    
    """
    for name, method in inspect.getmembers(cls):
        if (not inspect.ismethod(method) and not inspect.isfunction(method)) or inspect.isbuiltin(method):
            continue
        if method.__name__ == '__init__':
            continue
        setattr(cls, name, check_args(method))
    return cls


def check_type(obj: Any,
               candidate_type: Any,
               reltype: str = 'invariant'):
    '''
    Args:
        obj (Any): The value to check.
        candidate_type (Any): The type to check the object against.
        reltype (:obj:`str`, optional): Variance of the type.
    Returns:
        bool: True if the type is fine, False otherwise
    '''
    assert reltype in ['invariant', 'covariant',
                       'contravariant'], f' Variadic type {reltype} is unknown'
    # print(type(candidate_type))

    if candidate_type == inspect._empty:
        return True

    if type(candidate_type) == type and reltype in ['invariant']:
        return isinstance(obj, candidate_type)

    if type(candidate_type) == type and reltype in ['covariant']:
        return issubclass(obj.__class__, candidate_type)

    if type(candidate_type) == type and reltype in ['contravariant']:
        return issubclass(candidate_type, obj.__class__)

    if type(candidate_type) == TypeVar:
        if not candidate_type.__constraints__:
            return True
        if not (candidate_type.__covariant__ or candidate_type.__contravariant__):
            return any(check_type(obj, t) for t in candidate_type.__constraints__)

    # if type(candidate_type) == type(Type):
    #     return check_type(obj, candidate_type.__args__[0], reltype='covariant')

    if inspect.isclass(candidate_type) and reltype in ['invariant']:
        return isinstance(obj, candidate_type)

    if type(candidate_type) == typing._SpecialForm:
        if candidate_type._name == 'Any':
            return True
    elif type(candidate_type) == typing._GenericAlias:
        # print(candidate_type._name)
        if candidate_type._name == 'Union':
            return any(check_type(obj, t, reltype) for t in candidate_type.__args__)

        elif candidate_type._name == 'Dict':
            if not hasattr(obj, 'keys'):
                return False
            if not hasattr(obj, 'values'):
                return False
            if not hasattr(obj, 'items'):
                return False
            if type(obj) in [dict]:
                return all(check_type(k, candidate_type.__args__[0], reltype)
                           and check_type(v, candidate_type.__args__[1], reltype)
                           for (k, v) in obj.items())

        elif candidate_type._name == 'List':
            if not hasattr(obj, 'sort'):
                return False
            return all(check_type(o, candidate_type.__args__[0], reltype) for o in obj)

        elif candidate_type._name == 'Set':
            if not hasattr(obj, '__or__'):
                return False
            return all(check_type(o, candidate_type.__args__[0], reltype) for o in obj)

        elif candidate_type._name == 'Sized':
            if not hasattr(obj, '__len__'):
                return False
            return True

        elif candidate_type._name == 'Tuple':
            if hasattr(obj, '__setitem__'):
                return False
            if hasattr(obj, '__delitem__'):
                return False
            return all(check_type(o, t, reltype) for (o, t) in zip(obj, candidate_type.__args__))

        elif candidate_type._name == 'Sequence':
            if not hasattr(obj, '__len__'):
                return False
            return all(check_type(o, candidate_type.__args__[0], reltype) for o in obj)

        elif candidate_type._name is None:
            if candidate_type.__origin__ == typing.Generic:
                return all(check_type(o, t, reltype) for (o, t) in zip(obj, candidate_type.__args__))
            if candidate_type.__origin__ == Union:
                return any(check_type(obj, t, reltype) for t in candidate_type.__args__)
            if candidate_type.__origin__ == Literal:
                return obj in candidate_type.__args__

    elif type(candidate_type) == typing._VariadicGenericAlias:
        if candidate_type._name == 'Callable':
            if not hasattr(obj, '__call__'):
                return False
            return True
    #     return obj in candidate_type.__args__

    # elif type(candidate_type) == typing._UnionGenericAlias:
    #     return any(check_type(obj, t, reltype) for t in candidate_type.__args__)

    return False


class Description(NamedTuple):
    """Represents single type mismatch"""
    func_name: str
    message: str

    def __repr__(self) -> str:
        return f'in function {self.func_name}(),{self.message}'


class DetailedTypeError(TypeError):
    """Error for more detailed info about type mismatches"""
    issues = []

    def __init__(self, issues: List[Description]):
        self.issues = issues
        super().__init__(f'typing issues found:{issues}')

    def __str__(self):
        return '\n'.join(str(i) for i in self.issues)

    def __iter__(self):
        return (x for x in self.issues)

    def __len__(self):
        return len(self.issues)
