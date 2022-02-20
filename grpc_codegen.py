#!/usr/bin/env python3.9

from grpc_tools import protoc

protoc.main(["protoc", "--python_out=.",
  "--grpc_python_out=.", "iot.proto"])



