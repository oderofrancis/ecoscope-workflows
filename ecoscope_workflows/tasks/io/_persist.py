from typing import Annotated

from pydantic import Field

from ecoscope_workflows.decorators import distributed


# TODO: Unlike the tasks in `._earthranger`, this is not tagged with `tags=["io"]`,
# because in the end to end test that tag is used to determine which tasks to mock.
# Ultimately, we should make the mocking process less brittle, but to get his PR merged,
# I'm going to leave this as is for now.
@distributed
def persist_text(
    text: Annotated[str, Field(description="Text to persist")],
    root_path: Annotated[str, Field(description="Root path to persist text to")],
    filename: Annotated[str, Field(description="Name of file to persist text to")],
) -> Annotated[str, Field(description="Path to persisted text")]:
    """Persist text to a file or cloud storage object."""
    from ecoscope_workflows.serde import _persist_text

    return _persist_text(text, root_path, filename)