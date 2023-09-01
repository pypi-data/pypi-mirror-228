"""_1803.py

DutyCyclePropertySummary
"""


from typing import Generic, TypeVar

from mastapy._internal import constructor
from mastapy import _0
from mastapy.utility.units_and_measurements import _1573
from mastapy._internal.python_net import python_net_import

_DUTY_CYCLE_PROPERTY_SUMMARY = python_net_import('SMT.MastaAPI.Utility.Property', 'DutyCyclePropertySummary')


__docformat__ = 'restructuredtext en'
__all__ = ('DutyCyclePropertySummary',)


TMeasurement = TypeVar('TMeasurement', bound='_1573.MeasurementBase')
T = TypeVar('T')


class DutyCyclePropertySummary(_0.APIBase, Generic[TMeasurement, T]):
    """DutyCyclePropertySummary

    This is a mastapy class.

    Generic Types:
        TMeasurement
        T
    """

    TYPE = _DUTY_CYCLE_PROPERTY_SUMMARY

    def __init__(self, instance_to_wrap: 'DutyCyclePropertySummary.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def maximum_absolute_value_load_case(self) -> 'T':
        """T: 'MaximumAbsoluteValueLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumAbsoluteValueLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def maximum_value_load_case(self) -> 'T':
        """T: 'MaximumValueLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumValueLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def minimum_value_load_case(self) -> 'T':
        """T: 'MinimumValueLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumValueLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
