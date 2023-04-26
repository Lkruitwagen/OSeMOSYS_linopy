import pytest
from variables import add_demand_variables, add_activity_variables
import xarray as xr
import numpy as np
from linopy import Model, Variable

from constraints import add_demand_constraints


@pytest.fixture()
def specified_annual_demand():
    data = np.empty((1, 2, 1))
    data.fill(np.nan)
    coords = {
        'REGION': ['SIMPLICITY'],
        'FUEL': ['ELC', 'HEAT'],
        'YEAR': [2010]
    }
    dims = ['REGION', 'FUEL', 'YEAR']
    return xr.DataArray(data, coords, dims, 'SpecifiedAnnualDemand')


@pytest.fixture()
def specified_demand_profile():
    data = np.empty((1, 2, 1, 1))
    data.fill(1)
    coords = {
        'REGION': ['SIMPLICITY'],
        'FUEL': ['ELC', 'HEAT'],
        'TIMESLICE': ['1'],
        'YEAR': [2010]
    }
    dims = ['REGION', 'FUEL', 'TIMESLICE', 'YEAR']
    return xr.DataArray(data, coords, dims, 'SpecifiedDemandProfile')


@pytest.fixture()
def year_split():
    data = np.empty((1, 1))
    data[0, 0] = 1
    coords = {
        'TIMESLICE': ['1'],
        'YEAR': [2010]
    }
    dims = ['TIMESLICE', 'YEAR']
    return xr.DataArray(data, coords, dims, 'SpecifiedDemandProfile')


@pytest.fixture()
def coords():
    return {
        '_REGION': ['SIMPLICITY'],
        'REGION': ['SIMPLICITY'],
        'TECHNOLOGY': ['HEATER'],
        'TIMESLICE': ['1'],
        'MODE_OF_OPERATION': [1],
        'FUEL': ['ELC', 'HEAT'],
        'YEAR': [2010]
        }


@pytest.fixture()
def dataset(coords, specified_annual_demand, specified_demand_profile, year_split):
    data_vars = {
        'SpecifiedAnnualDemand': specified_annual_demand,
        'SpecifiedDemandProfile': specified_demand_profile,
        'YearSplit': year_split
    }

    # Dataset containing all the parameters read in from an OSeMOSYS file
    ds = xr.Dataset(data_vars=data_vars, coords=coords)

    return ds


def test_add_demand_constraints(dataset):

    model = Model(force_dim_names=True)

    RTiFY = [dataset.coords['REGION'], dataset.coords['TIMESLICE'], dataset.coords['FUEL'], dataset.coords['YEAR']]
    model.add_variables(coords=RTiFY, name='RateOfDemand')

    actual = add_demand_constraints(dataset, model).constraints

    assert actual.labels.EQ_SpecifiedDemand.shape == (1, 1, 2, 1)

    assert (actual.labels.EQ_SpecifiedDemand[0, 0, :, 0] == -1).all()


def test_add_demand_constraints_no_mask(dataset):

    model = Model(force_dim_names=True)

    RTiFY = [dataset.coords['REGION'], dataset.coords['TIMESLICE'], dataset.coords['FUEL'], dataset.coords['YEAR']]
    model.add_variables(coords=RTiFY, name='RateOfDemand')

    # Fill non nan values into demand so the constraint is built for all demands
    dataset['SpecifiedAnnualDemand'] = dataset['SpecifiedAnnualDemand'].fillna(1)

    actual = add_demand_constraints(dataset, model).constraints

    assert actual.labels.EQ_SpecifiedDemand.shape == (1, 1, 2, 1)

    assert (actual.labels.EQ_SpecifiedDemand[0, 0, :, 0] != -1).all()

    assert(actual['EQ_SpecifiedDemand'].coeffs.values == np.array([[[[1], [1]]]])).all()
