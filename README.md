#### Setup
```
bash setup.sh
source $PWD/venv/bin/activate
```

#### Test
`bash test.sh`

#### To start server

`python3 server.py`


#### To do functional testing and start the simulator

```
python3 -m pytest
python3 simulator.py
```

The rpc requests sent to the server are put to sqlite database called `canvass.db` (shared via LFS on this repo)

### Big picture

We send json using the method `send_sensor_json` in the `IotAPI` class in `client.py`.
We get info about the statuses using `get_sensor_historgram` and `get_sensor_history` from `IotAPI` class.

I assume when you say "histogram of the status for each given device id" to be the int array which
gives the total number of "ON", "OFF", "ACTIVE", "INACTIVE" status from which a histogram can be drawn.
If you meant the array of all the statuses for a given device, I can update my code for that.

The `Simulator` class has two attributes, `num_devices` and `interval_secs` which can be used to set the number of devices and the frequency with which the statues of the devices are sent.

The JSON is of format:
```
{
  "deviceId": str,
  "timestamp": int,
  "pressure": float,
  "status": enum {"ON", "OFF", "ACTIVE", "INACTIVE"},
  "temperature": int
}
```

