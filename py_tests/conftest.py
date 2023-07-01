import os
from typing import Any, Dict

import h5py
import pytest

HERE = os.path.dirname(__file__)
DETAILED_EVOLUTION_PATH = os.path.join(
    HERE, "../misc/examples/methods_paper_plots/detailed_evolution"
)

TEST_ARCHIVE_DIR = os.path.join(HERE, "test_artifacts")


@pytest.fixture()
def example_compas_output_path(clean=False):
    """Get the path to the COMPAS output file generated by the test suite.

    (This is a fixture so it can passed as a parameter to other tests)
    """
    compas_data_path = os.path.join(
        DETAILED_EVOLUTION_PATH, "COMPAS_Output/COMPAS_Output.h5"
    )

    if not os.path.exists(compas_data_path) or clean:  # Check if path exists
        curr_dir = os.getcwd()
        os.chdir(DETAILED_EVOLUTION_PATH)
        os.system("python runSubmitDemo.py")
        os.chdir(curr_dir)
        print("Generated COMPAS test data")

    return compas_data_path


@pytest.fixture()
def test_archive_dir():
    """Get the path to the test archive directory."""
    os.makedirs(TEST_ARCHIVE_DIR, exist_ok=True)
    return TEST_ARCHIVE_DIR


def get_compas_data(path: str) -> Dict[str, Any]:
    """Reads in a COMPAS h5 file and returns a dict with some data from the file."""
    data = {}
    with h5py.File(path, "r") as f:
        data["groups"] = list(f.keys())
        for group in data["groups"]:
            data[f"{group}_n_cols"] = len(f[group])
            if "SEED" in f[group]:
                data[f"{group}_SEED"] = f[group]["SEED"][:]
    return data