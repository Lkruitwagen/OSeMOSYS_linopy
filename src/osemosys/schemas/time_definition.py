import os
import pandas as pd

from .base import *
from osemosys.utils import *

class TimeDefinition(BaseModel):
    """
    Class to contain all temporal information, including years and timeslices.
    """
    
    # Sets
    years: List[int]
    season: List[int]
    timeslice: List[str]
    day_type: List[int]
    daily_time_bracket: List[int]
    # Parameters
    year_split: StringYearData | None
    day_split: IntYearData | None
    days_in_day_type: IntIntIntData | None
    conversion_ld: StringYearData | None
    conversion_lh: StringYearData | None
    conversion_ls: StringYearData | None



    @classmethod
    def from_simplicity(cls, root_dir) -> "cls":
        """
        Instantiate a single TimeDefinition object containing all relevant data from otoole-organised csvs.

        Parameters
        ----------
        root_dir: str
            Path to the root of the simplicity directory

        Returns
        -------
        TimeDefinition
            A single TimeDefinition instance that can be used downstream or dumped to json/yaml
        """
        # Sets
        df_years = pd.read_csv(os.path.join(root_dir, 'YEAR.csv'))
        df_season = pd.read_csv(os.path.join(root_dir, 'SEASON.csv'))
        df_timeslice = pd.read_csv(os.path.join(root_dir, 'TIMESLICE.csv'))
        df_day_type = pd.read_csv(os.path.join(root_dir, 'DAYTYPE.csv'))
        df_daily_time_bracket = pd.read_csv(os.path.join(root_dir, 'DAILYTIMEBRACKET.csv'))

        # Parameters
        df_year_split = pd.read_csv(os.path.join(root_dir, 'YearSplit.csv'))
        df_day_split = pd.read_csv(os.path.join(root_dir, 'DaySplit.csv'))
        df_days_in_day_type = pd.read_csv(os.path.join(root_dir, 'DaysInDayType.csv'))
        df_conversion_ld = pd.read_csv(os.path.join(root_dir, 'Conversionld.csv'))
        df_conversion_lh = pd.read_csv(os.path.join(root_dir, 'Conversionlh.csv'))
        df_conversion_ls = pd.read_csv(os.path.join(root_dir, 'Conversionls.csv'))

        # Assert days in day type values <=7
        assert df_days_in_day_type["VALUE"].isin([1,2,3,4,5,6,7]).all(), "Days in day type can only take values from 1-7"

        return cls(
                    id="TimeDefinition",
                    #TODO
                    long_name = None,
                    description = None,
                    # Sets
                    years = df_years["VALUE"].values.tolist(),
                    season = df_season["VALUE"].values.tolist(),
                    timeslice = df_timeslice["VALUE"].values.tolist(),
                    day_type = df_day_type["VALUE"].values.tolist(),
                    daily_time_bracket = df_daily_time_bracket["VALUE"].values.tolist(),
                    # Parameters
                    year_split = (
                        StringYearData(
                            data=group_to_json(
                                g=df_year_split,
                                root_column='TIMESLICE',
                                data_columns=['YEAR'],
                                target_column='VALUE',
                            )
                        )
                        if not df_year_split.empty else None),
                    day_split = (
                        IntYearData(
                            data=group_to_json(
                                g=df_year_split,
                                root_column='DAILYTIMEBRACKET',
                                data_columns=['YEAR'],
                                target_column='VALUE',
                            )
                        )
                        if not df_day_split.empty else None),
                    days_in_day_type = (
                        IntIntIntData(
                            data=group_to_json(
                                g=df_year_split,
                                root_column='SEASON',
                                data_columns=['DAYTYPE','YEAR'],
                                target_column='VALUE',
                            )
                        )
                        if not df_days_in_day_type.empty else None),
                    conversion_ld = (
                        StringYearData(
                            data=group_to_json(
                                g=df_year_split,
                                root_column='TIMESLICE',
                                data_columns=['DAYTYPE'],
                                target_column='VALUE',
                            )
                        )
                        if not df_conversion_ld.empty else None),
                    conversion_lh = (
                        StringYearData(
                            data=group_to_json(
                                g=df_year_split,
                                root_column='TIMESLICE',
                                data_columns=['DAILYTIMEBRACKET'],
                                target_column='VALUE',
                            )
                        )
                        if not df_conversion_lh.empty else None),
                    conversion_ls = (
                        StringYearData(
                            data=group_to_json(
                                g=df_year_split,
                                root_column='TIMESLICE',
                                data_columns=['SEASON'],
                                target_column='VALUE',
                            )
                        )
                        if not df_conversion_ls.empty else None)
                    )
