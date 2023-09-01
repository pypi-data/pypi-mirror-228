"""_1198.py

CylindricalGearLTCAContactChartDataAsTextFile
"""


from mastapy._internal import constructor
from mastapy.gears.cylindrical import _1202
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_LTCA_CONTACT_CHART_DATA_AS_TEXT_FILE = python_net_import('SMT.MastaAPI.Gears.Cylindrical', 'CylindricalGearLTCAContactChartDataAsTextFile')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearLTCAContactChartDataAsTextFile',)


class CylindricalGearLTCAContactChartDataAsTextFile(_1202.GearLTCAContactChartDataAsTextFile):
    """CylindricalGearLTCAContactChartDataAsTextFile

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_LTCA_CONTACT_CHART_DATA_AS_TEXT_FILE

    def __init__(self, instance_to_wrap: 'CylindricalGearLTCAContactChartDataAsTextFile.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def coefficient_of_friction_benedict_and_kelley(self) -> 'str':
        """str: 'CoefficientOfFrictionBenedictAndKelley' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CoefficientOfFrictionBenedictAndKelley

        if temp is None:
            return ''

        return temp

    @property
    def gap_between_unloaded_flanks_transverse(self) -> 'str':
        """str: 'GapBetweenUnloadedFlanksTransverse' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GapBetweenUnloadedFlanksTransverse

        if temp is None:
            return ''

        return temp

    @property
    def gear_a_depth_of_maximum_material_exposure_iso633642019(self) -> 'str':
        """str: 'GearADepthOfMaximumMaterialExposureISO633642019' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearADepthOfMaximumMaterialExposureISO633642019

        if temp is None:
            return ''

        return temp

    @property
    def gear_a_maximum_material_exposure_iso633642019(self) -> 'str':
        """str: 'GearAMaximumMaterialExposureISO633642019' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearAMaximumMaterialExposureISO633642019

        if temp is None:
            return ''

        return temp

    @property
    def gear_b_depth_of_maximum_material_exposure_iso633642019(self) -> 'str':
        """str: 'GearBDepthOfMaximumMaterialExposureISO633642019' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearBDepthOfMaximumMaterialExposureISO633642019

        if temp is None:
            return ''

        return temp

    @property
    def gear_b_maximum_material_exposure_iso633642019(self) -> 'str':
        """str: 'GearBMaximumMaterialExposureISO633642019' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearBMaximumMaterialExposureISO633642019

        if temp is None:
            return ''

        return temp

    @property
    def micropitting_contact_temperature_isotr1514412010(self) -> 'str':
        """str: 'MicropittingContactTemperatureISOTR1514412010' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingContactTemperatureISOTR1514412010

        if temp is None:
            return ''

        return temp

    @property
    def micropitting_contact_temperature_isotr1514412014(self) -> 'str':
        """str: 'MicropittingContactTemperatureISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingContactTemperatureISOTR1514412014

        if temp is None:
            return ''

        return temp

    @property
    def micropitting_contact_temperature_isots6336222018(self) -> 'str':
        """str: 'MicropittingContactTemperatureISOTS6336222018' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingContactTemperatureISOTS6336222018

        if temp is None:
            return ''

        return temp

    @property
    def micropitting_flash_temperature_isotr1514412010(self) -> 'str':
        """str: 'MicropittingFlashTemperatureISOTR1514412010' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingFlashTemperatureISOTR1514412010

        if temp is None:
            return ''

        return temp

    @property
    def micropitting_flash_temperature_isotr1514412014(self) -> 'str':
        """str: 'MicropittingFlashTemperatureISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingFlashTemperatureISOTR1514412014

        if temp is None:
            return ''

        return temp

    @property
    def micropitting_flash_temperature_isots6336222018(self) -> 'str':
        """str: 'MicropittingFlashTemperatureISOTS6336222018' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingFlashTemperatureISOTS6336222018

        if temp is None:
            return ''

        return temp

    @property
    def micropitting_safety_factor_isotr1514412010(self) -> 'str':
        """str: 'MicropittingSafetyFactorISOTR1514412010' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingSafetyFactorISOTR1514412010

        if temp is None:
            return ''

        return temp

    @property
    def micropitting_safety_factor_isotr1514412014(self) -> 'str':
        """str: 'MicropittingSafetyFactorISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingSafetyFactorISOTR1514412014

        if temp is None:
            return ''

        return temp

    @property
    def micropitting_safety_factor_isots6336222018(self) -> 'str':
        """str: 'MicropittingSafetyFactorISOTS6336222018' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingSafetyFactorISOTS6336222018

        if temp is None:
            return ''

        return temp

    @property
    def minimum_lubricant_film_thickness_isotr1514412010(self) -> 'str':
        """str: 'MinimumLubricantFilmThicknessISOTR1514412010' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLubricantFilmThicknessISOTR1514412010

        if temp is None:
            return ''

        return temp

    @property
    def minimum_lubricant_film_thickness_isotr1514412014(self) -> 'str':
        """str: 'MinimumLubricantFilmThicknessISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLubricantFilmThicknessISOTR1514412014

        if temp is None:
            return ''

        return temp

    @property
    def minimum_lubricant_film_thickness_isots6336222018(self) -> 'str':
        """str: 'MinimumLubricantFilmThicknessISOTS6336222018' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLubricantFilmThicknessISOTS6336222018

        if temp is None:
            return ''

        return temp

    @property
    def pressure_velocity_pv(self) -> 'str':
        """str: 'PressureVelocityPV' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PressureVelocityPV

        if temp is None:
            return ''

        return temp

    @property
    def scuffing_contact_temperature_agma925a03(self) -> 'str':
        """str: 'ScuffingContactTemperatureAGMA925A03' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingContactTemperatureAGMA925A03

        if temp is None:
            return ''

        return temp

    @property
    def scuffing_contact_temperature_agma925b22(self) -> 'str':
        """str: 'ScuffingContactTemperatureAGMA925B22' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingContactTemperatureAGMA925B22

        if temp is None:
            return ''

        return temp

    @property
    def scuffing_contact_temperature_din399041987(self) -> 'str':
        """str: 'ScuffingContactTemperatureDIN399041987' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingContactTemperatureDIN399041987

        if temp is None:
            return ''

        return temp

    @property
    def scuffing_contact_temperature_isotr1398912000(self) -> 'str':
        """str: 'ScuffingContactTemperatureISOTR1398912000' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingContactTemperatureISOTR1398912000

        if temp is None:
            return ''

        return temp

    @property
    def scuffing_contact_temperature_isots6336202017(self) -> 'str':
        """str: 'ScuffingContactTemperatureISOTS6336202017' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingContactTemperatureISOTS6336202017

        if temp is None:
            return ''

        return temp

    @property
    def scuffing_contact_temperature_isots6336202022(self) -> 'str':
        """str: 'ScuffingContactTemperatureISOTS6336202022' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingContactTemperatureISOTS6336202022

        if temp is None:
            return ''

        return temp

    @property
    def scuffing_flash_temperature_agma925a03(self) -> 'str':
        """str: 'ScuffingFlashTemperatureAGMA925A03' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingFlashTemperatureAGMA925A03

        if temp is None:
            return ''

        return temp

    @property
    def scuffing_flash_temperature_agma925b22(self) -> 'str':
        """str: 'ScuffingFlashTemperatureAGMA925B22' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingFlashTemperatureAGMA925B22

        if temp is None:
            return ''

        return temp

    @property
    def scuffing_flash_temperature_din399041987(self) -> 'str':
        """str: 'ScuffingFlashTemperatureDIN399041987' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingFlashTemperatureDIN399041987

        if temp is None:
            return ''

        return temp

    @property
    def scuffing_flash_temperature_isotr1398912000(self) -> 'str':
        """str: 'ScuffingFlashTemperatureISOTR1398912000' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingFlashTemperatureISOTR1398912000

        if temp is None:
            return ''

        return temp

    @property
    def scuffing_flash_temperature_isots6336202017(self) -> 'str':
        """str: 'ScuffingFlashTemperatureISOTS6336202017' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingFlashTemperatureISOTS6336202017

        if temp is None:
            return ''

        return temp

    @property
    def scuffing_flash_temperature_isots6336202022(self) -> 'str':
        """str: 'ScuffingFlashTemperatureISOTS6336202022' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingFlashTemperatureISOTS6336202022

        if temp is None:
            return ''

        return temp

    @property
    def scuffing_safety_factor_agma925a03(self) -> 'str':
        """str: 'ScuffingSafetyFactorAGMA925A03' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingSafetyFactorAGMA925A03

        if temp is None:
            return ''

        return temp

    @property
    def scuffing_safety_factor_agma925b22(self) -> 'str':
        """str: 'ScuffingSafetyFactorAGMA925B22' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingSafetyFactorAGMA925B22

        if temp is None:
            return ''

        return temp

    @property
    def scuffing_safety_factor_din399041987(self) -> 'str':
        """str: 'ScuffingSafetyFactorDIN399041987' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingSafetyFactorDIN399041987

        if temp is None:
            return ''

        return temp

    @property
    def scuffing_safety_factor_isotr1398912000(self) -> 'str':
        """str: 'ScuffingSafetyFactorISOTR1398912000' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingSafetyFactorISOTR1398912000

        if temp is None:
            return ''

        return temp

    @property
    def scuffing_safety_factor_isots6336202017(self) -> 'str':
        """str: 'ScuffingSafetyFactorISOTS6336202017' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingSafetyFactorISOTS6336202017

        if temp is None:
            return ''

        return temp

    @property
    def scuffing_safety_factor_isots6336202022(self) -> 'str':
        """str: 'ScuffingSafetyFactorISOTS6336202022' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingSafetyFactorISOTS6336202022

        if temp is None:
            return ''

        return temp

    @property
    def sliding_power_loss(self) -> 'str':
        """str: 'SlidingPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlidingPowerLoss

        if temp is None:
            return ''

        return temp

    @property
    def sliding_velocity(self) -> 'str':
        """str: 'SlidingVelocity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlidingVelocity

        if temp is None:
            return ''

        return temp

    @property
    def specific_lubricant_film_thickness_isotr1514412010(self) -> 'str':
        """str: 'SpecificLubricantFilmThicknessISOTR1514412010' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpecificLubricantFilmThicknessISOTR1514412010

        if temp is None:
            return ''

        return temp

    @property
    def specific_lubricant_film_thickness_isotr1514412014(self) -> 'str':
        """str: 'SpecificLubricantFilmThicknessISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpecificLubricantFilmThicknessISOTR1514412014

        if temp is None:
            return ''

        return temp

    @property
    def specific_lubricant_film_thickness_isots6336222018(self) -> 'str':
        """str: 'SpecificLubricantFilmThicknessISOTS6336222018' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpecificLubricantFilmThicknessISOTS6336222018

        if temp is None:
            return ''

        return temp
