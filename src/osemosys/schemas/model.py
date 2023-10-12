import os
import pandas as pd


from .base import *
from osemosys.utils import *
from .time_definition import *
from .region import *
from .commodity import *
from .impact import *
from .technology import *


class RunSpec(OSeMOSYSBase):

    # financials
    depreciation_method: RegionData | None # 1= "straight-line" # or "sinking-fund"
    discount_rate: RegionTechnologyYearData | None # may want to express this at the technology or model level

    # time definition
    #TODO
    #time_definition: TimeDefinition

    # nodes
    regions: List[Region]

    # commodities
    commodities: List[Commodity]

    # impact constraints (e.g. CO2)
    #TODO
    #impacts: List[Impact]

    # technologies
    #TODO
    #production_technologies: List[TechnologyProduction]
    #storage_technologies: List[TechnologyStorage]
    #transmission_technologies: List[TechnologyTransmission]

    # reserve margins if any
    reserve_margins_commodity: List[Dict[str,RegionYearData]] | None
    reserve_margins_technology: List[Dict[str, RegionYearData]] | None

    # renewable targets
    renewable_targets: RegionYearData | None
    

    def to_simplicity(self, comparison_directory) -> Dict[str,str]:
        """
        Dump regions to 

        Parameters
        ----------
        root_dir: str
            Path to the root of the simplicity directory

        Returns
        -------
        Dict[str,str]
            A dictionary with keys the otool filenames and paths the otool paths
        """
        self.commodities.to_simplicity(comparison_directory)
        
        pass

    @classmethod
    def from_simplicity(cls, root_dir) -> "cls":

        def get_depreciation_method(root_dir):
            df = pd.read_csv(os.path.join(root_dir, 'DepreciationMethod.csv'))
            

        def get_discount_rate(root_dir):
            None
        def get_reserve_margins_commodity(root_dir):
            None
        def get_reserve_margins_technology(root_dir):
            None
        def get_renewable_targets(root_dir):
            None

        # depreciation method
        depreciation_method = get_depreciation_method(root_dir)
        discount_rate = get_discount_rate(root_dir)
        reserve_margins_commodity = get_reserve_margins_commodity(root_dir)
        reserve_margins_technology = get_reserve_margins_technology(root_dir)
        renewable_targets = get_renewable_targets(root_dir)


        return cls(
            id = "id",
            long_name = None,
            description = None,
            depreciation_method = depreciation_method,
            discount_rate=discount_rate,
            regions=Region.from_simplicity(root_dir=root_dir),
            #TODO
            #production_technologies=TechnologyProduction.from_simplicity(root_dir=root_dir),
            #storage_technologies=TechnologyStorage.from_simplicity(root_dir=root_dir),
            #transmission_technologies=TechnologyTransmission.from_simplicity(root_dir=root_dir),
            commodities=Commodity.from_simplicity(root_dir=root_dir),
            reserve_margins_commodity=reserve_margins_commodity,
            reserve_margins_technology=reserve_margins_technology,
            renewable_targets=renewable_targets
            
        )