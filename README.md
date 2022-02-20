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

