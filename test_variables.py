import pytest
from variables import add_demand_variables, add_activity_variables
import xarray as xr
import numpy as np
from linopy import Model, Variable


@pytest.fixture()
def input_activity_ratio():
    data = np.empty((1, 1, 2, 1, 1))
    data.fill(np.nan)
    data[0, 0, 0, 0, 0] = 1
    coords = {
        'REGION': ['SIMPLICITY'],
        'TECHNOLOGY': ['HEATER'],
        'FUEL': ['ELC', 'HEAT'],
        'MODE_OF_OPERATION': [1],
        'YEAR': [2010]
    }
    dims = ['REGION', 'TECHNOLOGY', 'FUEL', 'MODE_OF_OPERATION', 'YEAR']
    return xr.DataArray(data, coords, dims, name='InputActivityRatio')


@pytest.fixture()
def output_activity_ratio():
    data = np.empty((1, 1, 2, 1, 1))
    data.fill(np.nan)
    data[0, 0, 1, 0, 0] = 1
    coords = {
        'REGION': ['SIMPLICITY'],
        'TECHNOLOGY': ['HEATER'],
        'FUEL': ['ELC', 'HEAT'],
        'MODE_OF_OPERATION': [1],
        'YEAR': [2010]
    }
    dims = ['REGION', 'TECHNOLOGY', 'FUEL', 'MODE_OF_OPERATION', 'YEAR']
    return xr.DataArray(data, coords, dims, 'OutputActivityRatio')

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
def model(coords, input_activity_ratio, output_activity_ratio):
    data_vars = {
        'InputActivityRatio': input_activity_ratio,
        'OutputActivityRatio': output_activity_ratio,
    }

    # Dataset containing all the parameters read in from an OSeMOSYS file
    ds = xr.Dataset(data_vars=data_vars, coords=coords)

    m = Model(force_dim_names=True)
    return (m, ds)


def test_add_demand_variables(model):

    model, ds = model

    model = add_demand_variables(ds, model)

    actual = model.variables

    assert actual.nvars == 4
    assert 'RateOfDemand' in actual
    assert 'Demand' in actual
    assert actual['Demand'].shape == (1, 1, 2, 1)
    assert actual['RateOfDemand'].shape == (1, 1, 2, 1)


def test_add_activity_variables(model):
    """Checks that the largest variables are created correctly

    Mask is applied which prevents variable creation for values not in Input or Output activity ratio
    """

    model, ds = model
    model = add_activity_variables(ds, model)
    variables = model.variables

    assert variables.nvars == 29

    assert 'RateOfProductionByTechnologyByMode' in variables
    assert 'RateOfUseByTechnologyByMode' in variables

    assert variables['RateOfProductionByTechnologyByMode'].shape == (1, 1, 1, 1, 2, 1)
    assert variables['RateOfUseByTechnologyByMode'].shape == (1, 1, 1, 1, 2, 1)

    print(variables['RateOfProductionByTechnologyByMode'].mask)
    actual = variables['RateOfProductionByTechnologyByMode'].mask.values
    expected = np.array([[[[[[False], [True]]]]]])
    assert (actual == expected).all()

    print(variables['RateOfUseByTechnologyByMode'].mask)
    actual = variables['RateOfUseByTechnologyByMode'].mask.values
    expected = np.array([[[[[[True], [False]]]]]])
    assert (actual == expected).all()

