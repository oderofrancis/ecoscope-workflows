# [generated]
# by = { compiler = "ecoscope-workflows-core", version = "9999" }
# from-spec-sha256 = "b9febf5b3ff98ca3fd882b4f918e74114c04e0ff454b22c33ea84337b0ba9b0f"


from io import TextIOWrapper

import click
import ruamel.yaml

from ecoscope_workflows_subject_tracking_workflow.dispatch import dispatch
from ecoscope_workflows_subject_tracking_workflow.params import Params


@click.command()
@click.option(
    "--config-file",
    type=click.File("r"),
    required=True,
    help="Configuration parameters for running the workflow.",
)
@click.option(
    "--execution-mode",
    required=True,
    type=click.Choice(["async", "sequential"]),
)
@click.option(
    "--mock-io/--no-mock-io",
    is_flag=True,
    default=False,
    help="Whether or not to mock io with 3rd party services; for testing only.",
)
def main(
    config_file: TextIOWrapper,
    execution_mode: str,
    mock_io: bool,
) -> None:
    yaml = ruamel.yaml.YAML(typ="safe")
    params = Params(**yaml.load(config_file))

    result = dispatch(execution_mode, mock_io, params)

    print(result)


if __name__ == "__main__":
    main()
