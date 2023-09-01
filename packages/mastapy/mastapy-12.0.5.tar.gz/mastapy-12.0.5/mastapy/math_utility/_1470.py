"""_1470.py

DegreeOfFreedom
"""


from enum import Enum

from mastapy._internal.python_net import python_net_import

_DEGREE_OF_FREEDOM = python_net_import('SMT.MastaAPI.MathUtility', 'DegreeOfFreedom')


__docformat__ = 'restructuredtext en'
__all__ = ('DegreeOfFreedom',)


class DegreeOfFreedom(Enum):
    """DegreeOfFreedom

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls):
        return _DEGREE_OF_FREEDOM

    X = 0
    Y = 1
    Z = 2
    ΘX = 3
    ΘY = 4
    ΘZ = 5


def __enum_setattr(self, attr, value):
    raise AttributeError('Cannot set the attributes of an Enum.') from None


def __enum_delattr(self, attr):
    raise AttributeError('Cannot delete the attributes of an Enum.') from None


DegreeOfFreedom.__setattr__ = __enum_setattr
DegreeOfFreedom.__delattr__ = __enum_delattr
