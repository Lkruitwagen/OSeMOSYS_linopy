



class Model(BaseModel):

    # financials
    depreciation_method: str = "straight-line" # or "sinking-fund"
    discount_rate: RegionTechnologyYearData | None # may want to express this at the technology or model level

    # nodes
    regions: List[Region]

    # technologies
    production_technologies: List[TechnologyProduction]
    storage_technologies: List[TechnologyStorage]
    transmission_technologies: List[TechnologyTransmission]

    reserve_margins_commodity: List[List[str,RegionYearData]]
    reserve_margins_technology: List[List[str, RegionalYearData]]

    renewable_targets: RegionYearData


    @classmethod
    def to_simplicity(cls, root_dir) -> Dict[str,str]:
        """
        Dump regions to 

        Parameters
        ----------
        root_dir: str
            Path to the root of the simplicity directory

        Returns
        -------
        Dict[str,str]
            A list of Region instances that can be used downstream or dumped to json/yaml
        """