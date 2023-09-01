"""_2572.py

BearingDetailSelection
"""


from typing import Optional, List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bearings.bearing_results import _1924
from mastapy.system_model.part_model import _2398, _2397
from mastapy.system_model.part_model.configurations import _2574
from mastapy.bearings.bearing_designs import _2092
from mastapy._internal.python_net import python_net_import

_BEARING_DETAIL_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'BearingDetailSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingDetailSelection',)


class BearingDetailSelection(_2574.PartDetailSelection['_2397.Bearing', '_2092.BearingDesign']):
    """BearingDetailSelection

    This is a mastapy class.
    """

    TYPE = _BEARING_DETAIL_SELECTION

    def __init__(self, instance_to_wrap: 'BearingDetailSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def inner_offset(self) -> 'Optional[float]':
        """Optional[float]: 'InnerOffset' is the original name of this property."""

        temp = self.wrapped.InnerOffset

        if temp is None:
            return None

        return temp

    @inner_offset.setter
    def inner_offset(self, value: 'Optional[float]'):
        self.wrapped.InnerOffset = value

    @property
    def orientation(self) -> '_1924.Orientations':
        """Orientations: 'Orientation' is the original name of this property."""

        temp = self.wrapped.Orientation

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1924.Orientations)(value) if value is not None else None

    @orientation.setter
    def orientation(self, value: '_1924.Orientations'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Orientation = value

    @property
    def outer_offset(self) -> 'Optional[float]':
        """Optional[float]: 'OuterOffset' is the original name of this property."""

        temp = self.wrapped.OuterOffset

        if temp is None:
            return None

        return temp

    @outer_offset.setter
    def outer_offset(self, value: 'Optional[float]'):
        self.wrapped.OuterOffset = value

    @property
    def mounting(self) -> 'List[_2398.BearingRaceMountingOptions]':
        """List[BearingRaceMountingOptions]: 'Mounting' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Mounting

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
