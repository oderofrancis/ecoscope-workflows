# [generated]
# by = { compiler = "ecoscope-workflows-core", version = "9999" }
# from-spec-sha256 = "d9d548e9cb9367a2c7ded96cb3d5d53baa753c1ae615426fd47ffb4d149d9df5"


# ruff: noqa: E402

# %% [markdown]
# # Subject Tracking
# TODO: top level description

# %% [markdown]
# ## Imports

import os
from ecoscope_workflows_core.tasks.config import set_workflow_details
from ecoscope_workflows_core.tasks.groupby import set_groupers
from ecoscope_workflows_core.tasks.filter import set_time_range
from ecoscope_workflows_ext_ecoscope.tasks.io import get_subjectgroup_observations
from ecoscope_workflows_ext_ecoscope.tasks.preprocessing import process_relocations
from ecoscope_workflows_ext_ecoscope.tasks.transformation import classify_is_night
from ecoscope_workflows_ext_ecoscope.tasks.preprocessing import (
    relocations_to_trajectory,
)
from ecoscope_workflows_core.tasks.transformation import add_temporal_index
from ecoscope_workflows_core.tasks.groupby import split_groups
from ecoscope_workflows_ext_ecoscope.tasks.transformation import apply_classification
from ecoscope_workflows_ext_ecoscope.tasks.transformation import apply_color_map
from ecoscope_workflows_core.tasks.transformation import map_values_with_unit
from ecoscope_workflows_ext_ecoscope.tasks.results import create_map_layer
from ecoscope_workflows_ext_ecoscope.tasks.results import draw_ecomap
from ecoscope_workflows_core.tasks.io import persist_text
from ecoscope_workflows_core.tasks.results import create_map_widget_single_view
from ecoscope_workflows_core.tasks.results import merge_widget_views
from ecoscope_workflows_core.tasks.analysis import dataframe_column_mean
from ecoscope_workflows_core.tasks.transformation import with_unit
from ecoscope_workflows_core.tasks.results import create_single_value_widget_single_view
from ecoscope_workflows_core.tasks.analysis import dataframe_column_max
from ecoscope_workflows_core.tasks.analysis import dataframe_count
from ecoscope_workflows_ext_ecoscope.tasks.analysis import get_day_night_ratio
from ecoscope_workflows_core.tasks.analysis import dataframe_column_sum
from ecoscope_workflows_ext_ecoscope.tasks.analysis import calculate_time_density
from ecoscope_workflows_ext_ecoscope.tasks.results import draw_ecoplot
from ecoscope_workflows_core.tasks.results import create_plot_widget_single_view
from ecoscope_workflows_core.tasks.results import gather_dashboard

# %% [markdown]
# ## Set Workflow Details

# %%
# parameters

workflow_details_params = dict(
    name=...,
    description=...,
    image_url=...,
)

# %%
# call the task


workflow_details = set_workflow_details.partial(**workflow_details_params).call()


# %% [markdown]
# ## Set Groupers

# %%
# parameters

groupers_params = dict(
    groupers=...,
)

# %%
# call the task


groupers = set_groupers.partial(**groupers_params).call()


# %% [markdown]
# ## Set Time Range Filters

# %%
# parameters

time_range_params = dict(
    since=...,
    until=...,
    time_format=...,
)

# %%
# call the task


time_range = set_time_range.partial(**time_range_params).call()


# %% [markdown]
# ## Get Subject Group Observations from EarthRanger

# %%
# parameters

subject_obs_params = dict(
    client=...,
    subject_group_name=...,
    include_inactive=...,
)

# %%
# call the task


subject_obs = get_subjectgroup_observations.partial(
    time_range=time_range, **subject_obs_params
).call()


# %% [markdown]
# ## Transform Observations to Relocations

# %%
# parameters

subject_reloc_params = dict(
    filter_point_coords=...,
    relocs_columns=...,
)

# %%
# call the task


subject_reloc = process_relocations.partial(
    observations=subject_obs, **subject_reloc_params
).call()


# %% [markdown]
# ## Apply Day/Night Labels to Relocations

# %%
# parameters

day_night_labels_params = dict()

# %%
# call the task


day_night_labels = classify_is_night.partial(
    relocations=subject_reloc, **day_night_labels_params
).call()


# %% [markdown]
# ## Transform Relocations to Trajectories

# %%
# parameters

subject_traj_params = dict(
    min_length_meters=...,
    max_length_meters=...,
    max_time_secs=...,
    min_time_secs=...,
    max_speed_kmhr=...,
    min_speed_kmhr=...,
)

# %%
# call the task


