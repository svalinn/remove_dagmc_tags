
import os
import unittest
from pathlib import Path

from remove_dagmc_tags import find_tags, remove_tags


class TestReactor(unittest.TestCase):

    def test_removal_of_graveyard(self):
        """removes a single tag called reflective, passed in as a str"""

        os.system('rm output.h5m')

        remove_tags(
            input='tests/dagmc.h5m',
            output='output.h5m',
            tags='mat:graveyard',
        )

        assert 'mat:graveyard' in find_tags('tests/dagmc.h5m')
        assert 'mat:graveyard' not in find_tags('output.h5m')
        assert Path('output.h5m').stat().st_size < Path(
            'tests/dagmc.h5m').stat().st_size

    def test_removal_of_reflective_tag(self):
        """removes a single tag called reflective, passed in as a list of one"""

        os.system('rm output.h5m')

        remove_tags(
            input='tests/dagmc.h5m',
            output='output.h5m',
            tags=['reflective'],
        )

        assert 'reflective' in find_tags('tests/dagmc.h5m')
        assert 'reflective' not in find_tags('output.h5m')
        assert Path('output.h5m').stat().st_size < Path(
            'tests/dagmc.h5m').stat().st_size

    def test_removal_of_two_tags(self):
        """removes two tags called graveyard and reflective"""

        os.system('rm output.h5m')

        returned_vars = remove_tags(
            input='tests/dagmc.h5m',
            output='output.h5m',
            tags=['mat:graveyard', 'reflective'],
        )
        assert returned_vars[0] == ['output.h5m']
        assert returned_vars[1] == ['mat:graveyard', 'reflective']
        assert 'reflective' in find_tags('tests/dagmc.h5m')
        assert 'reflective' not in find_tags('output.h5m')
        assert 'mat:graveyard' in find_tags('tests/dagmc.h5m')
        assert 'mat:graveyard' not in find_tags('output.h5m')
        assert Path('output.h5m').stat().st_size < Path(
            'tests/dagmc.h5m').stat().st_size

    def test_removal_of_two_tags_and_vtk_production(self):
        """removes two tags called graveyard and reflective"""

        os.system('rm output.h5m output.vtk')

        returned_vars = remove_tags(
            input='tests/dagmc.h5m',
            output=['output.h5m', 'output.vtk'],
            tags=['mat:graveyard', 'reflective'],
        )
        assert returned_vars[0] == ['output.h5m', 'output.vtk']
        assert returned_vars[1] == ['mat:graveyard', 'reflective']
        assert 'reflective' in find_tags('tests/dagmc.h5m')
        assert 'reflective' not in find_tags('output.h5m')
        assert 'mat:graveyard' in find_tags('tests/dagmc.h5m')
        assert 'mat:graveyard' not in find_tags('output.h5m')
        assert Path('output.h5m').stat().st_size < Path(
            'tests/dagmc.h5m').stat().st_size

    # If processed file is the same as the input file then this test can be performed
    # def test_conversion_to_h5m(self):
    #     remove_tags(
    #         input='tests/dagmc.h5m',
    #         output='output.h5m',
    #         verbose=True
    #         # tags is not set so this is a save of the same file with no change
    #     )
    #     assert Path('output.h5m').stat().st_size == Path('tests/dagmc.h5m').stat().st_size

    def test_conversion_to_vtk(self):

        os.system('rm output.vtk')

        remove_tags(
            input='tests/dagmc.h5m',
            output='output.vtk',
            # tags is not set so this is a straight conversion
        )
        assert Path('output.vtk').is_file()

    def test_conversion_to_vtk_without_graveyard(self):

        os.system('rm output.vtk')

        returned_var = remove_tags(
            input='tests/dagmc.h5m',
            output='output.vtk',
            tags=['mat:graveyard'],
        )

        assert Path('output.vtk').is_file()
        assert ['output.vtk'] == returned_var[0]
        assert ['mat:graveyard'] == returned_var[1]

    def test_returned_tags_only_include_removed_tags(self):

        os.system('rm output.vtk')

        returned_var = remove_tags(
            input='tests/dagmc.h5m',
            output='output.vtk',
            tags=['mat:graveyard', 'non_existent_tag'],
        )

        assert Path('output.vtk').is_file()
        assert ['output.vtk'] == returned_var[0]
        assert ['mat:graveyard'] == returned_var[1]

    def test_conversion_to_vtk_without_graveyard_or_reflective_tag(self):

        os.system('rm output.vtk output_small.vtk')

        remove_tags(
            input='tests/dagmc.h5m',
            output='output.vtk',
            tags=['mat:graveyard'],
        )

        remove_tags(
            input='tests/dagmc.h5m',
            output='output_small.vtk',
            tags=['mat:graveyard', 'reflective'],
        )
        assert Path('output_small.vtk').is_file()
        assert Path('output.vtk').is_file()
        # This test will work if tags require space in the file
        # assert Path('output.vtk').stat().st_size > Path('output_small.vtk').stat().st_size


if __name__ == "__main__":
    unittest.main()
