from linopy import Model
import xarray as xr
from numpy import inf


def add_variables(ds: xr.Dataset, m: Model) -> Model:
    """
    """
    RRTiFY = [ds.coords['REGION'], ds.coords['_REGION'], ds.coords['TIMESLICE'], ds.coords['FUEL'], ds.coords['YEAR']]
    RRFY = [ds.coords['REGION'], ds.coords['_REGION'], ds.coords['FUEL'], ds.coords['YEAR']]
    RFY = [ds.coords['REGION'], ds.coords['FUEL'], ds.coords['YEAR']]
    RTiFY = [ds.coords['REGION'], ds.coords['TIMESLICE'], ds.coords['FUEL'], ds.coords['YEAR']]
    RSY = [ds.coords['REGION'], ds.coords['STORAGE'], ds.coords['YEAR']]
    RTeY = [ds.coords['REGION'], ds.coords['TECHNOLOGY'], ds.coords['YEAR']]
    RSSDDY = [ds.coords['REGION'], ds.coords['STORAGE'], ds.coords['SEASON'], ds.coords['DAYTYPE'], ds.coords['DAILYTIMEBRACKET'], ds.coords['YEAR']]
    RY = [ds.coords['REGION'], ds.coords['YEAR']]

    # mask = ~ds['SpecifiedAnnualDemand'].expand_dims('TIMESLICE').isnull()
    m.add_variables(lower=0, upper=inf, coords=RTiFY, name='RateOfDemand', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RTiFY, name='Demand', integer=False)
    m.add_variables(lower=-inf, upper=inf, coords=RSSDDY, name='RateOfStorageCharge', integer=False)
    m.add_variables(lower=-inf, upper=inf, coords=RSSDDY, name='RateOfStorageDischarge', integer=False)
    m.add_variables(lower=-inf, upper=inf, coords=RSSDDY, name='NetChargeWithinYear', integer=False)
    m.add_variables(lower=-inf, upper=inf, coords=RSSDDY, name='NetChargeWithinDay', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RSY, name='StorageLevelYearStart', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RSY, name='StorageLevelYearFinish', integer=False)
    coords = [ds.coords['REGION'], ds.coords['STORAGE'], ds.coords['SEASON'], ds.coords['YEAR']]
    m.add_variables(lower=0, upper=inf, coords=coords, name='StorageLevelSeasonStart', integer=False)
    coords = [ds.coords['REGION'], ds.coords['STORAGE'], ds.coords['SEASON'], ds.coords['DAYTYPE'], ds.coords['YEAR']]
    m.add_variables(lower=0, upper=inf, coords=coords, name='StorageLevelDayTypeStart', integer=False)
    coords = [ds.coords['REGION'], ds.coords['STORAGE'], ds.coords['SEASON'], ds.coords['DAYTYPE'], ds.coords['YEAR']]
    m.add_variables(lower=0, upper=inf, coords=coords, name='StorageLevelDayTypeFinish', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RSY, name='StorageLowerLimit', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RSY, name='StorageUpperLimit', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RSY, name='AccumulatedNewStorageCapacity', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RSY, name='NewStorageCapacity', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RSY, name='CapitalInvestmentStorage', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RSY, name='DiscountedCapitalInvestmentStorage', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RSY, name='SalvageValueStorage', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RSY, name='DiscountedSalvageValueStorage', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RSY, name='TotalDiscountedStorageCost', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RTeY, name='NumberOfNewTechnologyUnits', integer=True)
    m.add_variables(lower=0, upper=inf, coords=RTeY, name='NewCapacity', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RTeY, name='AccumulatedNewCapacity', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RTeY, name='TotalCapacityAnnual', integer=False)
    coords = [ds.coords['REGION'], ds.coords['TIMESLICE'], ds.coords['TECHNOLOGY'], ds.coords['MODE_OF_OPERATION'], ds.coords['YEAR']]
    m.add_variables(lower=0, upper=inf, coords=coords, name='RateOfActivity', integer=False)
    coords = [ds.coords['REGION'], ds.coords['TECHNOLOGY'], ds.coords['TIMESLICE'], ds.coords['YEAR']]
    m.add_variables(lower=0, upper=inf, coords=coords, name='RateOfTotalActivity', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RTeY, name='TotalTechnologyAnnualActivity', integer=False)
    coords = [ds.coords['REGION'], ds.coords['TECHNOLOGY'], ds.coords['MODE_OF_OPERATION'], ds.coords['YEAR']]
    m.add_variables(lower=0, upper=inf, coords=coords, name='TotalAnnualTechnologyActivityByMode', integer=False)
    coords = [ds.coords['REGION'], ds.coords['TECHNOLOGY']]
    m.add_variables(lower=-inf, upper=inf, coords=coords, name='TotalTechnologyModelPeriodActivity', integer=False)
    coords = [ds.coords['REGION'], ds.coords['TIMESLICE'], ds.coords['TECHNOLOGY'], ds.coords['MODE_OF_OPERATION'], ds.coords['FUEL'], ds.coords['YEAR']]
    m.add_variables(lower=0, upper=inf, coords=coords, name='RateOfProductionByTechnologyByMode', integer=False)
    coords = [ds.coords['REGION'], ds.coords['TIMESLICE'], ds.coords['TECHNOLOGY'], ds.coords['FUEL'], ds.coords['YEAR']]
    m.add_variables(lower=0, upper=inf, coords=coords, name='RateOfProductionByTechnology', integer=False)
    coords = [ds.coords['REGION'], ds.coords['TIMESLICE'], ds.coords['TECHNOLOGY'], ds.coords['FUEL'], ds.coords['YEAR']]
    m.add_variables(lower=0, upper=inf, coords=coords, name='ProductionByTechnology', integer=False)
    coords = [ds.coords['REGION'], ds.coords['TECHNOLOGY'], ds.coords['FUEL'], ds.coords['YEAR']]
    m.add_variables(lower=0, upper=inf, coords=coords, name='ProductionByTechnologyAnnual', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RTiFY, name='RateOfProduction', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RTiFY, name='Production', integer=False)
    coords = [ds.coords['REGION'], ds.coords['TIMESLICE'], ds.coords['TECHNOLOGY'], ds.coords['MODE_OF_OPERATION'], ds.coords['FUEL'], ds.coords['YEAR']]
    m.add_variables(lower=0, upper=inf, coords=coords, name='RateOfUseByTechnologyByMode', integer=False)
    coords = [ds.coords['REGION'], ds.coords['TIMESLICE'], ds.coords['TECHNOLOGY'], ds.coords['FUEL'], ds.coords['YEAR']]
    m.add_variables(lower=0, upper=inf, coords=coords, name='RateOfUseByTechnology', integer=False)
    coords = [ds.coords['REGION'], ds.coords['TECHNOLOGY'], ds.coords['FUEL'], ds.coords['YEAR']]
    m.add_variables(lower=0, upper=inf, coords=coords, name='UseByTechnologyAnnual', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RTiFY, name='RateOfUse', integer=False)
    coords = [ds.coords['REGION'], ds.coords['TIMESLICE'], ds.coords['TECHNOLOGY'], ds.coords['FUEL'], ds.coords['YEAR']]
    m.add_variables(lower=0, upper=inf, coords=coords, name='UseByTechnology', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RTiFY, name='Use', integer=False)
    m.add_variables(lower=-inf, upper=inf, coords=RRTiFY, name='Trade', integer=False)
    m.add_variables(lower=-inf, upper=inf, coords=RRFY, name='TradeAnnual', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RFY, name='ProductionAnnual', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RFY, name='UseAnnual', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RTeY, name='CapitalInvestment', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RTeY, name='DiscountedCapitalInvestment', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RTeY, name='SalvageValue', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RTeY, name='DiscountedSalvageValue', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RTeY, name='OperatingCost', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RTeY, name='DiscountedOperatingCost', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RTeY, name='AnnualVariableOperatingCost', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RTeY, name='AnnualFixedOperatingCost', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RTeY, name='TotalDiscountedCostByTechnology', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RY, name='TotalDiscountedCost', integer=False)
    coords = [ds.coords['REGION']]
    m.add_variables(lower=0, upper=inf, coords=coords, name='ModelPeriodCostByRegion', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RY, name='TotalCapacityInReserveMargin', integer=False)
    coords = [ds.coords['REGION'], ds.coords['TIMESLICE'], ds.coords['YEAR']]
    m.add_variables(lower=0, upper=inf, coords=coords, name='DemandNeedingReserveMargin', integer=False)
    m.add_variables(lower=-inf, upper=inf, coords=RY, name='TotalREProductionAnnual', integer=False)
    m.add_variables(lower=-inf, upper=inf, coords=RY, name='RETotalProductionOfTargetFuelAnnual', integer=False)
    coords = [ds.coords['REGION'], ds.coords['TECHNOLOGY'], ds.coords['EMISSION'], ds.coords['MODE_OF_OPERATION'], ds.coords['YEAR']]
    m.add_variables(lower=0, upper=inf, coords=coords, name='AnnualTechnologyEmissionByMode', integer=False)
    coords = [ds.coords['REGION'], ds.coords['TECHNOLOGY'], ds.coords['EMISSION'], ds.coords['YEAR']]
    m.add_variables(lower=0, upper=inf, coords=coords, name='AnnualTechnologyEmission', integer=False)
    coords = [ds.coords['REGION'], ds.coords['TECHNOLOGY'], ds.coords['EMISSION'], ds.coords['YEAR']]
    m.add_variables(lower=0, upper=inf, coords=coords, name='AnnualTechnologyEmissionPenaltyByEmission', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RTeY, name='AnnualTechnologyEmissionsPenalty', integer=False)
    m.add_variables(lower=0, upper=inf, coords=RTeY, name='DiscountedTechnologyEmissionsPenalty', integer=False)
    coords = [ds.coords['REGION'], ds.coords['EMISSION'], ds.coords['YEAR']]
    m.add_variables(lower=0, upper=inf, coords=coords, name='AnnualEmissions', integer=False)
    coords = [ds.coords['REGION'], ds.coords['EMISSION']]
    m.add_variables(lower=0, upper=inf, coords=coords, name='ModelPeriodEmissions', integer=False)

    return m
