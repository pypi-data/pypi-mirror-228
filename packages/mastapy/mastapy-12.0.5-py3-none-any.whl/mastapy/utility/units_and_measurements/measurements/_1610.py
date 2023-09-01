"""_1610.py

Force
"""


from mastapy.utility.units_and_measurements import (
    _1578, _1570, _1571, _1572,
    _1576, _1577, _1579, _1573
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_FORCE = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'Force')


__docformat__ = 'restructuredtext en'
__all__ = ('Force',)


class Force(_1573.MeasurementBase):
    """Force

    This is a mastapy class.
    """

    TYPE = _FORCE

    def __init__(self, instance_to_wrap: 'Force.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def kilograms_force(self) -> '_1578.Unit':
        """Unit: 'KilogramsForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KilogramsForce

        if temp is None:
            return None

        if _1578.Unit.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast kilograms_force to Unit. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def kilonewtons(self) -> '_1578.Unit':
        """Unit: 'Kilonewtons' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Kilonewtons

        if temp is None:
            return None

        if _1578.Unit.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast kilonewtons to Unit. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def millinewtons(self) -> '_1578.Unit':
        """Unit: 'Millinewtons' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Millinewtons

        if temp is None:
            return None

        if _1578.Unit.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast millinewtons to Unit. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def newtons(self) -> '_1578.Unit':
        """Unit: 'Newtons' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Newtons

        if temp is None:
            return None

        if _1578.Unit.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast newtons to Unit. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def ounces_force(self) -> '_1578.Unit':
        """Unit: 'OuncesForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuncesForce

        if temp is None:
            return None

        if _1578.Unit.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast ounces_force to Unit. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def pounds_force(self) -> '_1578.Unit':
        """Unit: 'PoundsForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PoundsForce

        if temp is None:
            return None

        if _1578.Unit.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast pounds_force to Unit. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