subject_traj = relocations_to_trajectory.partial(
    relocations=day_night_labels, **subject_traj_params
).call()


# %% [markdown]
# ## Add temporal index to Subject Trajectories

# %%
# parameters

traj_add_temporal_index_params = dict(
    index_name=...,
    time_col=...,
    directive=...,
    cast_to_datetime=...,
    format=...,
)

# %%
# call the task


traj_add_temporal_index = add_temporal_index.partial(
    df=subject_traj, **traj_add_temporal_index_params
).call()


# %% [markdown]
# ## Split Subject Trajectories by Group

# %%
# parameters

split_subject_traj_groups_params = dict()

# %%
# call the task


split_subject_traj_groups = split_groups.partial(
    df=traj_add_temporal_index, groupers=groupers, **split_subject_traj_groups_params
).call()


# %% [markdown]
# ## Classify Trajectories By Speed

# %%
# parameters

classify_traj_speed_params = dict(
    input_column_name=...,
    output_column_name=...,
    labels=...,
    classification_options=...,
)

# %%
# call the task


classify_traj_speed = apply_classification.partial(
    **classify_traj_speed_params
).mapvalues(argnames=["df"], argvalues=split_subject_traj_groups)


# %% [markdown]
# ## Apply Color to Trajectories By Speed

# %%
# parameters

colormap_traj_speed_params = dict(
    input_column_name=...,
    colormap=...,
    output_column_name=...,
)

# %%
# call the task


colormap_traj_speed = apply_color_map.partial(**colormap_traj_speed_params).mapvalues(
    argnames=["df"], argvalues=classify_traj_speed
)


# %% [markdown]
# ## Format Speedmap Legend Label

# %%
# parameters

speedmap_legend_with_unit_params = dict(
    input_column_name=...,
    output_column_name=...,
    original_unit=...,
    new_unit=...,
    decimal_places=...,
)

# %%
# call the task


speedmap_legend_with_unit = map_values_with_unit.partial(
    **speedmap_legend_with_unit_params
).mapvalues(argnames=["df"], argvalues=colormap_traj_speed)


# %% [markdown]
# ## Create map layer for each trajectory group

# %%
# parameters

traj_map_layers_params = dict(
    layer_style=...,
    legend=...,
)

# %%
# call the task


traj_map_layers = create_map_layer.partial(**traj_map_layers_params).mapvalues(
    argnames=["geodataframe"], argvalues=speedmap_legend_with_unit
)


# %% [markdown]
# ## Draw Ecomaps for each trajectory group

# %%
# parameters

traj_ecomap_params = dict(
    tile_layers=...,
    static=...,
    title=...,
    north_arrow_style=...,
    legend_style=...,
)

# %%
# call the task


traj_ecomap = draw_ecomap.partial(**traj_ecomap_params).mapvalues(
    argnames=["geo_layers"], argvalues=traj_map_layers
)


# %% [markdown]
# ## Persist ecomap as Text

# %%
# parameters

ecomap_html_urls_params = dict(
    filename=...,
)

# %%
# call the task


ecomap_html_urls = persist_text.partial(
    root_path=os.environ["ECOSCOPE_WORKFLOWS_RESULTS"], **ecomap_html_urls_params
).mapvalues(argnames=["text"], argvalues=traj_ecomap)


# %% [markdown]
# ## Create Map Widgets for Trajectories

# %%
# parameters

traj_map_widgets_single_views_params = dict(
    title=...,
)

# %%
# call the task


traj_map_widgets_single_views = create_map_widget_single_view.partial(
    **traj_map_widgets_single_views_params
).map(argnames=["view", "data"], argvalues=ecomap_html_urls)


# %% [markdown]
# ## Merge EcoMap Widget Views

# %%
# parameters

traj_grouped_map_widget_params = dict()

# %%
# call the task


traj_grouped_map_widget = merge_widget_views.partial(
    widgets=traj_map_widgets_single_views, **traj_grouped_map_widget_params
).call()


# %% [markdown]
# ## Apply Color to Trajectories By Day/Night

# %%
# parameters

colormap_traj_night_params = dict(
    input_column_name=...,
    colormap=...,
    output_column_name=...,
)

# %%
# call the task


colormap_traj_night = apply_color_map.partial(**colormap_traj_night_params).mapvalues(
    argnames=["df"], argvalues=split_subject_traj_groups
)


# %% [markdown]
# ## Create map layer for each trajectory group

# %%
# parameters

traj_map_night_layers_params = dict(
    layer_style=...,
    legend=...,
)

# %%
# call the task


