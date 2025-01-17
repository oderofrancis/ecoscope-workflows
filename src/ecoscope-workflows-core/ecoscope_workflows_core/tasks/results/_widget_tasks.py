from typing import Annotated

from pydantic import Field

from ecoscope_workflows_core.decorators import task
from ecoscope_workflows_core.indexes import CompositeFilter
from ecoscope_workflows_core.tasks.results._widget_types import (
    GroupedWidget,
    GroupedWidgetMergeKey,
    PrecomputedHTMLWidgetData,
    TextWidgetData,
    WidgetSingleView,
)
from ecoscope_workflows_core.tasks.transformation._unit import Quantity


@task
def create_map_widget_single_view(
    title: Annotated[str, Field(description="The title of the widget")],
    data: Annotated[
        PrecomputedHTMLWidgetData, Field(description="Path to precomputed HTML")
    ],
    view: Annotated[
        CompositeFilter | None,
        Field(description="If grouped, the view of the widget", exclude=True),
    ] = None,
) -> Annotated[WidgetSingleView, Field(description="The widget")]:
    """Create a map widget with a single view.

    Args:
        title: The title of the widget.
        data: Path to precomputed HTML.
        view: If grouped, the view of the widget.

    Returns:
        The widget.
    """
    return WidgetSingleView(
        widget_type="map",
        title=title,
        view=view,
        data=data,
        is_filtered=(view is not None),
    )


@task
def create_plot_widget_single_view(
    title: Annotated[str, Field(description="The title of the widget")],
    data: Annotated[
        PrecomputedHTMLWidgetData, Field(description="Path to precomputed HTML")
    ],
    view: Annotated[
        CompositeFilter | None,
        Field(description="If grouped, the view of the widget", exclude=True),
    ] = None,
) -> Annotated[WidgetSingleView, Field(description="The widget")]:
    """Create a plot widget with a single view.

    Args:
        title: The title of the widget.
        data: Path to precomputed HTML.
        view: If grouped, the view of the widget.

    Returns:
        The widget.
    """
    return WidgetSingleView(
        widget_type="graph",
        title=title,
        view=view,
        data=data,
        is_filtered=(view is not None),
    )


@task
def create_text_widget_single_view(
    title: Annotated[str, Field(description="The title of the widget")],
    data: Annotated[TextWidgetData, Field(description="Text to display.")],
    view: Annotated[
        CompositeFilter | None,
        Field(description="If grouped, the view of the widget", exclude=True),
    ] = None,
) -> Annotated[WidgetSingleView, Field(description="The widget")]:
    """Create a text widget with a single view.

    Args:
        title: The title of the widget.
        data: Text to display.
        view: If grouped, the view of the widget.

    Returns:
        The widget.
    """
    return WidgetSingleView(
        widget_type="text",
        title=title,
        view=view,
        data=data,
        is_filtered=(view is not None),
    )


@task
def create_single_value_widget_single_view(
    title: Annotated[str, Field(description="The title of the widget")],
    data: Annotated[Quantity | float | int, Field(description="Value to display.")],
    view: Annotated[
        CompositeFilter | None,
        Field(description="If grouped, the view of the widget", exclude=True),
    ] = None,
    decimal_places: Annotated[
        int, Field(description="The number of decimal places to display.")
    ] = 1,
) -> Annotated[WidgetSingleView, Field(description="The widget")]:
    """Create a single value widget with a single view.

    Args:
        title: The title of the widget.
        data: Path to precomputed HTML.
        view: If grouped, the view of the widget.

    Returns:
        The widget.
    """
    data_str = ""
    if isinstance(data, Quantity):
        data_str = f"{data.value:.{decimal_places}f} {data.unit or ''}".strip()
    elif isinstance(data, float):
        data_str = f"{data:.{decimal_places}f}"
    else:
        data_str = str(data)

    return WidgetSingleView(
        widget_type="stat",
        title=title,
        view=view,
        data=data_str,
        is_filtered=(view is not None),
    )


@task
def merge_widget_views(
    widgets: Annotated[
        list[WidgetSingleView],
        Field(description="The widgets to merge", exclude=True),
    ],
) -> Annotated[list[GroupedWidget], Field(description="The merged widgets")]:
    """Merge widgets with the same `title` and `widget_type`.

    Args:
        widgets: The widgets to merge.

    Returns:
        The merged grouped widgets.
    """
    grouped_widgets = [GroupedWidget.from_single_view(w) for w in widgets]
    merged: dict[GroupedWidgetMergeKey, GroupedWidget] = {}
    for gw in grouped_widgets:
        if gw.merge_key not in merged:
            merged[gw.merge_key] = gw
        else:
            merged[gw.merge_key] |= gw
    return list(merged.values())
