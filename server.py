#!/usr/bin/env python3.9

import grpc
import iot_pb2
import iot_pb2_grpc
from datetime import datetime
from config import Config
import asyncio
import storage
import logging
import os



class Service(iot_pb2_grpc.IotSenderServicer):

    def check(self, request):
      if request.timestamp == Config.int_default or not request.deviceId:
        return 1
      try:
        datetime.utcfromtimestamp(request.timestamp)
      except (OverflowError, OSError):
        return 2
      return 0

    def GetSensorData(self, request_iterator, _):
      ret = 0
      sql_db = storage.SqlStorage()
      for request in request_iterator:
        # Unfortunately sqlite3 doesn't send error codes.
        str_list = [request.deviceId, request.timestamp, request.pressure, request.status, request.temperature]
        logging.info("Received: %s", str(str_list))

        sql_db.append_to_table(deviceId=request.deviceId, timestamp=request.timestamp,
          pressure=request.pressure, status=request.status, temperature=request.temperature)
        logging.info("Date received: %s" % datetime.utcfromtimestamp(request.timestamp))
        ret = max(ret, self.check(request))
      sql_db.cursor.close()
      sql_db.connection.close()
      return iot_pb2.Reply(returnValue=ret)

    def SendSensorStatus(self, request, _):
      sql_db = storage.SqlStorage()
      status_freq = []
      for status in Config.status_dict:
        val = Config.status_dict[status]
        sql_object = sql_db.cursor.execute(f"SELECT COUNT(status) FROM {Config.table_name} "
            "WHERE deviceId = '%s' AND status = %d" % (request.deviceId, val))
        status_freq.append(sql_object.fetchone()[0])
      sql_db.cursor.close()
      sql_db.connection.close()
      return iot_pb2.SensorStatus(status_freq=status_freq)

    def SendSensorHistory(self, request, _):
      sql_db = storage.SqlStorage()
      status_freq = []
      sql_object = sql_db.cursor.execute(f"SELECT status FROM {Config.table_name} "
          "WHERE deviceId = '%s'" % (request.deviceId))
      status_freq = [x[0] for x in sql_object.fetchall()]
      sql_db.cursor.close()
      sql_db.connection.close()
      return iot_pb2.SensorStatus(status_freq=status_freq)

    def SendTopSensorId(self, request, _):
      sql_db = storage.SqlStorage()
      field = request.field
      sql_object = sql_db.cursor.execute(f"SELECT deviceId,{field} FROM {Config.table_name} "
          f"ORDER BY {field} DESC LIMIT 10")
      sql_object_populated = sql_object.fetchall()
      ids = [str(x[0]) for x in sql_object_populated]
      values = [float(x[1]) for x in sql_object_populated]
      return iot_pb2.TopSensorId(ids=ids, field=values)



# Handle exceptions
async def run_server():
    server = grpc.aio.server()
    iot_pb2_grpc.add_IotSenderServicer_to_server(Service(), server)
    address = "{}:{}".format(Config.hostname, Config.port)
    port = server.add_insecure_port(address)
    if port != Config.port:
      raise RuntimeError(f"Could not open port {address}")
    await server.start()
    logging.info(f"Server starting. PID: {os.getpid()}")
    await server.wait_for_termination()


if __name__ == '__main__':
  asyncio.run(run_server()) # Instead of threadpool we use async
