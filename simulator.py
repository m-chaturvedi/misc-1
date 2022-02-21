import datetime

from client import IotAPI
import random
import logging
from time import sleep
logging.basicConfig(level='INFO')

date_format = "%Y-%m-%dT%H:%M:%S"
R = random.randint

class Simulator:

  def __init__(self, num_devices, interval_secs):
    self.num_devices = num_devices
    self.interval_secs = interval_secs
    self.iot_server = IotAPI()
    self.sent_status = []
    self.device_history = []
    for _ in range(self.num_devices):
      self.sent_status.append([0, 0, 0, 0])
      self.device_history.append([])

  def create_json(self):
    json_dict_list = []
    for num in range(self.num_devices):
      sensor_name = f"sensor-{num + 1}"
      random_status_ind = R(0, 3)
      status = ["ON", "OFF", "ACTIVE", "INACTIVE"][random_status_ind]
      self.sent_status[num][random_status_ind] += 1
      self.device_history[num].append(status)

      json_dict = {"deviceId": sensor_name, "timestamp": datetime.datetime.now().strftime(date_format),
          "status": status, "pressure": R(1, 1000), "temperature": R(-100, 100)}
      json_dict_list.append(json_dict)
    return json_dict_list

  def send_json(self):
    return self.iot_server.send_sensor_json(self.create_json())

  def test_expected_status(self):
    for ind in range(self.num_devices):
      assert self.iot_server.get_sensor_histogram(f"sensor-{ind+1}") == self.sent_status[ind]
      assert self.iot_server.get_sensor_history(f"sensor-{ind+1}") == self.device_history[ind]

  def run(self):
    while True:
      assert self.send_json() == 0
      sleep(self.interval_secs)
      self.test_expected_status()


if __name__ == '__main__':
  simulator = Simulator(10, 2)
  simulator.run()