traj_map_night_layers = create_map_layer.partial(
    **traj_map_night_layers_params
).mapvalues(argnames=["geodataframe"], argvalues=colormap_traj_night)


# %% [markdown]
# ## Draw Ecomaps for each trajectory group

# %%
# parameters

traj_daynight_ecomap_params = dict(
    tile_layers=...,
    static=...,
    title=...,
    north_arrow_style=...,
    legend_style=...,
)

# %%
# call the task


traj_daynight_ecomap = draw_ecomap.partial(**traj_daynight_ecomap_params).mapvalues(
    argnames=["geo_layers"], argvalues=traj_map_night_layers
)


# %% [markdown]
# ## Persist ecomap as Text

# %%
# parameters

ecomap_daynight_html_urls_params = dict(
    filename=...,
)

# %%
# call the task


ecomap_daynight_html_urls = persist_text.partial(
    root_path=os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
    **ecomap_daynight_html_urls_params,
).mapvalues(argnames=["text"], argvalues=traj_daynight_ecomap)


# %% [markdown]
# ## Create Map Widgets for Trajectories

# %%
# parameters

traj_map_daynight_widgets_sv_params = dict(
    title=...,
)

# %%
# call the task


traj_map_daynight_widgets_sv = create_map_widget_single_view.partial(
    **traj_map_daynight_widgets_sv_params
).map(argnames=["view", "data"], argvalues=ecomap_daynight_html_urls)


# %% [markdown]
# ## Merge EcoMap Widget Views

# %%
# parameters

traj_daynight_grouped_map_widget_params = dict()

# %%
# call the task


traj_daynight_grouped_map_widget = merge_widget_views.partial(
    widgets=traj_map_daynight_widgets_sv, **traj_daynight_grouped_map_widget_params
).call()


# %% [markdown]
# ## Calculate Mean Speed Per Group

# %%
# parameters

mean_speed_params = dict(
    column_name=...,
)

# %%
# call the task


mean_speed = dataframe_column_mean.partial(**mean_speed_params).mapvalues(
    argnames=["df"], argvalues=split_subject_traj_groups
)


# %% [markdown]
# ## Convert Average Speed units

# %%
# parameters

average_speed_converted_params = dict(
    original_unit=...,
    new_unit=...,
)

# %%
# call the task


average_speed_converted = with_unit.partial(**average_speed_converted_params).mapvalues(
    argnames=["value"], argvalues=mean_speed
)


# %% [markdown]
# ## Create Single Value Widgets for Mean Speed Per Group

# %%
# parameters

mean_speed_sv_widgets_params = dict(
    title=...,
    decimal_places=...,
)

# %%
# call the task


mean_speed_sv_widgets = create_single_value_widget_single_view.partial(
    **mean_speed_sv_widgets_params
).map(argnames=["view", "data"], argvalues=average_speed_converted)


# %% [markdown]
# ## Merge per group Mean Speed SV widgets

# %%
# parameters

mean_speed_grouped_sv_widget_params = dict()

# %%
# call the task


mean_speed_grouped_sv_widget = merge_widget_views.partial(
    widgets=mean_speed_sv_widgets, **mean_speed_grouped_sv_widget_params
).call()


# %% [markdown]
# ## Calculate Max Speed Per Group

# %%
# parameters

max_speed_params = dict(
    column_name=...,
)

# %%
# call the task


max_speed = dataframe_column_max.partial(**max_speed_params).mapvalues(
    argnames=["df"], argvalues=split_subject_traj_groups
)


# %% [markdown]
# ## Convert Max Speed units

# %%
# parameters

max_speed_converted_params = dict(
    original_unit=...,
    new_unit=...,
)

# %%
# call the task


max_speed_converted = with_unit.partial(**max_speed_converted_params).mapvalues(
    argnames=["value"], argvalues=max_speed
)


# %% [markdown]
# ## Create Single Value Widgets for Max Speed Per Group

# %%
# parameters

max_speed_sv_widgets_params = dict(
    title=...,
    decimal_places=...,
)

# %%
# call the task


max_speed_sv_widgets = create_single_value_widget_single_view.partial(
    **max_speed_sv_widgets_params
).map(argnames=["view", "data"], argvalues=max_speed_converted)


# %% [markdown]
# ## Merge per group Max Speed SV widgets

# %%
# parameters

max_speed_grouped_sv_widget_params = dict()

# %%
# call the task


max_speed_grouped_sv_widget = merge_widget_views.partial(
    widgets=max_speed_sv_widgets, **max_speed_grouped_sv_widget_params
).call()


# %% [markdown]
# ## Calculate Number of Locations Per Group

