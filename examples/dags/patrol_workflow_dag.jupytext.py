# ruff: noqa: E402

# %% [markdown]
# # Patrol Workflow
# TODO: top level description

# %% [markdown]
# ## Get Patrol Observations

# %%
# parameters

client = ...
since = ...
until = ...
patrol_type = ...
status = ...
include_patrol_details = ...


# %%
# the code for Get Patrol Observations

"Get observations for a patrol type from EarthRanger."

# %%
# return value from this section

get_patrol_observations_return = client.get_patrol_observations_with_patrol_filter(
    since=since,
    until=until,
    patrol_type=patrol_type,
    status=status,
    include_patrol_details=include_patrol_details,
)


# %% [markdown]
# ## Process Relocations
# %%
# dependencies assignments

observations = get_patrol_observations_return


# %%
# parameters

filter_point_coords = ...
relocs_columns = ...


# %%
# the code for Process Relocations

from ecoscope.base import RelocsCoordinateFilter, Relocations

relocs = Relocations(observations)
relocs.apply_reloc_filter(
    RelocsCoordinateFilter(filter_point_coords=filter_point_coords), inplace=True
)
relocs.remove_filtered(inplace=True)
relocs = relocs[relocs_columns]
relocs.columns = [i.replace("extra__", "") for i in relocs.columns]
relocs.columns = [i.replace("subject__", "") for i in relocs.columns]

# %%
# return value from this section

process_relocations_return = relocs


# %% [markdown]
# ## Relocations To Trajectory
# %%
# dependencies assignments

relocations = process_relocations_return


# %%
# parameters

min_length_meters = ...
max_length_meters = ...
max_time_secs = ...
min_time_secs = ...
max_speed_kmhr = ...
min_speed_kmhr = ...


# %%
# the code for Relocations To Trajectory

from ecoscope.base import Relocations
from ecoscope.base import Trajectory, TrajSegFilter

traj = Trajectory.from_relocations(Relocations(relocations))
traj_seg_filter = TrajSegFilter(
    min_length_meters=min_length_meters,
    max_length_meters=max_length_meters,
    min_time_secs=min_time_secs,
    max_time_secs=max_time_secs,
    min_speed_kmhr=min_speed_kmhr,
    max_speed_kmhr=max_speed_kmhr,
)
traj.apply_traj_filter(traj_seg_filter, inplace=True)
traj.remove_filtered(inplace=True)

# %%
# return value from this section

relocations_to_trajectory_return = traj


# %% [markdown]
# ## Draw Ecomap
# %%
# dependencies assignments

geodataframe = relocations_to_trajectory_return


# %%
# parameters

data_type = ...
style_kws = ...
tile_layer = ...
static = ...
title = ...
title_kws = ...
scale_kws = ...
north_arrow_kws = ...


# %%
# the code for Draw Ecomap

'\n    Creates a map based on the provided layer definitions and configuration.\n\n    Args:\n    geodataframe (geopandas.GeoDataFrame): The geodataframe to visualize.\n    data_type (str): The type of visualization, "Scatterplot", "Path" or "Polygon".\n    style_kws (dict): Style arguments for the data visualization.\n    tile_layer (str): A named tile layer, ie OpenStreetMap.\n    static (bool): Set to true to disable map pan/zoom.\n    title (str): The map title.\n    title_kws (dict): Additional arguments for configuring the Title.\n    scale_kws (dict): Additional arguments for configuring the Scale Bar.\n    north_arrow_kws (dict): Additional arguments for configuring the North Arrow.\n\n    Returns:\n    str: A static HTML representation of the map.\n    '
from ecoscope.mapping import EcoMap

m = EcoMap(static=static, default_widgets=False)
if title:
    m.add_title(title, **title_kws)
m.add_scale_bar(**scale_kws)
m.add_north_arrow(**north_arrow_kws)
if tile_layer:
    m.add_layer(EcoMap.get_named_tile_layer(tile_layer))
match data_type:
    case "Scatterplot":
        m.add_scatterplot_layer(geodataframe, **style_kws)
    case "Path":
        m.add_path_layer(geodataframe, **style_kws)
    case "Polygon":
        m.add_polygon_layer(geodataframe, **style_kws)
m.zoom_to_bounds(m.layers)

# %%
# return value from this section

draw_ecomap_return = m.to_html()


# %% [markdown]
# ## Persist Text
# %%
# dependencies assignments

text = draw_ecomap_return


# %%
# parameters

root_path = ...
filename = ...


# %%
# the code for Persist Text

"Persist text to a file or cloud storage object."
from ecoscope_workflows.serde import _persist_text

# %%
# return value from this section

persist_text_return = _persist_text(text, root_path, filename)