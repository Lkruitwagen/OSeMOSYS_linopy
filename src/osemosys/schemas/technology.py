import os
import pandas as pd

from .base import *
from osemosys.utils import *

# ##################
# ### TECHNOLOGY ###
# ##################

class Technology(OSeMOSYSBase):
    """
    Class to contain all information pertaining to technologies (excluding storage technologies)
    """
        
    # Capacity unit to activity unit conversion
    # Conversion factor relating the energy that would be produced when one unit of capacity is fully used in one year.
    capacity_activity_unit_ratio: RegionData

    # Capacity of one new unit of a technology
    # If specified the problem will turn into a Mixed Integer Linear Problem
    capacity_one_tech_unit: RegionYearData | None

    # Capacity factor, lifespan, availability
    availability_factor: RegionYearData | None # Maximum time a technology can run in the whole year, as a fraction from 0 to 1
    capacity_factor: RegionYearTimeData | None
    operating_life: RegionData
    
    # financials
    capex: RegionYearData | None
    opex_fixed: RegionYearData | None
    opex_variable: RegionModeYearData | None

    # operations
    operating_modes: List[int]
    
    # initial capacity
    residual_capacity: RegionYearData | None
    
    # constraints - capacity
    capacity_gross_max: RegionYearData | None               # Maximum technology capacity (installed + residual) per year
    capacity_gross_min: RegionYearData | None               # Minimum technology capacity (installed + residual) per year
    capacity_additional_max: RegionYearData | None          # Maximum technology capacity additions per year
    capacity_additional_min: RegionYearData | None          # Minimum technology capacity additions per year
    
    #TODO
    # Relative growth rate restrictions not currently implemented in osemosys, can be added via change in osemosys code
    #additional_capacity_max_growth_rate: RegionYearData     # growth rate (<1.)
    #additional_capacity_max_ceil: RegionYearData            # Absolute value (ceil relative to growth rate)
    #additional_capacity_max_floor: RegionYearData           # absolute value (floor relative to growth rate)
    #additional_capacity_min_growth_rate: RegionYearData     # growth rate (<1.)

    # constraints - activity
    activity_annual_max: RegionYearData | None              # Maximum technology activity per year
    activity_annual_min: RegionYearData | None              # Minimum technology activity per year
    activity_total_max: RegionData | None                   # Maximum technology activity across whole modelled period
    activity_total_min: RegionData | None                   # Minimum technology activity across whole modelled period

    # activity ratios & efficiency
    emission_activity_ratio: StringStringIntIntData | None        # Technology emission activity ratio by mode of operation
    input_activity_ratio: StringStringIntIntData | None           # Technology fuel input activity ratio by mode of operation
    output_activity_ratio: StringStringIntIntData | None          # Technology fuel output activity ratio by mode of operation
    to_storage: StringStringIntIntData | None                     # Binary parameter linking a technology to the storage facility it charges (1 linked, 0 unlinked)
    from_storage: StringStringIntIntData | None                   # Binary parameter linking a storage facility to the technology it feeds (1 linked, 0 unlinked)
    
    
    @classmethod
    def from_otoole_csv(cls, root_dir) -> List["cls"]:
        
        df_technologies = pd.read_csv(os.path.join(root_dir, 'TECHNOLOGY.csv'))
        
        df_capacity_activity_unit_ratio = pd.read_csv(os.path.join(root_dir, 'TECHNOLOGY.csv'))
        capacity_one_tech_unit = pd.read_csv(os.path.join(root_dir, 'CapacityOfOneTechnologyUnit.csv'))
        availability_factor = pd.read_csv(os.path.join(root_dir, 'AvailabilityFactor.csv'))
        capacity_factor = pd.read_csv(os.path.join(root_dir, 'CapacityFactor.csv'))
        operating_life = pd.read_csv(os.path.join(root_dir, 'OperationalLife.csv'))
        capex = pd.read_csv(os.path.join(root_dir, 'CapitalCost.csv'))
        opex_fixed = pd.read_csv(os.path.join(root_dir, 'FixedCost.csv'))
        opex_variable = pd.read_csv(os.path.join(root_dir, 'VariableCost.csv'))
        operating_modes = pd.read_csv(os.path.join(root_dir, 'MODE_OF_OPERATION.csv'))
        residual_capacity = pd.read_csv(os.path.join(root_dir, 'ResidualCapacity.csv'))
        capacity_gross_max = pd.read_csv(os.path.join(root_dir, 'TotalAnnualMaxCapacity.csv'))
        capacity_gross_min = pd.read_csv(os.path.join(root_dir, 'TotalAnnualMinCapacity.csv'))
        capacity_additional_max = pd.read_csv(os.path.join(root_dir, 'TotalAnnualMaxCapacityInvestment.csv'))
        capacity_additional_min = pd.read_csv(os.path.join(root_dir, 'TotalAnnualMinCapacityInvestment.csv'))
        activity_annual_max = pd.read_csv(os.path.join(root_dir, 'TotalTechnologyAnnualActivityUpperLimit.csv'))
        activity_annual_min = pd.read_csv(os.path.join(root_dir, 'TotalTechnologyAnnualActivityLowerLimit.csv'))
        activity_total_max = pd.read_csv(os.path.join(root_dir, 'TotalTechnologyModelPeriodActivityUpperLimit.csv'))
        activity_total_min = pd.read_csv(os.path.join(root_dir, 'TotalTechnologyModelPeriodActivityLowerLimit.csv'))
        emission_activity_ratio = pd.read_csv(os.path.join(root_dir, 'EmissionActivityRatio.csv'))
        input_activity_ratio = pd.read_csv(os.path.join(root_dir, 'InputActivityRatio.csv'))
        output_activity_ratio = pd.read_csv(os.path.join(root_dir, 'OutputActivityRatio.csv'))
        to_storage = pd.read_csv(os.path.join(root_dir, 'TechnologyToStorage.csv'))
        from_storage = pd.read_csv(os.path.join(root_dir, 'TechnologyFromStorage.csv'))

        technology_instances = []
        for technology in df_technologies['VALUE'].values.tolist():
            #TODO can this be generalised into a function?
            None

        return technology_instances
    