# %%
# parameters

num_location_params = dict()

# %%
# call the task


num_location = dataframe_count.partial(**num_location_params).mapvalues(
    argnames=["df"], argvalues=split_subject_traj_groups
)


# %% [markdown]
# ## Create Single Value Widgets for Number of Location Per Group

# %%
# parameters

num_location_sv_widgets_params = dict(
    title=...,
    decimal_places=...,
)

# %%
# call the task


num_location_sv_widgets = create_single_value_widget_single_view.partial(
    **num_location_sv_widgets_params
).map(argnames=["view", "data"], argvalues=num_location)


# %% [markdown]
# ## Merge per group Number of Locations SV widgets

# %%
# parameters

num_location_grouped_sv_widget_params = dict()

# %%
# call the task


num_location_grouped_sv_widget = merge_widget_views.partial(
    widgets=num_location_sv_widgets, **num_location_grouped_sv_widget_params
).call()


# %% [markdown]
# ## Calculate Day/Night Ratio Per Group

# %%
# parameters

daynight_ratio_params = dict()

# %%
# call the task


daynight_ratio = get_day_night_ratio.partial(**daynight_ratio_params).mapvalues(
    argnames=["df"], argvalues=split_subject_traj_groups
)


# %% [markdown]
# ## Create Single Value Widgets for Day/Night Ratio Per Group

# %%
# parameters

daynight_ratio_sv_widgets_params = dict(
    title=...,
    decimal_places=...,
)

# %%
# call the task


daynight_ratio_sv_widgets = create_single_value_widget_single_view.partial(
    **daynight_ratio_sv_widgets_params
).map(argnames=["view", "data"], argvalues=daynight_ratio)


# %% [markdown]
# ## Merge per group Day/Night Ratio SV widgets

# %%
# parameters

daynight_ratio_grouped_sv_widget_params = dict()

# %%
# call the task


daynight_ratio_grouped_sv_widget = merge_widget_views.partial(
    widgets=daynight_ratio_sv_widgets, **daynight_ratio_grouped_sv_widget_params
).call()


# %% [markdown]
# ## Calculate Total Distance Per Group

# %%
# parameters

total_distance_params = dict(
    column_name=...,
)

# %%
# call the task


total_distance = dataframe_column_sum.partial(**total_distance_params).mapvalues(
    argnames=["df"], argvalues=split_subject_traj_groups
)


# %% [markdown]
# ## Convert total distance units

# %%
# parameters

total_dist_converted_params = dict(
    original_unit=...,
    new_unit=...,
)

# %%
# call the task


total_dist_converted = with_unit.partial(**total_dist_converted_params).mapvalues(
    argnames=["value"], argvalues=total_distance
)


# %% [markdown]
# ## Create Single Value Widgets for Total Distance Per Group

# %%
# parameters

total_distance_sv_widgets_params = dict(
    title=...,
    decimal_places=...,
)

# %%
# call the task


total_distance_sv_widgets = create_single_value_widget_single_view.partial(
    **total_distance_sv_widgets_params
).map(argnames=["view", "data"], argvalues=total_dist_converted)


# %% [markdown]
# ## Merge per group Total Distance SV widgets

# %%
# parameters

total_dist_grouped_sv_widget_params = dict()

# %%
# call the task


total_dist_grouped_sv_widget = merge_widget_views.partial(
    widgets=total_distance_sv_widgets, **total_dist_grouped_sv_widget_params
).call()


# %% [markdown]
# ## Calculate Total Time Per Group

# %%
# parameters

total_time_params = dict(
    column_name=...,
)

# %%
# call the task


total_time = dataframe_column_sum.partial(**total_time_params).mapvalues(
    argnames=["df"], argvalues=split_subject_traj_groups
)


# %% [markdown]
# ## Convert total time units

# %%
# parameters

total_time_converted_params = dict(
    original_unit=...,
    new_unit=...,
)

# %%
# call the task


total_time_converted = with_unit.partial(**total_time_converted_params).mapvalues(
    argnames=["value"], argvalues=total_time
)


# %% [markdown]
# ## Create Single Value Widgets for Total Distance Per Group

# %%
# parameters

total_time_sv_widgets_params = dict(
    title=...,
    decimal_places=...,
)

# %%
# call the task


total_time_sv_widgets = create_single_value_widget_single_view.partial(
    **total_time_sv_widgets_params
).map(argnames=["view", "data"], argvalues=total_time_converted)


# %% [markdown]
# ## Merge per group Total Distance SV widgets

# %%
# parameters

total_time_grouped_sv_widget_params = dict()

