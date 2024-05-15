"""Airflow DAG generated by `ecoscope_workflows/generate_dag.py`"""

from airflow.configuration import conf 
from airflow.decorators import dag, task

from ecoscope_workflows.decorators import distributed as DistributedTask

namespace = conf.get("kubernetes", "NAMESPACE")  # does this work?

def import_item(): ...  # TODO: implement in workflows

# TODO: possibly need some global de/serialization fsspec filesystem
# defined here, inheriting system credentials?


@task.kubernetes(
    image="ecoscope:0.1.7",
    in_cluster=True,
    namespace=namespace,
    name="pod",
    get_logs=True,
    log_events_on_failure=True,
    do_xcom_push=True,
)
def get_earthranger_subjectgroup_observations(params: dict | None = None):
    task: DistributedTask = import_item("ecoscope_workflows.tasks.python.io.get_subjectgroup_observations")
    task_kwargs = params["get_earthranger_subjectgroup_observations"]
    # something about loading registered deserializers by arg type
    # something about return_postvalidator closures
    outpath = task.replace(
        arg_prevalidators=...,  # this is a loop in itself
        return_postvalidator=...,  # set this from a storage config
        validate=True
    )(**task_kwargs)
    return outpath


    # TODO: task dependencies

@dag(schedule="@daily", start_date=datetime(2021, 12, 1), catchup=False)
def calculate_time_density():
    ...