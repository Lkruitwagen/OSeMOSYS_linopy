import xarray as xr


def validate_user_data(ds: xr.Dataset):
    """Validate the user parameters

    """

    df = ds['SpecifiedDemandProfile'].to_dataframe().dropna()
    # Returns True if all sums over TIMESLICE == 1
    df_sum = df.groupby(by=['REGION', 'FUEL', 'YEAR']).sum()

    msg = """The fraction of annual energy-service/fuel/proxy demand that is
           required in each time step should sum to 1."""
    errors = []
    if not (df_sum == 1).values.all():
        for row in df_sum.iterrows():
            if (row[1] != 1).all():
                print(row[0])
                errors.append((row[0], float(row[1].values)))
        raise ValueError(f"{msg}:\n\n{errors}")
    return True
