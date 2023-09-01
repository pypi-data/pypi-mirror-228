"""_4604.py

MultipleExcitationsSpeedRangeOption
"""


from enum import Enum

from mastapy._internal.python_net import python_net_import

_MULTIPLE_EXCITATIONS_SPEED_RANGE_OPTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'MultipleExcitationsSpeedRangeOption')


__docformat__ = 'restructuredtext en'
__all__ = ('MultipleExcitationsSpeedRangeOption',)


class MultipleExcitationsSpeedRangeOption(Enum):
    """MultipleExcitationsSpeedRangeOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls):
        return _MULTIPLE_EXCITATIONS_SPEED_RANGE_OPTION

    INTERSECTION_OF_SPEED_RANGES = 0
    UNION_OF_SPEED_RANGES = 1


def __enum_setattr(self, attr, value):
    raise AttributeError('Cannot set the attributes of an Enum.') from None


def __enum_delattr(self, attr):
    raise AttributeError('Cannot delete the attributes of an Enum.') from None


MultipleExcitationsSpeedRangeOption.__setattr__ = __enum_setattr
MultipleExcitationsSpeedRangeOption.__delattr__ = __enum_delattr
