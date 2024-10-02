# [generated]
# by = { compiler = "ecoscope-workflows-core", version = "9999" }
# from-spec-sha256 = "f125a6e84a7bc2e8aa6f1059f0833e75cf111d9d58b7faaf86cbdf88367c6173"


import os
import tempfile
import traceback
from typing import Literal

import ruamel.yaml
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel, Field, SecretStr

from .dispatch import dispatch
from .params import Params


app = FastAPI(
    title="Ecoscope Workflows Runner",
    debug=True,
    version="0.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict to only the fastapi server, anywhere else?
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)


class Lithops(BaseModel):
    backend: Literal["localhost", "gcp_cloudrun"] = "localhost"
    storage: Literal["localhost", "gcp_storage"] = "localhost"
    log_level: str = "DEBUG"
    data_limit: int = 16


class GCP(BaseModel):
    region: str = "us-central1"
    credentials_path: str = (
        "placeholder"  # os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )


class GCPCloudRun(BaseModel):
    runtime: str = "placeholder"  # os.environ["LITHOPS_GCP_CLOUDRUN_RUNTIME"]
    runtime_cpu: int = 2
    runtime_memory: int = 1000


class LithopsConfig(BaseModel):
    lithops: Lithops = Field(default_factory=Lithops)
    gcp: GCP | None = None
    gcp_cloudrun: GCPCloudRun | None = None


@app.post("/", status_code=200)
def run(
    # service response
    response: Response,
    # user (http) inputs
    params: Params,
    execution_mode: Literal["async", "sequential"],
    mock_io: bool,
    results_url: str,
    data_connections_env_vars: dict[str, SecretStr] | None = None,
    lithops_config: LithopsConfig | None = None,
    callback_url: str | None = None,  # TODO: authentication (hmac)
):
    yaml = ruamel.yaml.YAML(typ="safe")
    update_env = {"ECOSCOPE_WORKFLOWS_RESULTS": results_url}

    if execution_mode == "async":
        if not lithops_config:
            lithops_config = LithopsConfig()
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".yaml"
        ) as lithops_config_file:
            yaml.dump(lithops_config.model_dump(exclude_none=True), lithops_config_file)
            update_env["LITHOPS_CONFIG_FILE"] = lithops_config_file.name

    if data_connections_env_vars:
        update_env |= {
            k: v.get_secret_value() for k, v in data_connections_env_vars.items()
        }
    os.environ.update(update_env)
    try:
        result = dispatch(execution_mode, mock_io, params)
        if callback_url:
            raise NotImplementedError("Callbacks are not yet implemented.")
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        trace = traceback.format_exc().splitlines()
        return {"error": str(e), "traceback": trace}
    finally:
        for k in update_env:
            del os.environ[k]

    return result
