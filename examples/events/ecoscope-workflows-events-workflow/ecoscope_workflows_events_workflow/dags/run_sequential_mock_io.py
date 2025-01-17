# [generated]
# by = { compiler = "ecoscope-workflows-core", version = "9999" }
# from-spec-sha256 = "b5668113de9c7ad66e877a1a1213652245a4dcce1605622c1676fda3585da365"

# ruff: noqa: E402

"""WARNING: This file is generated in a testing context and should not be used in production.
Lines specific to the testing context are marked with a test tube emoji (🧪) to indicate
that they would not be included (or would be different) in the production version of this file.
"""

import json
import os
import warnings  # 🧪
from ecoscope_workflows_core.testing import create_task_magicmock  # 🧪


from ecoscope_workflows_core.tasks.config import set_workflow_details
from ecoscope_workflows_core.tasks.groupby import set_groupers
from ecoscope_workflows_core.tasks.filter import set_time_range

get_events = create_task_magicmock(  # 🧪
    anchor="ecoscope_workflows_ext_ecoscope.tasks.io",  # 🧪
    func_name="get_events",  # 🧪
)  # 🧪
from ecoscope_workflows_ext_ecoscope.tasks.transformation import (
    apply_reloc_coord_filter,
)
from ecoscope_workflows_core.tasks.transformation import add_temporal_index
from ecoscope_workflows_ext_ecoscope.tasks.transformation import apply_color_map
from ecoscope_workflows_ext_ecoscope.tasks.results import create_map_layer
from ecoscope_workflows_ext_ecoscope.tasks.results import draw_ecomap
from ecoscope_workflows_core.tasks.io import persist_text
from ecoscope_workflows_core.tasks.results import create_map_widget_single_view
from ecoscope_workflows_ext_ecoscope.tasks.results import draw_time_series_bar_chart
from ecoscope_workflows_core.tasks.results import create_plot_widget_single_view
from ecoscope_workflows_ext_ecoscope.tasks.analysis import create_meshgrid
from ecoscope_workflows_ext_ecoscope.tasks.analysis import calculate_feature_density
from ecoscope_workflows_core.tasks.groupby import split_groups
from ecoscope_workflows_core.tasks.results import merge_widget_views
from ecoscope_workflows_ext_ecoscope.tasks.results import draw_pie_chart
from ecoscope_workflows_core.tasks.results import gather_dashboard

from ..params import Params


