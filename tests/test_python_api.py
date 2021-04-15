
import json
import os
import unittest
from pathlib import Path

import pytest

import urllib.request
from remove_dagmc_tags import remove_tags, find_tags


class TestReactor(unittest.TestCase):

    if Path('dagmc.h5m').is_file() is False:
        test_h5m_file_url = 'https://github.com/Shimwell/fusion_example_for_openmc_using_paramak/raw/main/dagmc.h5m'

        urllib.request.urlretrieve(test_h5m_file_url, 'dagmc.h5m')

    def test_removal_of_graveyard(self):
        """removes a single tag called reflective, passed in as a str"""

        remove_tags(
            input='dagmc.h5m',
            output='output.h5m',
            tags='graveyard',
        )

        assert 'graveyard' in find_tags('dagmc.h5m')
        assert 'graveyard' not in find_tags('output.h5m')
        assert Path('output.h5m').stat().st_size < Path('dagmc.h5m').stat().st_size

    def test_removal_of_reflective_tag(self):
        """removes a single tag called reflective, passed in as a list of one"""

        remove_tags(
            input='dagmc.h5m',
            output='output.h5m',
            tags=['reflective'],
        )

        assert 'reflective' in find_tags('dagmc.h5m')
        assert 'reflective' not in find_tags('output.h5m')
        assert Path('output.h5m').stat().st_size < Path('dagmc.h5m').stat().st_size

    def test_removal_of_two_tags(self):
        """removes two tags called graveyard and reflective"""

        remove_tags(
            input='dagmc.h5m',
            output='output.h5m',
            tags=['graveyard', 'reflective'],
        )

        assert 'reflective' in find_tags('dagmc.h5m')
        assert 'reflective' not in find_tags('output.h5m')
        assert 'graveyard' in find_tags('dagmc.h5m')
        assert 'graveyard' not in find_tags('output.h5m')
        assert Path('output.h5m').stat().st_size < Path('dagmc.h5m').stat().st_size

    def test_conversion_to_h5m(self):
        remove_tags(
            input='dagmc.h5m',
            output='output.h5m',
            # tags is not set so this is a save of the same file with no change
        )
        assert Path('output.h5m').stat().st_size == Path('dagmc.h5m').stat().st_size

    def test_conversion_to_vtk(self):
        remove_tags(
            input='dagmc.h5m',
            output='output.vtk',
            # tags is not set so this is a straight conversion
        )
        assert Path('output.vtk').is_file()

    def test_conversion_to_vtk_without_graveyard(self):
        remove_tags(
            input='dagmc.h5m',
            output='output.vtk',
            tags=['graveyard'],
        )
        assert Path('output.vtk').is_file()

    def test_conversion_to_vtk_without_graveyard_or_reflective_tag(self):
        remove_tags(
            input='dagmc.h5m',
            output='output.vtk',
            tags=['reflective'],
        )
        remove_tags(
            input='dagmc.h5m',
            output='output_big.vtk',
            tags=['graveyard', 'reflective'],
        )
        assert Path('output_big.vtk').is_file()
        assert Path('output.vtk').is_file()
        assert Path('output.vtk').stat().st_size < Path('output_big.vtk').stat().st_size


if __name__ == "__main__":
    unittest.main()
