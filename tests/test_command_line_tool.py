
import os
import unittest
from pathlib import Path

import pytest


class TestReactor(unittest.TestCase):

    if Path('dagmc.h5m').is_file() is False:
        test_h5m_file_url = 'https://github.com/Shimwell/fusion_example_for_openmc_using_paramak/raw/main/dagmc.h5m'

        urllib.request.urlretrieve(test_h5m_file_url, 'dagmc.h5m')


    def test_removal_of_graveyard(self):
        os.system('remove-dagmc-tags -i dagmc.h5m -o dagmc_output.h5m -t mat:graveyard')
        assert Path('dagmc_output.h5m').exists
        assert Path('dagmc_output.h5m').stat < Path('dagmc.h5m').stat

    def test_removal_of_reflecting_tag(self):
        os.system('remove-dagmc-tags -i dagmc.h5m -o dagmc_output.h5m -t reflective')
        assert Path('dagmc_output.h5m').exists
        assert Path('dagmc_output.h5m').stat < Path('dagmc.h5m').stat

    def test_removal_of_two_tags(self):
    def test_conversion_to_vtk(self):
    def test_conversion_to_vtk_without_graveyard(self):
    def test_conversion_to_vtk_without_graveyard_or_reflecting_tag(self):


if __name__ == "__main__":
    unittest.main()