def main(params: Params):
    warnings.warn("This test script should not be used in production!")  # 🧪

    params_dict = json.loads(params.model_dump_json(exclude_unset=True))

    workflow_details = (
        set_workflow_details.validate()
        .partial(**params_dict["workflow_details"])
        .call()
    )

    groupers = set_groupers.validate().partial(**params_dict["groupers"]).call()

    time_range = set_time_range.validate().partial(**params_dict["time_range"]).call()

    get_events_data = (
        get_events.validate()
        .partial(time_range=time_range, **params_dict["get_events_data"])
        .call()
    )

    filter_events = (
        apply_reloc_coord_filter.validate()
        .partial(df=get_events_data, **params_dict["filter_events"])
        .call()
    )

    events_add_temporal_index = (
        add_temporal_index.validate()
        .partial(df=filter_events, **params_dict["events_add_temporal_index"])
        .call()
    )

    events_colormap = (
        apply_color_map.validate()
        .partial(df=events_add_temporal_index, **params_dict["events_colormap"])
        .call()
    )

    events_map_layer = (
        create_map_layer.validate()
        .partial(geodataframe=events_colormap, **params_dict["events_map_layer"])
        .call()
    )

    events_ecomap = (
        draw_ecomap.validate()
        .partial(geo_layers=events_map_layer, **params_dict["events_ecomap"])
        .call()
    )

    events_ecomap_html_url = (
        persist_text.validate()
        .partial(
            text=events_ecomap,
            root_path=os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
            **params_dict["events_ecomap_html_url"],
        )
        .call()
    )

    events_map_widget = (
        create_map_widget_single_view.validate()
        .partial(data=events_ecomap_html_url, **params_dict["events_map_widget"])
        .call()
    )

    events_bar_chart = (
        draw_time_series_bar_chart.validate()
        .partial(dataframe=events_colormap, **params_dict["events_bar_chart"])
        .call()
    )

    events_bar_chart_html_url = (
        persist_text.validate()
        .partial(
            text=events_bar_chart,
            root_path=os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
            **params_dict["events_bar_chart_html_url"],
        )
        .call()
    )

    events_bar_chart_widget = (
        create_plot_widget_single_view.validate()
        .partial(
            data=events_bar_chart_html_url, **params_dict["events_bar_chart_widget"]
        )
        .call()
    )

    events_meshgrid = (
        create_meshgrid.validate()
        .partial(aoi=events_add_temporal_index, **params_dict["events_meshgrid"])
        .call()
    )

    events_feature_density = (
        calculate_feature_density.validate()
        .partial(
            geodataframe=events_add_temporal_index,
            meshgrid=events_meshgrid,
            **params_dict["events_feature_density"],
        )
        .call()
    )

    fd_colormap = (
        apply_color_map.validate()
        .partial(df=events_feature_density, **params_dict["fd_colormap"])
        .call()
    )

    fd_map_layer = (
        create_map_layer.validate()
        .partial(geodataframe=fd_colormap, **params_dict["fd_map_layer"])
        .call()
    )

    fd_ecomap = (
        draw_ecomap.validate()
        .partial(geo_layers=fd_map_layer, **params_dict["fd_ecomap"])
        .call()
    )

    fd_ecomap_html_url = (
        persist_text.validate()
        .partial(
            text=fd_ecomap,
            root_path=os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
            **params_dict["fd_ecomap_html_url"],
        )
        .call()
    )

    fd_map_widget = (
        create_map_widget_single_view.validate()
        .partial(data=fd_ecomap_html_url, **params_dict["fd_map_widget"])
        .call()
    )

    split_event_groups = (
        split_groups.validate()
        .partial(
            df=events_colormap, groupers=groupers, **params_dict["split_event_groups"]
        )
        .call()
    )

    grouped_events_map_layer = (
        create_map_layer.validate()
        .partial(**params_dict["grouped_events_map_layer"])
        .mapvalues(argnames=["geodataframe"], argvalues=split_event_groups)
    )

    grouped_events_ecomap = (
        draw_ecomap.validate()
        .partial(**params_dict["grouped_events_ecomap"])
        .mapvalues(argnames=["geo_layers"], argvalues=grouped_events_map_layer)
    )

    grouped_events_ecomap_html_url = (
        persist_text.validate()
        .partial(
            root_path=os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
            **params_dict["grouped_events_ecomap_html_url"],
        )
        .mapvalues(argnames=["text"], argvalues=grouped_events_ecomap)
    )

    grouped_events_map_widget = (
        create_map_widget_single_view.validate()
        .partial(**params_dict["grouped_events_map_widget"])
        .map(argnames=["view", "data"], argvalues=grouped_events_ecomap_html_url)
    )

    grouped_events_map_widget_merge = (
        merge_widget_views.validate()
        .partial(
            widgets=grouped_events_map_widget,
            **params_dict["grouped_events_map_widget_merge"],
        )
        .call()
    )

    grouped_events_pie_chart = (
        draw_pie_chart.validate()
        .partial(**params_dict["grouped_events_pie_chart"])
        .mapvalues(argnames=["dataframe"], argvalues=split_event_groups)
    )

    grouped_pie_chart_html_urls = (
        persist_text.validate()
        .partial(
            root_path=os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
            **params_dict["grouped_pie_chart_html_urls"],
        )
        .mapvalues(argnames=["text"], argvalues=grouped_events_pie_chart)
    )

    grouped_events_pie_chart_widgets = (
        create_plot_widget_single_view.validate()
        .partial(**params_dict["grouped_events_pie_chart_widgets"])
        .map(argnames=["view", "data"], argvalues=grouped_pie_chart_html_urls)
    )

    grouped_events_pie_widget_merge = (
        merge_widget_views.validate()
        .partial(
            widgets=grouped_events_pie_chart_widgets,
            **params_dict["grouped_events_pie_widget_merge"],
        )
        .call()
    )

    grouped_events_feature_density = (
        calculate_feature_density.validate()
        .partial(
            meshgrid=events_meshgrid, **params_dict["grouped_events_feature_density"]
        )
        .mapvalues(argnames=["geodataframe"], argvalues=split_event_groups)
    )

    grouped_fd_colormap = (
        apply_color_map.validate()
        .partial(**params_dict["grouped_fd_colormap"])
        .mapvalues(argnames=["df"], argvalues=grouped_events_feature_density)
    )

    grouped_fd_map_layer = (
        create_map_layer.validate()
        .partial(**params_dict["grouped_fd_map_layer"])
        .mapvalues(argnames=["geodataframe"], argvalues=grouped_fd_colormap)
    )

    grouped_fd_ecomap = (
        draw_ecomap.validate()
        .partial(**params_dict["grouped_fd_ecomap"])
        .mapvalues(argnames=["geo_layers"], argvalues=grouped_fd_map_layer)
    )

    grouped_fd_ecomap_html_url = (
        persist_text.validate()
        .partial(
            root_path=os.environ["ECOSCOPE_WORKFLOWS_RESULTS"],
            **params_dict["grouped_fd_ecomap_html_url"],
        )
        .mapvalues(argnames=["text"], argvalues=grouped_fd_ecomap)
    )

    grouped_fd_map_widget = (
        create_map_widget_single_view.validate()
        .partial(**params_dict["grouped_fd_map_widget"])
        .map(argnames=["view", "data"], argvalues=grouped_fd_ecomap_html_url)
    )

    grouped_fd_map_widget_merge = (
        merge_widget_views.validate()
        .partial(
            widgets=grouped_fd_map_widget, **params_dict["grouped_fd_map_widget_merge"]
        )
        .call()
    )

    events_dashboard = (
        gather_dashboard.validate()
        .partial(
            details=workflow_details,
            widgets=[
                events_map_widget,
                events_bar_chart_widget,
                fd_map_widget,
                grouped_events_map_widget_merge,
                grouped_events_pie_widget_merge,
                grouped_fd_map_widget_merge,
            ],
            groupers=groupers,
            time_range=time_range,
            **params_dict["events_dashboard"],
        )
        .call()
    )

    return events_dashboard
