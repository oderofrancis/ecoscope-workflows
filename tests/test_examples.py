import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal

import pytest
import ruamel.yaml

from ecoscope_workflows.compiler import DagCompiler
from ecoscope_workflows.registry import TaskTag, known_tasks

EXAMPLES = Path(__file__).parent.parent / "examples"

TemplateName = Literal["script-sequential.jinja2", "airflow-kubernetes.jinja2"]


def _spec_path_to_dag_fname(path: Path, template: TemplateName) -> str:
    return (
        f"{path.stem.replace('-', '_')}_dag.{Path(template).stem.replace('-', '_')}.py"
    )


def _spec_path_to_jsonschema_fname(path: Path) -> str:
    return f"{path.stem.replace('-', '_')}_params_fillable.json"


def _spec_path_to_yaml_fname(path: Path) -> str:
    return f"{path.stem.replace('-', '_')}_params_fillable.yaml"


def _spec_path_to_param_fname(path: Path) -> str:
    return f"{path.stem.replace('-', '_')}_params.yaml"


@dataclass
class SpecFixture:
    path: Path
    spec: dict


@pytest.fixture(
    params=[
        path.absolute() for path in EXAMPLES.joinpath("compilation-specs").iterdir()
    ],
    ids=[path.name for path in EXAMPLES.joinpath("compilation-specs").iterdir()],
)
def spec(request: pytest.FixtureRequest) -> SpecFixture:
    example_spec_path: Path = request.param
    yaml = ruamel.yaml.YAML(typ="safe")
    with open(example_spec_path) as f:
        spec_dict = yaml.load(f)
    return SpecFixture(example_spec_path, spec_dict)


@pytest.mark.parametrize(
    "template",
    [
        "jupytext.jinja2",
        "script-sequential.jinja2",
        # TODO: "airflow-kubernetes.jinja2",
    ],
)
def test_generate_dag(spec: SpecFixture, template: TemplateName):
    dag_compiler = DagCompiler.from_spec(spec=spec.spec)
    dag_compiler.template = template
    dag_str = dag_compiler.generate_dag()
    script_fname = _spec_path_to_dag_fname(path=spec.path, template=template)
    with open(EXAMPLES / "dags" / script_fname) as f:
        assert dag_str == f.read()


def test_dag_params_jsonschema(spec: SpecFixture):
    dag_compiler = DagCompiler.from_spec(spec=spec.spec)
    params = dag_compiler.get_params_jsonschema()
    jsonschema_fname = _spec_path_to_jsonschema_fname(spec.path)
    with open(EXAMPLES / "params" / jsonschema_fname) as f:
        assert params == json.load(f)


def test_dag_params_fillable_yaml(spec: SpecFixture):
    dag_compiler = DagCompiler.from_spec(spec=spec.spec)
    yaml_str = dag_compiler.get_params_fillable_yaml()
    yaml = ruamel.yaml.YAML(typ="rt")
    yaml_fname = _spec_path_to_yaml_fname(spec.path)
    with open(EXAMPLES / "params" / yaml_fname) as f:
        assert yaml.load(yaml_str) == yaml.load(f)


@dataclass
class EndToEndFixture:
    spec_fixture: SpecFixture
    param_path: Path
    mock_tasks: list[str]
    assert_that_stdout: list[Callable[[str], bool]]


# TODO: package this alongside task somehow
assert_that_stdout = {
    "time-density.yaml": [
        lambda out: "A dashboard for visualizing a time density map." in out,
        lambda out: "td_map.html" in out,
        lambda out: "widget_type='map', title='Great Map'," in out,
    ],
    "patrol_workflow.yaml": [
        # FIXME: See note below; we need to be able to pass an array of values to an aggregator
        # task (e.g. gather_dashboard) but we will need
        # https://github.com/wildlife-dynamics/ecoscope-workflows/pull/90 to make this possible
        # lambda out: "A dashboard for visualizing patrol trajectories." in out,
        # lambda out: "patrol_traj_map.html" in out,
        # lambda out: "widget_type='map', title='Patrol Trajectory Map'" in out,
        # NOTE: Below commented-out asserts pass prior to merge of
        # https://github.com/wildlife-dynamics/ecoscope-workflows/pull/99,
        # but following that merge, the output of the script (e.g. e.g. what is printed to stdout)
        # is different. Leaving this note here rather than deleting the commented-out asserts, bc
        # this speaks to a forthcoming item we'll need to address, namely aggregation of results
        # from non-convergent branches of the workflow.
        # lambda out: "patrol_traj_map.html" in out,
        # lambda out: "widget_type='map', title='Patrol Trajectory Map'" in out,
        lambda out: "geometry" in out,
    ],
}


@pytest.fixture
def end_to_end(spec: SpecFixture) -> EndToEndFixture:
    return EndToEndFixture(
        spec_fixture=spec,
        param_path=EXAMPLES.joinpath(
            "params", _spec_path_to_param_fname(path=spec.path)
        ),
        mock_tasks=[
            task
            for task in spec.spec["tasks"]
            # mock tasks that require io
            # TODO: this could also be a default for the compiler in --testing mode!
            if TaskTag.io in known_tasks[task].tags
        ],
        assert_that_stdout=assert_that_stdout[spec.path.name],
    )


def test_end_to_end(end_to_end: EndToEndFixture, tmp_path: Path):
    dc = DagCompiler.from_spec(spec=end_to_end.spec_fixture.spec)
    dc.template = "script-sequential.jinja2"
    dc.testing = True
    dc.mock_tasks = end_to_end.mock_tasks
    script = dc.generate_dag()
    tmp = tmp_path / "tmp"
    tmp.mkdir()
    script_outpath = tmp / "script.py"
    with open(script_outpath, mode="w") as f:
        f.write(script)

    cmd = [
        "python3",
        "-W",
        "ignore",  # in testing context warnings are added; exclude them from stdout
        script_outpath.as_posix(),
        "--config-file",
        end_to_end.param_path.as_posix(),
    ]
    out = subprocess.run(cmd, capture_output=True, text=True)
    assert out.returncode == 0
    for assert_fn in end_to_end.assert_that_stdout:
        assert assert_fn(out.stdout.strip())
