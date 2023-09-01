"""_5781.py

ExcitationSourceSelectionBase
"""


from typing import Optional

from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_EXCITATION_SOURCE_SELECTION_BASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Results', 'ExcitationSourceSelectionBase')


__docformat__ = 'restructuredtext en'
__all__ = ('ExcitationSourceSelectionBase',)


class ExcitationSourceSelectionBase(_0.APIBase):
    """ExcitationSourceSelectionBase

    This is a mastapy class.
    """

    TYPE = _EXCITATION_SOURCE_SELECTION_BASE

    def __init__(self, instance_to_wrap: 'ExcitationSourceSelectionBase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def included(self) -> 'Optional[bool]':
        """Optional[bool]: 'Included' is the original name of this property."""

        temp = self.wrapped.Included

        if temp is None:
            return None

        return temp

    @included.setter
    def included(self, value: 'Optional[bool]'):
        self.wrapped.Included = value

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return ''

        return temp