class TechnologyStorage(OSeMOSYSBase):
    """
    Class to contain all information pertaining to storage technologies
    """
    
    capex: RegionYearData | None
    operating_life: RegionData
    minimum_charge: RegionYearData | None   # Lower bound to the amount of energy stored, as a fraction of the maximum, with a number reanging between 0 and 1
    initial_level: RegionData | None        # Level of storage at the beginning of first modelled year, in units of activity
    residual_capacity: RegionYearData | None
    max_discharge_rate: RegionData | None   # Maximum discharging rate for the storage, in units of activity per year
    max_charge_rate: RegionData | None      # Maximum charging rate for the storage, in units of activity per year

    
    @classmethod
    def from_otoole_csv(cls, root_dir) -> List["cls"]:
        
        df_storage_technologies = pd.read_csv(os.path.join(root_dir, 'STORAGE.csv'))
        
        df_capex = pd.read_csv(os.path.join(root_dir, 'TechnologyFromStorage.csv'))
        df_operating_life = pd.read_csv(os.path.join(root_dir, 'TechnologyFromStorage.csv'))
        df_minimum_charge = pd.read_csv(os.path.join(root_dir, 'TechnologyFromStorage.csv'))
        df_initial_level = pd.read_csv(os.path.join(root_dir, 'TechnologyFromStorage.csv'))
        df_residual_capacity = pd.read_csv(os.path.join(root_dir, 'TechnologyFromStorage.csv'))
        df_max_discharge_rate = pd.read_csv(os.path.join(root_dir, 'TechnologyFromStorage.csv'))
        df_max_charge_rate = pd.read_csv(os.path.join(root_dir, 'TechnologyFromStorage.csv'))

        storage_instances = []
        for storage in df_storage_technologies['VALUE'].values.tolist():
            storage_instances.append(
                cls(
                    id = storage,
                    long_name = None,
                    description = None,
                    capex = (
                        RegionYearData(
                        data=group_to_json(
                            g=df_capex.loc[df_capex['STORAGE']==storage],
                            root_column='STORAGE',
                            data_columns=['REGION','YEAR'],
                            target_column='VALUE',
                            )
                        )
                        if storage in df_capex["STORAGE"].values
                        else None),
                    operating_life = (
                        RegionTechnologyYearData(
                        data=group_to_json(
                            g=df_operating_life.loc[df_operating_life['STORAGE']==storage],
                            root_column='STORAGE',
                            data_columns=['REGION'],
                            target_column='VALUE',
                            )
                        )
                        if storage in df_operating_life["STORAGE"].values
                        else None),
                    minimum_charge = (
                        RegionTechnologyYearData(
                        data=group_to_json(
                            g=df_minimum_charge.loc[df_minimum_charge['STORAGE']==storage],
                            root_column='STORAGE',
                            data_columns=['REGION','YEAR'],
                            target_column='VALUE',
                            )
                        )
                        if storage in df_minimum_charge["STORAGE"].values
                        else None),
                    initial_level = (
                        RegionTechnologyYearData(
                        data=group_to_json(
                            g=df_initial_level.loc[df_initial_level['STORAGE']==storage],
                            root_column='STORAGE',
                            data_columns=['REGION'],
                            target_column='VALUE',
                            )
                        )
                        if storage in df_initial_level["STORAGE"].values
                        else None),
                    residual_capacity = (
                        RegionTechnologyYearData(
                        data=group_to_json(
                            g=df_residual_capacity.loc[df_residual_capacity['STORAGE']==storage],
                            root_column='STORAGE',
                            data_columns=['REGION','YEAR'],
                            target_column='VALUE',
                            )
                        )
                        if storage in df_residual_capacity["STORAGE"].values
                        else None),
                    max_discharge_rate = (
                        RegionTechnologyYearData(
                        data=group_to_json(
                            g=df_max_discharge_rate.loc[df_max_discharge_rate['STORAGE']==storage],
                            root_column='STORAGE',
                            data_columns=['REGION'],
                            target_column='VALUE',
                            )
                        )
                        if storage in df_max_discharge_rate["STORAGE"].values
                        else None),
                    max_charge_rate = (
                        RegionTechnologyYearData(
                        data=group_to_json(
                            g=df_max_charge_rate.loc[df_max_charge_rate['STORAGE']==storage],
                            root_column='STORAGE',
                            data_columns=['REGION'],
                            target_column='VALUE',
                            )
                        )
                        if storage in df_max_charge_rate["STORAGE"].values
                        else None)
                )
            )

        return storage_instances
    






