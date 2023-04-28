import pytest
from variables import add_demand_variables, add_activity_variables
import xarray as xr
import numpy as np
from linopy import Model, Variable

from validate import validate_user_data

@pytest.fixture()
def specified_demand_profile():
    data = np.empty((1, 1, 2, 1))
    data.fill(0.5)
    coords = {
        'REGION': ['SIMPLICITY'],
        'FUEL': ['ELC'],
        'TIMESLICE': ['1', '2'],
        'YEAR': [2010]
    }
    dims = ['REGION', 'FUEL', 'TIMESLICE', 'YEAR']
    return xr.DataArray(data, coords, dims, 'SpecifiedDemandProfile')


@pytest.fixture()
def coords():
    return {
        '_REGION': ['SIMPLICITY'],
        'REGION': ['SIMPLICITY'],
        'TECHNOLOGY': ['HEATER'],
        'TIMESLICE': ['1', '2'],
        'MODE_OF_OPERATION': [1],
        'FUEL': ['ELC'],
        'YEAR': [2010]
        }


@pytest.fixture()
def dataset(coords, specified_demand_profile):
    data_vars = {
        'SpecifiedDemandProfile': specified_demand_profile,
    }

    # Dataset containing all the parameters read in from an OSeMOSYS file
    ds = xr.Dataset(data_vars=data_vars, coords=coords)

    return ds

def test_validate_demand_profile(dataset):

    assert validate_user_data(dataset)

def test_validate_demand_profile_raises(dataset):

    dataset['SpecifiedDemandProfile'].data = np.array([[[[0.25], [0.3]]]])

    with pytest.raises(ValueError):
        assert validate_user_data(dataset)

def test_validate_demand_profile_approx(dataset):

    dataset['SpecifiedDemandProfile'].data = np.array([[[[0.99999998], [0.00000001]]]])

    assert validate_user_data(dataset)