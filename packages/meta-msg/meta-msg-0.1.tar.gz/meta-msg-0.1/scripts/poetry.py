from pathlib import Path

import pkg_resources
from grpc_tools import protoc


def _generate(dev_mode: bool):
    paths = Path(".").glob("**/*.proto")
    proto_include = pkg_resources.resource_filename("grpc_tools", "_proto")

    for proto in paths:
        print(f"Processing {proto}")

        params = [
            "",
            "-I.",
            f"-I{proto_include}",
            "--python_out=.",
            "--grpclib_python_out=.",
        ]

        if dev_mode:
            params.extend(
                [
                    "--mypy_out=.",
                    "--mypy_opt=quiet",
                ]
            )

        params.append(f"{proto}")

        protoc.main(params)


def generate_proto_dev():
    _generate(dev_mode=True)


def generate_proto():
    _generate(dev_mode=False)