####################################################################################################################### OLD
"""
class TechnologyOperatingMode(OSeMOSYSBase):
    # activity ratios & efficiency
    impact_activity_ratio: RegionCommodityYearData
    input_activity_ratio: RegionCommodityYearData
    output_activity_ratio: RegionCommodityYearData
    to_storage: str | None
    from_storage: str | None

    # financials
    opex_variable: RegionYearData

class Technology(OSeMOSYSBase):
    # unit conversions
    activity_unit_ratio: float # one unit of capacity used for a whole year

    # economic grain size, e.g. only 5000MW plants (forces MILP problem)
    capacity_addition_size: RegionData | None 

    # capacity, lifespan, availability
    availability_factor: RegionYearData 
    capacity_factor: RegionYearTimeData
    operating_life: RegionData

    # financials
    capex: RegionYearData
    opex_fixed: RegionYearData
    
    # operations
    operating_modes: List[TechnologyOperatingMode]

    # initial conditions
    residual_capacity: RegionYearData

    # constraints - capacity
    gross_capacity_max: RegionYearData                      # potential
    additional_capacity_max_ceil: RegionYearData            # Absolute value (ceil relative to growth rate)
    additional_capacity_max_floor: RegionYearData           # absolute value (floor relative to growth rate)
    additional_capacity_max_growth_rate: RegionYearData     # growth rate (<1.)
    gross_capacity_min: RegionYearData                      # must-build
    additional_capacity_min: RegionYearData                 # Absolute must-build value
    additional_capacity_min_growth_rate: RegionYearData     # growth rate (<1.)

    # constraints - activity
    annual_activity_max: RegionYearData
    annual_activity_min: RegionYearData
    total_activity_max: RegionData
    total_activity_min: RegionData



class TechnologyStorage(Technology):
    include_regions: List[str] | None
    exclude_regions: List[str] | None
    minimum_charge: RegionData
    initial_level: RegionData
    max_discharge_rate: RegionData
    max_charge_rate: RegionData



class TechnologyProduction(Technology):
    include_regions: List[str] | None
    exclude_regions: List[str] | None
    is_renewable: bool



class TechnologyTransmission(Technology):
    include_region_pairs: List[str] | None
    exclude_region_pairs: List[str] | None

"""