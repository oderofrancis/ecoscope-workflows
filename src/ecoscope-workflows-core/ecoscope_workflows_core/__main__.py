import argparse
import json
from enum import Enum
from getpass import getpass

import ruamel.yaml
from pydantic import SecretStr

from ecoscope_workflows_core import config
from ecoscope_workflows_core.artifacts import (
    Dags,
    PackageDirectory,
    Tests,
    WorkflowArtifacts,
)
from ecoscope_workflows_core.compiler import DagCompiler, Spec
from ecoscope_workflows_core.config import TomlConfigTable
from ecoscope_workflows_core.registry import known_tasks

yaml = ruamel.yaml.YAML(typ="safe")


class Colors(str, Enum):
    WARNING = "\033[93m"
    ENDC = "\033[0m"


def compile_command(args):
    compilation_spec = Spec(**yaml.load(args.spec))
    dc = DagCompiler(spec=compilation_spec)
    dags = Dags(
        **{
            "jupytext.py": dc.generate_dag("jupytext"),
            "run_async_mock_io.py": dc.generate_dag("async", mock_io=True),
            "run_async.py": dc.generate_dag("async"),
            "run_sequential_mock_io.py": dc.generate_dag("sequential", mock_io=True),
            "run_sequential.py": dc.generate_dag("sequential"),
        }
    )
    wa = WorkflowArtifacts(
        package_name=dc.package_name,
        release_name=dc.release_name,
        pixi_toml=dc.get_pixi_toml(),
        pyproject_toml=dc.get_pyproject_toml(),
        package=PackageDirectory(
            dags=dags,
            params_jsonschema=dc.get_params_jsonschema(),
        ),
        tests=Tests(
            **{"test_dags.py": dc.get_test_dags()},
        ),
    )
    wa.dump(clobber=args.clobber)
    if args.lock:
        wa.lock()


def tasks_command(args):
    print()
    for t, kt in known_tasks.items():
        print(f"{t}:")
        for field, val in kt.model_dump().items():
            print(f"    {field}: {val}")
        print("\n")


def get_params_command(args):
    compilation_spec = Spec(**yaml.load(args.spec))
    dc = DagCompiler(spec=compilation_spec)
    if args.format == "json":
        params = dc.get_params_jsonschema()
    elif args.format == "yaml":
        params = dc.get_params_fillable_yaml()
    if args.outpath:
        with open(args.outpath, "w") as f:
            if args.format == "json":
                json.dump(params, f, indent=4)
            elif args.format == "yaml":
                f.write(params)
    else:
        print(params)


def visualize(args):
    from ecoscope_workflows_core.visualize import write_png

    compilation_spec = Spec(**yaml.load(args.spec))
    outpath = args.outpath
    write_png(compilation_spec, outpath)


def connections_create_command(args):
    known_connections = {}  # FIXME: fix this
    if args.type not in known_connections:
        raise ValueError(f"Unknown connection type '{args.type}'")  # FIXME: fix this
    conn_type = known_connections[args.type]
    cont = input(
        f"{Colors.WARNING}WARNING: All connection fields set here, including secrets, will be "
        f"stored in clear text at '{str(config.PATH)}'. If you prefer not to store secrets in "
        "clear text in this location, you may: (a) change the local storage path by setting the "
        "`ECOSCOPE_WORKFLOWS_CONFIG` env var; (b) leave secrets fields empty here, and inject "
        "values at with the `ECOSCOPE_WORKFLOWS__CONNECTIONS__"
        f"{args.type.upper()}__{args.name.upper()}__{{field_name}}` env var."
        f"\nContinue? [y/N]: {Colors.ENDC}"
    )
    if cont.lower() != "y":
        print("Exiting...")
        return
    if args.fields:
        fields = json.loads(args.fields)
    else:
        fields = {}
        print(f"Creating {args.type} connection '{args.name}' interactively...")
        for k, v in conn_type.model_fields.items():
            prompt = f"{v.description}"
            if v.annotation == SecretStr:
                prompt = f"{prompt} (input hidden for security)"
                fields[k] = getpass(f"{prompt}: ")
            else:
                fields[k] = input(f"{prompt}: ")
    tct = TomlConfigTable(
        header="connections", subheader=args.type, name=args.name, fields=fields
    )
    if args.store == "local":
        tct.dump()
    else:
        raise NotImplementedError(f"Storage method '{args.store}' not implemented.")


