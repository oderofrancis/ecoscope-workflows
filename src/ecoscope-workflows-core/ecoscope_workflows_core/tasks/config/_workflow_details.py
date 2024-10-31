from dataclasses import dataclass
from typing import Annotated

from pydantic import Field

from ecoscope_workflows_core.decorators import task


@dataclass
class WorkflowDetails:
    name: str
    description: str
    image_url: str = ""


@task
def set_workflow_details(
    name: Annotated[str, Field(description="The name of your workflow")],
    description: Annotated[str, Field(description="A description")],
    image_url: Annotated[str, Field(description="An image url")] = "",
) -> WorkflowDetails:
    return WorkflowDetails(
        name=name,
        description=description,
        image_url=image_url,
    )
