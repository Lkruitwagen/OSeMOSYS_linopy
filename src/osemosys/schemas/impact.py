import os
import pandas as pd

from .base import *
from osemosys.utils import *




class Impact(OSeMOSYSBase):
    # previously 'emissions'
    constraint: Union[RegionTechnologyYearData, YearData]
    exogenous: Union[RegionTechnologyYearData, YearData]
    penalty: RegionTechnologyYearData