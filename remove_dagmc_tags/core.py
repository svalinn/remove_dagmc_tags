
import warnings
from pathlib import Path
from typing import List, Optional, Union

import numpy as np
from pymoab import core, types
from pymoab.types import MBENTITYSET


def create_moab_core(input):

    moab_core = core.Core()
    moab_core.load_file(str(input))

    tag_name = moab_core.tag_get_handle(str(types.NAME_TAG_NAME))

    tag_category = moab_core.tag_get_handle(str(types.CATEGORY_TAG_NAME))
    root = moab_core.get_root_set()

    # An array of tag values to be matched for entities returned by the
    # following call.
    group_tag_values = np.array(["Group"])

    # Retrieve all EntitySets with a category tag of the user input value.
    group_categories = list(moab_core.get_entities_by_type_and_tag(
                            root, MBENTITYSET, tag_category, group_tag_values))

    return moab_core, group_categories, tag_name


def find_tags(
    input: Optional[str] = 'dagmc.h5m',
) -> List[str]:
    """Removes a specific tag from a dagmc h5m file and saves the remaining
    geometry as a new h5m file. Useful for visulising the geometry by removing
    the graveyard tag and then the vtk file can be made without a bounding box
    graveyard obstructing the view. Adapted from
    https://github.com/svalinn/DAGMC-viz source code

    Arguments:
        input: The name of the h5m file to remove the dagmc tags from
        output: The name of the outfile file(s) with the tags removed.
            Supported extentions are .vtk and .h5m
        tags: The tag or tags to remove.
        verbose:

    Returns:
        filename of the new dagmc h5m file with the tags removed
    """

    moab_core, group_categories, tag_name = create_moab_core(input)

    # Retrieve all EntitySets with a name tag.
    group_names = moab_core.tag_get_data(tag_name, group_categories, flat=True)

    return group_names


def remove_tags(
    input: Optional[str] = 'dagmc.h5m',
    output: Optional[Union[str, List[str]]] = 'dagmc_removed_tag.vtk',
    tags: Optional[Union[str, List[str]]] = 'graveyard',
    verbose: Optional[bool] = False,
):
# -> List[List[str], List[str], List[str]]:
    """Removes a specific tag from a dagmc h5m file and saves the remaining
    geometry as a new h5m file. Useful for visulising the geometry by removing
    the graveyard tag and then the vtk file can be made without a bounding box
    graveyard obstructing the view. Adapted from
    https://github.com/svalinn/DAGMC-viz source code

    Arguments:
        input: The name of the h5m file to remove the dagmc tags from
        output: The name of the outfile file(s) with the tags removed.
            Supported extentions are .vtk and .h5m
        tags: The tag(S) to be removed.
        verbose: Print out additional information (True) or not (False)

    Returns:
        filename(s) of the output files produced, names of tags removed, names
        of all the tags available
    """
    if verbose is True:
        print()
        print('tags_to_remove', tags)

    moab_core, group_categories, tag_name = create_moab_core(input)

    group_names = find_tags(input=input)

    if isinstance(tags, str):
        tags_to_remove = [tags]
    else:
        tags_to_remove = tags

    # Find the EntitySet whose name includes tag provided
    sets_to_remove = []
    names_to_remove = []
    names_not_remove_removed = []

    for group_set, name in zip(group_categories, group_names):
        for tag_to_remove in tags_to_remove:
            if tag_to_remove in str(name.lower()):
                names_to_remove.append(name.lower())
                sets_to_remove.append(group_set)
            else:
                names_not_remove_removed.append(name.lower())

    names_to_remove = list(sorted(set(names_to_remove)))

    if len(sets_to_remove) == 0:
        warnings.warn('No tags removed.')

    # prints out 
    if verbose is True:
        print()
        for name in sorted(set(group_names)):
            if str(name.lower()) in tags_to_remove:
                print(str(name.lower()), ' --- >  Removing tag')
            else:
                print(str(name.lower()))
        print()

    # Remove the EntitySet from the data.
    groups_to_write = [
        group_set for group_set in group_categories if group_set not in sets_to_remove]

    if isinstance(output, (str, Path)):
        output = [output]

    for out in output:
        if verbose is True:
            print('Writing', out)
        moab_core.write_file(str(out), output_sets=groups_to_write)

    return output, names_to_remove, sorted(set(group_names))
