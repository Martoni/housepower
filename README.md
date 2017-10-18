# housepower
little web server and python script to log house power consumption


## Install

### Requirement

You need a raspberrypi with raspbian and python3

- python3
- python3-sqlite
- bokeh
- python3-flask
- pyaudio
- numpy

### Cron

Python scripts must be launched at Linux boot. For this we use cron :
```bash
$ sudo crontab -e

@reboot cd /opt/house_power/ && python3 recordwaves.py -d /run/hdata &
@reboot cd /opt/house_power/ && python3 waverms.py -d /run/hdata &
@reboot cd /opt/house_power/web/ && python3 house_power.py &
```

### Sqlite3
