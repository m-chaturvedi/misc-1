from typing import OrderedDict
import logging


class Config:
  hostname = "localhost"
  port = 5001
  sleep = True
  int_default = -1e6
  float_default = -1e6
  database_name = "canvass.db"
  table_name = "iot_sensor"
  # Ideally, this types info should be present only at one place, probably just
  # the proto code, and that should used to generate this.
  status_dict = OrderedDict({"ON": 1, "OFF": 2, "ACTIVE": 3, "INACTIVE": 4})
  sensor_table_types = OrderedDict({"deviceId": "str", "timestamp": "int",
    "pressure": "float", "status": "int", "temperature": "int"})
  logging.basicConfig(level='INFO')
