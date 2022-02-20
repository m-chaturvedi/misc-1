import datetime
import traceback
from grpc import RpcError
from client import IotAPI
import random
from time import sleep
import pytest
import logging
logging.basicConfig(level='INFO')

def send_data(sensor_num, status):
  s = IotAPI()
  date_format = "%Y-%m-%dT%H:%M:%S"
  R = random.randint
  try:
    json_dict = {"deviceId": sensor_num,
      "timestamp": datetime.datetime.now().strftime(date_format), "status": status, "pressure": R(1, 1000),
      "temperature": R(-100, 100)}
    print(f"Sending: {json_dict}")
    response = s.send_sensor_json(json_dict)
    return response
  except ValueError:
    print(f"Could not parse JSON.")
    print(traceback.format_exc())
  except RpcError:
    print(f"RPC error occured.")
    print(traceback.format_exc())

def receive_status(sensor_id):
  s = IotAPI()
  try:
    response = s.get_sensor_histogram(sensor_id)
    return response
  except ValueError:
    print(f"Could not parse JSON.")
    print(traceback.format_exc())
  except RpcError:
    print(f"RPC error occured.")
    print(traceback.format_exc())

def test_api():
  for _ in range(4): assert send_data("1", "ON") == 0
  for _ in range(3): assert send_data("1", "OFF") == 0
  for _ in range(2): assert send_data("1", "ACTIVE") == 0
  for _ in range(1): assert send_data("1", "INACTIVE") == 0
  assert receive_status("1") == [4, 3, 2, 1]

  assert send_data("2", "ON") == 0
  assert send_data("3", "OFF") == 0
  assert send_data("4", "ACTIVE") == 0
  assert send_data("5", "INACTIVE") == 0
  assert receive_status("1") == [4, 3, 2, 1]
  assert receive_status("2") == [1, 0, 0, 0]
  assert receive_status("3") == [0, 1, 0, 0]
  assert receive_status("4") == [0, 0, 1, 0]
  assert receive_status("5") == [0, 0, 0, 1]
  assert receive_status("6") == [0, 0, 0, 0] # Absent

  s = IotAPI()
  with pytest.raises(ValueError, match="JSON keys don't match the requirements"):
    s.send_sensor_json({})

  with pytest.raises(ValueError, match="JSON keys don't match the requirements"):
    s.send_sensor_json({"random": 3})

