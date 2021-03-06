import datetime

from grpc import RpcError
from client import IotAPI
import random
import pytest
import logging
logging.basicConfig(level='INFO')

date_format = "%Y-%m-%dT%H:%M:%S"
R = random.randint

def send_data(sensor_num, status):
  s = IotAPI()
  json_dict = {"deviceId": sensor_num,
    "timestamp": datetime.datetime.now().strftime(date_format), "status": status, "pressure": R(1, 1000),
    "temperature": R(-100, 100)}
  print(f"Sending: {json_dict}")
  response = s.send_sensor_json([json_dict])
  return response

def receive_status(sensor_id):
  s = IotAPI()
  response = s.get_sensor_histogram(sensor_id)
  return response

def receive_history(sensor_id):
  s = IotAPI()
  response = s.get_sensor_history(sensor_id)
  return response

def receive_topids(field):
  s = IotAPI()
  response = s.get_top_sensor_ids(field)
  return response


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
  assert receive_history("1") == ["ON"]* 4 + ["OFF"]*3 + ["ACTIVE"]*2 + ["INACTIVE"]

  s = IotAPI()
  with pytest.raises(RpcError):
    s.send_sensor_json([{}])

  with pytest.raises(RpcError):
    s.send_sensor_json([{"random": 3}])

  with pytest.raises(RpcError):
    json_dict = {"deviceId": "1",
      "timestamp": datetime.datetime.now().strftime(date_format),
      "status": "RANDOM", "pressure": R(1, 1000), "temperature": R(-100, 100)}
    s.send_sensor_json([json_dict])

  with pytest.raises(RpcError) as e:
    json_dict = {"deviceId": "1",
      "timestamp": datetime.datetime.now().strftime(date_format),
      "status": "INACTIVE", "pressure": R(1, 1000), "temperature": 1e20}
    s.send_sensor_json([json_dict])

  assert receive_status("1") == [4, 3, 2, 1]
  assert receive_status("2") == [1, 0, 0, 0]
  assert receive_status("3") == [0, 1, 0, 0]
  assert receive_status("4") == [0, 0, 1, 0]
  assert receive_status("5") == [0, 0, 0, 1]
  assert receive_status("6") == [0, 0, 0, 0] # Absent
  print(receive_topids("temperature"))
