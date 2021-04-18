
import os
import unittest
from pathlib import Path


class TestReactor(unittest.TestCase):

    def test_removal_of_multiple_tags(self):

        # test_removal_of_reflecting_tag
        os.system('rm dagmc_output.h5m')
        os.system(
            'remove-dagmc-tags -i tests/dagmc.h5m -o dagmc_output.h5m -t reflective')
        assert Path('dagmc_output.h5m').exists
        assert Path('dagmc_output.h5m').stat().st_size < Path(
            'tests/dagmc.h5m').stat().st_size
        size_with_out_reflective = Path('dagmc_output.h5m').stat().st_size

        # test_removal_of_graveyard
        os.system('rm dagmc_output.h5m')
        os.system(
            'remove-dagmc-tags -i tests/dagmc.h5m -o dagmc_output.h5m -t mat:graveyard')
        assert Path('dagmc_output.h5m').exists
        assert Path('dagmc_output.h5m').stat().st_size < Path(
            'tests/dagmc.h5m').stat().st_size
        size_with_out_graveyard = Path('dagmc_output.h5m').stat().st_size

        os.system('rm dagmc_output.h5m')
        os.system(
            'remove-dagmc-tags -i tests/dagmc.h5m -o dagmc_output.h5m -t reflective mat:graveyard')
        assert Path('dagmc_output.h5m').exists
        assert Path('dagmc_output.h5m').stat(
        ).st_size < size_with_out_graveyard
        assert Path('dagmc_output.h5m').stat(
        ).st_size < size_with_out_reflective

    def test_conversion_to_vtk_with_multiple_tag_removal(self):

        os.system('rm dagmc_output.vtk')
        os.system(
            'remove-dagmc-tags -i tests/dagmc.h5m -o dagmc_output.vtk -t reflective')
        assert Path('dagmc_output.vtk').exists

        # test_conversion_to_vtk_without_graveyard(self):
        os.system('rm dagmc_output.vtk')
        os.system(
            'remove-dagmc-tags -i tests/dagmc.h5m -o dagmc_output.vtk -t mat:graveyard')
        assert Path('dagmc_output.vtk').exists

        # test_conversion_to_vtk_without_graveyard_or_reflecting_tag(self):
        os.system('rm dagmc_output.vtk')
        os.system(
            'remove-dagmc-tags -i tests/dagmc.h5m -o dagmc_output.vtk -t reflective mat:graveyard')
        assert Path('dagmc_output.vtk').exists


if __name__ == "__main__":
    unittest.main()