def connections_delete_command(args):
    tct = TomlConfigTable(header="connections", subheader=args.type, name=args.name)
    if args.store == "local":
        tct.delete()
    else:
        raise NotImplementedError(f"Storage method '{args.store}' not implemented.")


# def connections_list_command(args):
#     ...

# def connections_check_command(args):
#     conn_type = known_connections[args.type]
#     conn = conn_type.from_named_connection(args.name)
#     conn.check_connection()


def main():
    parser = argparse.ArgumentParser(prog="ecoscope-workflows")
    subparsers = parser.add_subparsers(title="subcommands", dest="command")

    # Subcommand 'compile'
    compile_parser = subparsers.add_parser("compile", help="Compile workflows")
    compile_parser.set_defaults(func=compile_command)
    compile_parser.add_argument(
        "--spec",
        dest="spec",
        required=True,
        type=argparse.FileType(mode="r"),
    )
    compile_parser.add_argument(
        "--clobber",
        dest="clobber",
        default=False,
        action="store_true",
    )
    compile_parser.add_argument(
        "--lock",
        dest="lock",
        default=True,
        action="store_true",
    )

    # Subcommand 'tasks'
    tasks_parser = subparsers.add_parser("tasks", help="Manage tasks")
    tasks_parser.set_defaults(func=tasks_command)

    # Subcommand 'get-params'
    get_params_parser = subparsers.add_parser("get-params", help="Get params")
    get_params_parser.set_defaults(func=get_params_command)
    # FIXME: duplicative with `compile`
    get_params_parser.add_argument(
        "--spec",
        dest="spec",
        required=True,
        type=argparse.FileType(mode="r"),
    )
    get_params_parser.add_argument(
        "--outpath",
        dest="outpath",
    )
    get_params_parser.add_argument(
        "--format",
        dest="format",
        default="json",
    )

    # Subcommand 'visualize'
    visualize_parser = subparsers.add_parser("visualize", help="Visualize workflows")
    visualize_parser.set_defaults(func=visualize)
    visualize_parser.add_argument(
        "--spec",
        dest="spec",
        required=True,
        type=argparse.FileType(mode="r"),
    )
    visualize_parser.add_argument(
        "--outpath",
        dest="outpath",
    )
    # Subcommand 'connections'
    connections_parser = subparsers.add_parser("connections", help="Manage connections")
    connections_subparsers = connections_parser.add_subparsers()
    connections_create_parser = connections_subparsers.add_parser(
        "create",
        help="Create a new named connection",
    )
    connections_create_parser.set_defaults(func=connections_create_command)
    connections_create_parser.add_argument(
        "--type",
        dest="type",
        required=True,
        choices=["earthranger"],
    )
    connections_create_parser.add_argument(
        "--name",
        dest="name",
        required=True,
    )
    connections_create_parser.add_argument(
        "--store",
        dest="store",
        default="local",
        choices=["local"],
    )
    connections_create_parser.add_argument(
        "--fields",
        dest="fields",
        default=None,
    )
    connections_delete_parser = connections_subparsers.add_parser(
        "delete",
        help="Delete a named connection",
    )
    connections_delete_parser.set_defaults(func=connections_delete_command)
    connections_delete_parser.add_argument(
        "--type",
        dest="type",
        required=True,
        choices=["earthranger"],
    )
    connections_delete_parser.add_argument(
        "--name",
        dest="name",
        required=True,
    )
    connections_delete_parser.add_argument(
        "--store",
        dest="store",
        default="local",
        choices=["local"],
    )
    # connections_list_parser = connections_subparsers.add_parser(
    #     "list",
    #     help="List configured connections",
    # )
    # connections_list_parser.set_defaults(func=connections_list_command)

    # Parse args
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
