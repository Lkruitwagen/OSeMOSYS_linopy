class Commodity(OSeMOSYSBase):
    # either demand (region:year:timeslice:value)
    # or annual_demand (region:year:value) must be specified;
    # demand_profile may be optionally specified with annual_demand
    demand_annual: RegionYearData | None
    demand_profile: RegionYearTimeData | None
    demand: RegionYearTimeData | None
    is_renewable: bool