# %%
# call the task


total_time_grouped_sv_widget = merge_widget_views.partial(
    widgets=total_time_sv_widgets, **total_time_grouped_sv_widget_params
).call()


# %% [markdown]
# ## Calculate Time Density from Trajectory

# %%
# parameters

td_params = dict(
    pixel_size=...,
    crs=...,
    nodata_value=...,
    band_count=...,
    max_speed_factor=...,
    expansion_factor=...,
    percentiles=...,
)

# %%
# call the task


td = calculate_time_density.partial(**td_params).mapvalues(
    argnames=["trajectory_gdf"], argvalues=split_subject_traj_groups
)


# %% [markdown]
# ## Time Density Colormap

# %%
# parameters

td_colormap_params = dict(
    input_column_name=...,
    colormap=...,
    output_column_name=...,
)

# %%
# call the task


td_colormap = apply_color_map.partial(**td_colormap_params).mapvalues(
    argnames=["df"], argvalues=td
)


# %% [markdown]
# ## Create map layer from Time Density

# %%
# parameters

td_map_layer_params = dict(
    layer_style=...,
    legend=...,
)

# %%
# call the task


td_map_layer = create_map_layer.partial(**td_map_layer_params).mapvalues(
    argnames=["geodataframe"], argvalues=td_colormap
)


# %% [markdown]
# ## Draw Ecomap from Time Density

# %%
# parameters

td_ecomap_params = dict(
    tile_layers=...,
    static=...,
    title=...,
    north_arrow_style=...,
    legend_style=...,
)

# %%
# call the task


td_ecomap = draw_ecomap.partial(**td_ecomap_params).mapvalues(
    argnames=["geo_layers"], argvalues=td_map_layer
)


# %% [markdown]
# ## Persist Ecomap as Text

# %%
# parameters

td_ecomap_html_url_params = dict(
    filename=...,
)

# %%
# call the task


td_ecomap_html_url = persist_text.partial(
    root_path=os.environ["ECOSCOPE_WORKFLOWS_RESULTS"], **td_ecomap_html_url_params
).mapvalues(argnames=["text"], argvalues=td_ecomap)


# %% [markdown]
# ## Create Time Density Map Widget

# %%
# parameters

td_map_widget_params = dict(
    title=...,
)

# %%
# call the task


td_map_widget = create_map_widget_single_view.partial(**td_map_widget_params).map(
    argnames=["view", "data"], argvalues=td_ecomap_html_url
)


# %% [markdown]
# ## Merge Time Density Map Widget Views

# %%
# parameters

td_grouped_map_widget_params = dict()

# %%
# call the task


td_grouped_map_widget = merge_widget_views.partial(
    widgets=td_map_widget, **td_grouped_map_widget_params
).call()


# %% [markdown]
# ## Draw NSD Scatter Chart

# %%
# parameters

nsd_chart_params = dict(
    group_by=...,
    x_axis=...,
    y_axis=...,
    plot_style=...,
    color_column=...,
)

# %%
# call the task


nsd_chart = draw_ecoplot.partial(
    dataframe=traj_add_temporal_index, **nsd_chart_params
).call()


# %% [markdown]
# ## Persist NSD Scatter Chart as Text

# %%
# parameters

nsd_chart_html_url_params = dict(
    filename=...,
)

# %%
# call the task


nsd_chart_html_url = persist_text.partial(
    text=nsd_chart,
    root_path=os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
    **nsd_chart_html_url_params,
).call()


# %% [markdown]
# ## Create NSD Plot Widget

# %%
# parameters

nsd_chart_widget_params = dict(
    title=...,
    view=...,
)

# %%
# call the task


nsd_chart_widget = create_plot_widget_single_view.partial(
    data=nsd_chart_html_url, **nsd_chart_widget_params
).call()


# %% [markdown]
# ## Create Dashboard with Subject Tracking Widgets

# %%
# parameters

subject_tracking_dashboard_params = dict()

# %%
# call the task


subject_tracking_dashboard = gather_dashboard.partial(
    details=workflow_details,
    widgets=[
        traj_grouped_map_widget,
        mean_speed_grouped_sv_widget,
        max_speed_grouped_sv_widget,
        num_location_grouped_sv_widget,
        daynight_ratio_grouped_sv_widget,
        total_dist_grouped_sv_widget,
        total_time_grouped_sv_widget,
        td_grouped_map_widget,
        traj_daynight_grouped_map_widget,
        nsd_chart_widget,
    ],
    groupers=groupers,
    time_range=time_range,
    **subject_tracking_dashboard_params,
).call()
