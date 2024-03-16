from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient, Point
from config import config
from time import sleep
import requests as r
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%d.%m.%Y %H:%M:%S')

client = InfluxDBClient(url=config["influxdb"], token=config["accesstoken"], org=config["org"])
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

while True:
    try:
        res = r.get("http://{}/report".format(config["switchip"])).json()
        p = Point("solar-measure").tag("location", config["location"]).field("power", res["power"]).field("temperature", res["temperature"])
    except:
        logging.error("Error reading data from switch at http://{}/report".format(config["switchip"]))
    try:
        logging.info("Fetched data: "+str(p))
        write_api.write(bucket=config["bucket"], record=p)
    except:
        logging.error("Error sending data to Influx")
    
    sleep(config["interval"])
    