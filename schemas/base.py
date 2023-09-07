"""
Why? 
-> put documentation/descirptions where the action is.
-> consolidate input files
-> do validation early, using pydantic
-> JSONify
-> some explicitify renaming
"""

"""
extras:
  - parse basic python
  - use yaml links *&
  - wildcard str classes, e.g. *
  - inequality for year, e.g. >=2030
"""


# ####################
# ### BASE CLASSES ###
# ####################

class OSeMOSYSBase(BaseModel)
    code: str
    long_name: str | None
    description: str | None

class RegionTechnologyYearData(BaseModel):
    # can be expressed as:
    #  - one value
    #  - a dict of year:value or region:value or technology:value
    #  - nested technology:{year:value}
    #  - nested region:{technology:{year:value}}
    data: Union[
        float, 
        Dict[Union[str,int],float], 
        Dict[str,Dict[int,float]], 
        Dict[str,Dict[str,Dict[int,float]]]
    ]

class YearData(BaseModel):
    data: Union[
        float,
        Dict[int,float]
    ]

class RegionData(BaseModel):
    data: Union[
        float,
        Dict[str, float]
    ]

class RegionYearData(BaseModel):
    # can be expressed as:
    #  - one value
    #  - a dict of year:value OR region:value
    #  - a dict of region:{year:value}
    data: Union[
        float,
        Dict[Union[str,int],float],
        Dict[str,Dict[int,float]]
    ]

class RegionYearTimeData(BaseModel):
    # can be expressed as:
    #  - one value
    #  - a dict of region:value
    #  - a dict of timeslice:value
    #  - a dict of region:year:value
    #  - a dict of region:timeslice:value
    #  - a dict of region:{year:{timeslice:value}}
    data: Union[
        float, 
        Dict[str, float], # which one? ambiguous
        Dict[str, Dict[int, float]]
        Dict[str, Dict[str, float]],
        Dict[str, Dict[int, Dict[str, float]]]
    ]
class RegionCommodityYearData(BaseModel):
    data: Union[
        float,
        Dict[Union[str,int], float],
        Dict[str,Union[str,int],float],
        Dict[str,str,Union[str,int],float]

    ]