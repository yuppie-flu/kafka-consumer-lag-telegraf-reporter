# kafka-consumer-lag-telegraf-reporter

A script to collect metrics from Kafka consumer group offsets and lag outputs InfluxDB Line protocol. Designed to work with Telegraf exec plugin.

https://docs.influxdata.com/influxdb/v0.9/write_protocols/line/
https://github.com/influxdata/telegraf/tree/master/plugins/inputs/exec

Works with Kafka 1.0 

**This script should be run on the Kafka broker node**

### Usage

```
python kafka_consumer_lag_reporter.py --kafka-dir=/path/to/kafka_2.11-1.0 --group some_group --bootstrap-server kafka-broker-host.com:9092
```

### Usage with telegraf

This script works with telegraf exec plugin. Just download this script and set the following configuration in your telegraf.conf

```
[[inputs.exec]]
    commands = ["python /path/to/kafka_consumer_lag_reporter.py --kafka-dir=/path/to/kafka_2.11-0.9.0.1 --group some_group --bootstrap-server kafka-broker-host.com:9092"]
    data_format = "influx"
```
