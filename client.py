#!/usr/bin/env python3.9

import datetime
import grpc
import iot_pb2
import iot_pb2_grpc
from config import Config
import traceback
from time import sleep
import logging

class IotAPI:
  def __init__(self, hostname=Config.hostname, port=Config.port):
    self.address = f"{hostname}:{port}"
    self.all_keys = set(["deviceId", "timestamp", "pressure", "status", "temperature"])
    self.mandatory_keys = set(["deviceId", "timestamp"])

  @staticmethod
  def check_dict_keys(json_dict, all_keys, mandatory_keys):
    json_keys = set(json_dict.keys())
    if not all_keys.issuperset(set(json_keys)):
      return 1
    if not json_keys.issuperset(mandatory_keys):
      return 2
    return 0

  def parse_io_json(self, json_struct):
    if IotAPI.check_dict_keys(json_struct, self.all_keys, self.mandatory_keys):
      raise ValueError("JSON keys don't match the requirements.")

    if "status" in json_struct and (json_struct["status"] not in Config.status_dict):
      raise ValueError("'status' key incorrectly formatted")

    status = Config.status_dict[json_struct["status"]] if "status" in json_struct else 0

    # Assume the time zone to be +00:00
    timestamp = datetime.datetime.fromisoformat(str(json_struct["timestamp"]) + "+00:00").timestamp()

    protobuf_struct = {
        "deviceId": str(json_struct["deviceId"]),
        "timestamp": int(timestamp),
        "pressure": float(json_struct.get("pressure", Config.float_default)),
        "status": status,
        "temperature": int(json_struct.get("temperature", Config.int_default)),
    }
    return protobuf_struct

  def generate_structs(self, json_structs):
    for json_struct in json_structs:
      protobuf_struct = self.parse_io_json(json_struct)
      yield iot_pb2.SensorData(**protobuf_struct)

  def send_sensor_json(self, json_structs):
    with grpc.insecure_channel("{}:{}".format(Config.hostname, Config.port)) as channel:
      struct_iterator = self.generate_structs(json_structs)
      stub = iot_pb2_grpc.IotSenderStub(channel)
      response = stub.GetSensorData(struct_iterator)
    return response.returnValue

  def get_sensor_histogram(self, sensor_id):
    with grpc.insecure_channel("{}:{}".format(Config.hostname, Config.port)) as channel:
      stub = iot_pb2_grpc.IotSenderStub(channel)
      data = iot_pb2.SensorId(deviceId=sensor_id)
      response = stub.SendSensorStatus(data)
    return response.status_freq


