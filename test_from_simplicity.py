import glob
from pathlib import Path

from osemosys.schemas import RunSpec

root_dir = "test/model_three/"
comparison_directory = "simplicity_compare/"

# uses the class method on the base class to instantiate itself
run_spec_object = RunSpec.from_simplicity(root_dir=root_dir)

# type(run_spec_object) == <class RunSpec>
run_spec_object.to_csv(comparison_directory=comparison_directory)

comparison_files = glob.glob(comparison_directory + "*.csv")
comparison_files = {Path(f).stem:f for f in comparison_files}

original_files = glob.glob(root_dir + "*.csv")
original_files = {Path(f).stem:f for f in original_files}

# let's check all our keys from our original data are in comparison
for stem in original_files.keys():
    assert stem in comparison_files.keys(), f'missing stem: {stem}'

# now let's check that all data is equal
for stem in original_files.keys():
    assert (pd.read_csv(original_files[stem]).equals(pd.read_csv(compare_files[stem])), f'unequal files: {stem}')